from langchain_core.prompts import PromptTemplate,ChatPromptTemplate
from langchain_core.tools import Tool
from langchain_ollama import OllamaLLM
from langchain.agents import initialize_agent, AgentType


class CodeGenerator:
    def __init__(self):
        self.model = OllamaLLM(model="qwen2.5-coder:latest" , temperature=0) 
        self.example_prompt = ChatPromptTemplate.from_template("""
        You are an expert software engineer. Generate well-structured, clean, and maintainable {language} code 
        based on the description provided. Use best practices, including SOLID principles, DRY, and KISS.

        ### Example 1:
        **Language:** Python  
        **Description:** Write a function to check if a number is even or odd.  
        **Output:**
        ```
        def is_even(n):
            return n % 2 == 0
        ```

        ### Example 2:
        **Language:** JavaScript  
        **Description:** Create a function that returns the square of a number.  
        **Output:**
       
        ```
        function square(n) 
            return n * n;
        ```

        ### Now generate code for the following:

        **Language:** {language} 
        **Description:** {description} 
        **Output:**
        """)

        self.code_generation_prompt = PromptTemplate(
          input_variables=["generated_code"],
            template="""
            Act as a Senior Developer reviewing this code.
            Analyze and improve the solution using best practices.
            Identify pros and cons, potential optimizations, and scalability concerns.
            Ensure:
            - SOLID principles
            - Simplicity (KISS)
            - No redundancy (DRY)
            - Necessary components only (YAGNI)
            
            Given code:
            ```
            {generated_code}
            ```
            Provide improvements and explanation together with the given code:
            """
        )


        self.code_generation_chain  = self.example_prompt|self.model
        self.code_generation_check= self.code_generation_prompt|self.model

        self.code_generation_tool = Tool(
            name="CodeGenerator",
            func=self.generate_code_tool, 
            description="Generates code in a provided programming language and  a description. Arguments: language (str), description (str)." ,
            args_schema=None 
        )

    
        self.agent = initialize_agent(
            tools=[self.code_generation_tool],
            llm=self.model,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )

    def generate_code_tool(self, inputs):
        print(inputs + "printing inputs")
        if isinstance(inputs, str):
            inputs = {"language": inputs, "description": inputs}

        generated_code= self.code_generation_chain.invoke(
            {"language": inputs["language"], "description": inputs["description"]}
        )
        return self.code_generation_check.invoke({"generated_code":generated_code})

    def generate_code(self, language, description):
        structured_input = {
            "language": language,
            "description": description
        }
      
        response = self.agent.invoke({"input": structured_input})
        print(f"Response Type: {type(response)}") 
        return response


