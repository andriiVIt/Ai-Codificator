from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Request Model
class CodeRequest(BaseModel):
    language: str
    description: str

# API Endpoint
@app.post("/generate_code")
def generate_code(request: CodeRequest):
    try:
        # Step 1: Validate Language
        language_validation_result = agent.run(f"Check if {request.language} is supported.")
        if "Error" in language_validation_result:
            raise HTTPException(status_code=400, detail=language_validation_result)

        # Step 2: Generate Code
        generated_code = agent.run({
            "language": request.language,
            "description": request.description
        })

        return {"language": request.language, "generated_code": generated_code}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run API Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
