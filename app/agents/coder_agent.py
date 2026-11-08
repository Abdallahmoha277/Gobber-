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
            "You are an expert Python programmer. \nWrite ONLY raw Python code. No explanations.\nIf 'Past Memory' is provided, use it as a reference.\nIf 'Feedback' is provided, fix the code based on this feedback.",
        ),
        ("human", "Task: {query}\n\nPast Memory:\n{memory}\n\nFeedback:\n{feedback}"),
    ]
)

coder_chain = prompt | llm | StrOutputParser()


def generate_code(query: str, memory: str = "", feedback: str = "") -> str:
    return coder_chain.invoke({"query": query, "memory": memory, "feedback": feedback})