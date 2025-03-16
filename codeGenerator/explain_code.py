from fastapi import FastAPI, HTTPException
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import initialize_agent, AgentType
from LanguageRecognitionTool import LanguageRecognition
from pydantic import BaseModel

# Define a data model for input validation
class CodeInput(BaseModel):
    code: str


class ExplainCode:     
    def __init__(self):
        
        self.languageRecognition = LanguageRecognition()

        self.model = ChatOllama(model="codellama:7b", temperature=0)

  
        self.agent = initialize_agent(
            tools=[self.languageRecognition.language_detection_tool],
            llm=self.model,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )

    def explain_code(self, data: CodeInput):
        """Detects the language and explains the given code snippet."""

       
        detected_language = self.agent.invoke({"input": {"code": data.code}})

        explain_code_prompt = ChatPromptTemplate.from_template(
            """You are a helpful assistant that explains code in detail.

            Below are some examples of how to explain code:

            Example 1:
            Code (Python):
            def multiply(a, b):
                return a * b

            Explanation:
            1. This function multiplies two numbers.
            2. It assumes the inputs are numeric.
            3. To improve, you might add input validation.

            Example 2:
            Code (Python):
            try:
                result = 10 / 0
            except ZeroDivisionError:
                print("Cannot divide by zero")

            Explanation:
            1. This snippet demonstrates error handling for division by zero.
            2. It uses a try-except block to catch the ZeroDivisionError.
            3. A suggestion could be to handle the error more gracefully or log it.

            Now, consider the following code written in {language}:

            {code}

            Please provide:
            1. A clear summary of what the code does.
            2. Potential edge cases or errors the user should watch out for.
            3. Suggestions on how to run, improve, or debug the code.

            Answer:
            """
        )

      
        chain = explain_code_prompt | self.model
        response = chain.invoke({"code": data.code, "language": detected_language})

        return {"response": response.content, "language": detected_language}
