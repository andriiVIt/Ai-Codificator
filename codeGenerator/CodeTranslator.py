from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from fastapi import HTTPException
from langchain_core.tools import Tool
from langchain.agents import initialize_agent, AgentType

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

        self.supported_languages = ["Python", "Java", "JavaScript", "C++","C#","TypeScript"]

        self.code_translation_tool = Tool(
            name="CodeTranslator",
            func=self.translate_code, 
            description="Translates code between languages using a code snipet, given  source_language and target_language. Arguments: code (str), source_language (str),target_language (str) ." ,
            args_schema=None 
        )
        self.agent = initialize_agent(
          tools=[self.code_translation_tool],
          llm=self.llm,
          agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
          verbose=True
        )

    def translate_code(self, source_language: str, target_language: str, code: str) -> str:
        """Translates code between languages using the model."""
        
        if source_language not in self.supported_languages or target_language not in self.supported_languages:
            raise HTTPException(status_code=400, detail="Both source and target languages must be one of: Python, Java, JavaScript, C++,C#,TypeScript.")
        chain = self.code_translation_prompt | self.llm
        response = chain.invoke({
            "source_language": source_language,
            "target_language": target_language,
            "code": code
        })

        return response.content
    
    def translate_code(self, source_language: str, target_language: str, code: str):
        structured_input = {
            "source_language": source_language,
            "target_language": target_language,
            "code":code
        }
        response = self.agent.invoke({"input": structured_input})
        print(f"Response Type: {type(response)}") 
        return response
