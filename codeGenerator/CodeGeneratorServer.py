from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ollama import Client  
from CodeGenerator import CodeGenerator

app = FastAPI()

# Define request model
class Prompt(BaseModel):
    language: str
    description: str

# Define response model
class ResponseModel(BaseModel):
    response: str    

@app.post("/generateCode", response_model=ResponseModel)
async def translateItem(item: Prompt):
    try:
        codeGenerator = CodeGenerator()  
        generated_code = codeGenerator.generate_code(item.language, item.description)
        print("Printing the response object")
        print (generated_code)
        return ResponseModel(response=generated_code.get("output"))
         
    except Exception as e:
        return ResponseModel(response=f"Error generating code: {str(e)}")
        # raise HTTPException(status_code=500, detail=f"Error generating code: {str(e)}") 

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8080)
