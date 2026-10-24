import os
import subprocess
import tempfile
from fastapi import FastAPI

app = FastAPI()


@app.post("/execute")
async def execute_code(payload: dict):
    code = payload.get("code", "")
    if not code:
        return {"stdout": "", "stderr": "No code provided"}

    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            suffix=".py", mode="w", delete=False, encoding="utf-8"
        ) as file:
            file.write(code)
            temp_path = file.name

        result = subprocess.run(
            ["python", temp_path],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return {"stdout": result.stdout, "stderr": result.stderr}
    except subprocess.TimeoutExpired:
        return {"stdout": "", "stderr": "Execution timed out"}
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
