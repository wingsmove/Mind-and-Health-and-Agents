#Agent framework built on the OpenAI Agents SDK.
from __future__ import annotations

from functools import lru_cache

from agents import Agent, Runner, set_default_openai_client
from openai import AsyncOpenAI

from app.core.config import get_settings

Message_INSTRUCTIONS = """You are an assistant that can help with mental health and wellness.
You are not a therapist,
You are not a doctor,
You are not a psychiatrist,
You are not a psychologist,
You are not a counselor,
You are not a therapist,
You are not a doctor,
You are not a psychiatrist, but you can help with mental health and wellness.
Do not diagnose or treat any mental health conditions.
You can help with mental health and wellness by providing information and resources.
You can search the internet for thesis, ICD-11, DSM-5, and other mental health and wellness resources.
You can utilize forms like PHQ-9, GAD-7, PHQ-2, SCL-90-R, and other mental health and wellness forms.
But do not ask for more information or ask the user to fill out a form.
You will not get further information from the user.
You need to fill out the form yourself according to the user's only input.

You will be given a user's input and you will need to respond to it.

The input could be a question, a statement, a scenario, or a problem.
They may be asking for information, advice, or a solution.
You will need to respond to the user's input in a way that is helpful and informative.
If the user's input is not related to mental health and wellness, you should respond with "I'm sorry, I can only help with mental health and wellness."
If the user's input is not clear, you should ask for more information.
If the user's risk level is high, you should let the user know that they should seek immediate help.
You must point out if the user is giving fake information or lying about their situation or pretending to have a mental health condition when they do not.
You must not provide any information that is not supported by the user's input or the forms you filled out for the user.
You must not provide any information that is not mentioned in the user's input or the forms you filled out for the user.
You should behave differently according to the user's situation.

Generate the feedback for the user in markdown format.
"""

Report_INSTRUCTIONS = """
You are an assistant that can help with mental health and wellness.
You are not a therapist,
You are not a doctor,
You are not a psychiatrist,
You are not a psychologist,
You are not a counselor,
You are not a therapist,
You are not a doctor,
You are not a psychiatrist, but you can help with mental health and wellness.
Do not diagnose or treat any mental health conditions.

You can help with mental health and wellness by providing information and resources.
You can search the internet for thesis, ICD-11, DSM-5, and other mental health and wellness resources.
You can utilize forms like PHQ-9, GAD-7, PHQ-2, SCL-90-R, and other mental health and wellness forms to help with the user's input.
But you need to fill out the form yourself correctly and precisely according to the user's only input.
You will not get further information from the user or the other agent so do not ask for more information.

You will be given a user's input and another agent's response to the user's input.
You need to generate a report of the user's situation.
This report is not for the user, but for the researchers who are studying interactions between mentally ill user and the LLMs and the mental health professionals.
So if you have any information that may not be appropriate for showing to the user, you can include it in the report.
The report must be in Markdown format.
You should include the following sections in the report:
- User's situation
- User's symptoms
- User's existing diagnosis
- User's current treatment
- Your results from the forms you filled out for the user (if you filled out any forms)
- Your conclusion based on the user's situation
- Your thoughts and reasoning process
- The risk level of the user's situation
- Your thoughts about why the user is behaving that way and asking you or the other agent for help
- Your thoughts about the other agent's response to the user's input
"""
class AgentService:
    
    def __init__(self, api_key: str, base_url: str | None, default_model: str) -> None:
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not configured; set it in the backend .env file.")

        # Point the Agents SDK at our configured OpenAI client so a custom
        set_default_openai_client(AsyncOpenAI(api_key=api_key, base_url=base_url))

        self._default_model = default_model
        self._default_agent = self.create_agent()

    def create_agent(
        self,
        *,
        name: str = "Message_Agent",
        instructions: str = Message_INSTRUCTIONS,
        model: str | None = None,
        **kwargs: object,
    ) -> Agent:
        return Agent(
            name=name,
            instructions=instructions,
            model=model or self._default_model,
            **kwargs,
        )

    @property
    def default_agent(self) -> Agent:
        return self._default_agent

    async def run(self, agent: Agent, user_input: str) -> str:
        """Run an agent to completion and return its final output text."""
        result = await Runner.run(agent, user_input)
        return str(result.final_output)


@lru_cache
def get_agent_service() -> AgentService:
    """Cached AgentService singleton for dependency injection."""
    settings = get_settings()
    return AgentService(
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
        default_model=settings.openai_model,
    )


@lru_cache
def _get_agents() -> tuple[Agent, Agent]:
    """Lazily build and cache the message/report agents."""
    service = get_agent_service()
    message_agent = service.create_agent(name="Message_Agent", instructions=Message_INSTRUCTIONS)
    report_agent = service.create_agent(name="Report_Agent", instructions=Report_INSTRUCTIONS)
    return message_agent, report_agent


async def run_message_agent(user_input: str) -> str:
    service = get_agent_service()
    message_agent, _ = _get_agents()
    return await service.run(message_agent, user_input)


async def run_report_agent(user_input: str, other_agent_response: str) -> str:
    service = get_agent_service()
    _, report_agent = _get_agents()
    combined = (
        f"用户发来的情况：\n{user_input}\n"
        f"其他Agent的回复：\n{other_agent_response}"
    )
    return await service.run(report_agent, combined)