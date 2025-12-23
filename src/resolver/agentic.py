from pydantic import SecretStr
from langchain.agents import create_agent
from langchain.messages import HumanMessage, SystemMessage
from langchain_openai.chat_models import ChatOpenAI
from src.constants import (
    AGENTIC_API_KEY,
    AGENTIC_BASE_URL,
    AGENTIC_MODEL,
    SYSTEM_PROMPT,
)
from src.resolver.tools.research import research_topic
from src.resolver.tools.visitor import visit_news


class AgenticResolver:
    def __init__(self) -> None:
        model = ChatOpenAI(
            model=AGENTIC_MODEL,
            base_url=AGENTIC_BASE_URL,
            api_key=SecretStr(AGENTIC_API_KEY),
            temperature=0.1,
        )
        self.agentic = create_agent(
            model=model,
            tools=[
                research_topic,
                visit_news,
            ],
            system_prompt=SYSTEM_PROMPT,
        )

    def invoke(self, question: str) -> str:
        response = self.agentic.invoke(
            {
                "messages": [
                    SystemMessage(
                        "Please search for relevant information to answer the following question."
                    ),
                    HumanMessage(question),
                ]
            }
        )

        return response["messages"][-1].content
