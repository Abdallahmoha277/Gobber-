from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.core.config import settings


llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=settings.DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com",
    temperature=0.0,
)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a router agent. Classify the user's query into one of these three categories:
- 'qa': General question answering.
- 'research': Questions requiring external information or web search.
- 'code': Requests involving writing, fixing, or modifying code.

Respond with ONLY one word: qa, research, or code.""",
        ),
        ("human", "{query}"),
    ]
)


router_chain = prompt | llm | StrOutputParser()


def route_query(query: str) -> str:
    """يستقبل سؤال المستخدم ويعيد المسار المناسب"""
    result = router_chain.invoke({"query": query}).strip().lower()

    if result in ["qa", "research", "code"]:
        return result
    return "qa"
