from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import uvicorn

app = FastAPI()

llm = ChatOllama(model="codellama:7b", temperature=0)

class RequestData(BaseModel):
    source_language: str
    target_language: str
    code: str


code_translation_prompt = ChatPromptTemplate.from_template(
    """You are an assistant that translates code from one programming language to another.
    Translate the following code from {source_language} to {target_language}:
    Code: {code}
    Translated Code:"""
)

@app.post("/translate")
async def translate_code(data: RequestData):

    supported_languages = ["Python", "Java", "JavaScript", "C++"]
    
    if data.source_language not in supported_languages or data.target_language not in supported_languages:
        raise HTTPException(status_code=400, detail="Both source and target languages must be one of: Python, Java, JavaScript, C++.")

    
   
    chain = code_translation_prompt | llm

    response = chain.invoke({
        "source_language": data.source_language,
        "target_language": data.target_language,
        "code": data.code
    })
    
    return {"translated_code": response.content}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)