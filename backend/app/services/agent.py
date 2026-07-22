#Agent framework built on the OpenAI Agents SDK.
from __future__ import annotations

from functools import lru_cache

from agents import Agent, Runner, WebSearchTool, set_default_openai_client
from openai import AsyncOpenAI

from app.core.config import get_settings
from app.services.prompts import MESSAGE_INSTRUCTIONS, REPORT_INSTRUCTIONS


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
        instructions: str = MESSAGE_INSTRUCTIONS,
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
    """Lazily build and cache the message/report agents.

    Both agents get a hosted web-search tool so they can look up
    up-to-date mental-health resources (research papers, ICD-11, DSM-5, etc.).
    """
    service = get_agent_service()
    message_agent = service.create_agent(
        name="Message_Agent",
        instructions=MESSAGE_INSTRUCTIONS,
        tools=[WebSearchTool()],
    )
    report_agent = service.create_agent(
        name="Report_Agent",
        instructions=REPORT_INSTRUCTIONS,
        tools=[WebSearchTool()],
    )
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