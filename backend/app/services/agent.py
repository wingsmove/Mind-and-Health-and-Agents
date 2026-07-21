#Agent framework built on the OpenAI Agents SDK.
from __future__ import annotations

from functools import lru_cache

from agents import Agent, Runner, set_default_openai_client
from openai import AsyncOpenAI

from app.core.config import get_settings

DEFAULT_INSTRUCTIONS = "You are a helpful assistant."


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
        name: str = "Assistant",
        instructions: str = DEFAULT_INSTRUCTIONS,
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

#Placeholder for the actual agent run function.
    async def run(self, user_input: str, *, agent: Agent | None = None) -> str:
        result = await Runner.run(agent or self._default_agent, user_input)
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
