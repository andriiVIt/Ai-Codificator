from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from fastapi import HTTPException

class CodeTranslator:
    """Handles code translation between programming languages using LLM."""

    def __init__(self):
        self.llm = ChatOllama(model="codellama:7b", temperature=0)

        # Define the translation prompt
        self.code_translation_prompt = ChatPromptTemplate.from_template(
            """You are an assistant that translates code from one programming language to another.
            Translate the following code from {source_language} to {target_language}:
            Code: {code}
            Translated Code:"""
        )

        self.supported_languages = ["Python", "Java", "JavaScript", "C++"]

    def translate_code(self, source_language: str, target_language: str, code: str) -> str:
        """Translates code between languages using the model."""
        
        if source_language not in self.supported_languages or target_language not in self.supported_languages:
            raise HTTPException(status_code=400, detail="Both source and target languages must be one of: Python, Java, JavaScript, C++.")

        chain = self.code_translation_prompt | self.llm

        response = chain.invoke({
            "source_language": source_language,
            "target_language": target_language,
            "code": code
        })

        return response.content
