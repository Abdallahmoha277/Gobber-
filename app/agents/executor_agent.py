import requests

SANDBOX_URL = "http://localhost:7070/execute"


def execute_code(code: str) -> tuple[str, str]:
    try:
        response = requests.post(SANDBOX_URL, json={"code": code}, timeout=15)
        response.raise_for_status()
        result = response.json()
        return result.get("stdout", ""), result.get("stderr", "")
    except Exception as e:
        return "", f"Execution Error: {str(e)}"
