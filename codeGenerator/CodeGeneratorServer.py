from fastapi import FastAPI
from pydantic import BaseModel
from ollama import Client  
from CodeGenerator import CodeGenerator
from CodeTranslator import CodeTranslator
from langchain_ollama import ChatOllama
from explain_code import LanguageRecognition
app = FastAPI()
   

class Prompt(BaseModel):
    language: str
    description: str


class ResponseModel(BaseModel):
    response: str
    language:str

class RequestData(BaseModel):
    source_language: str
    target_language: str
    code: str

class ExplainRequestData(BaseModel):
    code: str 


@app.post("/generateCode", response_model=ResponseModel)
async def translateItem(item: Prompt):
    try:
        codeGenerator = CodeGenerator() 
        generated_code = codeGenerator.generate_code(item.language,item.description)
        return ResponseModel(response=generated_code.get("output"),language=item.language)
    except Exception as e:
        return ResponseModel(response=f"Error generating code: {str(e)}",language=item.language)
     
@app.post("/translate",response_model=ResponseModel)
async def translate_code(data: RequestData):
    """API route to translate code between languages."""
    print(data.code)
    translated_code = CodeTranslator().translate_code(data.source_language, data.target_language, data.code)
    return ResponseModel(response=translated_code,language=data.target_language)
    

@app.post("/explain_code",response_model=ResponseModel)
async def explain_code(data: ExplainRequestData):
    print(data)
    """
    POST /explain_code endpoint.
    Receives a code snippet in the request body, automatically detects its programming language,
    and returns a detailed explanation that takes into account the specific language and context.
    """
    languageRecognition = LanguageRecognition()
    response = languageRecognition.explainCode(data)
    print(response)
    return response
    

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8080)
