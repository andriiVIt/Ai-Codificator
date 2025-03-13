from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ollama import Client  
from CodeGenerator import CodeGenerator
from codeGenerator.CodeTranslator import CodeTranslator
import json
app = FastAPI()

# Define request model
class Prompt(BaseModel):
    language: str
    description: str

# Define response model
class ResponseModel(BaseModel):
    response: str
    language:str

class RequestData(BaseModel):
    source_language: str
    target_language: str
    code: str


@app.post("/generateCode", response_model=ResponseModel)
async def translateItem(item: Prompt):
    try:
        # codeGenerator = CodeGenerator()  
        # generated_code = codeGenerator.generate_code(item.language, item.description)
    


        # return ResponseModel(response=generated_code.get("output"),language=item.language)
 
     code_string = "\n".join([f"print('This is line {i + 1}')" for i in range(100)])

     return ResponseModel(response=json.dumps({
    # "code": "def add(a, b):\n    return a + b\n\nprint(add(2, 3))"
    "code": code_string 
}), language=item.language)

         
    except Exception as e:
        return ResponseModel(response=f"Error generating code: {str(e)}")
        # raise HTTPException(status_code=500, detail=f"Error generating code: {str(e)}") 

@app.post("/translate")
async def translate_code(data: RequestData):
    """API route to translate code between languages."""
    # translated_code = CodeTranslator.translate_code(data.source_language, data.target_language, data.code)
    code_string = "\n".join([f"print('This is line {i + 1}')" for i in range(100)])
    return {"translated_code": code_string}
 

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8080)
