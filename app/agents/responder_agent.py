from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.core.config import settings

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=settings.DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com",
    temperature=0.7,
)
prompt = ChatPromptTemplate.from_messages(
    [("system", "You are a helpful assistant. Answer clearly."), ("human", "{query}")]
)
responder_chain = prompt | llm | StrOutputParser()


def generate_response(query: str) -> str:
    return responder_chain.invoke({"query": query})
