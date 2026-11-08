from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.core.config import settings

llm = ChatOpenAI(model="deepseek-chat", api_key=settings.DEEPSEEK_API_KEY, base_url="https://api.deepseek.com", temperature=0.0)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a strict code reviewer. Analyze the provided code and its execution output.
If there is an error or the output is incorrect, respond with 'FAIL' followed by a brief explanation of the issue.
If the code ran successfully and the output is correct, respond with 'PASS'."""),
    ("human", "Task: {query}\n\nCode:\n{code}\n\nExecution Output/Error:\n{output}")
])

critic_chain = prompt | llm | StrOutputParser()

def evaluate_code(query: str, code: str, output: str) -> tuple[bool, str]:
    response = critic_chain.invoke({"query": query, "code": code, "output": output})
    
    if response.strip().startswith("PASS"):
        return True, "Success"
    
    return False, response