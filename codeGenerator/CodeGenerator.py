from langchain_core.prompts import PromptTemplate,ChatPromptTemplate
from langchain_core.tools import Tool
from langchain_ollama import OllamaLLM
from langchain.agents import initialize_agent, AgentType


class CodeGenerator:
    def __init__(self):
        self.model = OllamaLLM(model="qwen2.5-coder:latest" , temperature=0) 
        # self.example_prompt = ChatPromptTemplate.from_template("""
        # You are an expert software engineer. Generate well-structured, clean, and maintainable {{language}} code 
        # based on the description provided. Use best practices, including SOLID principles, DRY, and KISS.

        # ### Example 1:
        # **Language:** Python  
        # **Description:** Write a function to check if a number is even or odd.  
        # **Output:**
        # ```
        # def is_even(n):
        #     return n % 2 == 0
        # ```

        # ### Example 2:
        # **Language:** JavaScript  
        # **Description:** Create a function that returns the square of a number.  
        # **Output:**
       
        # ```
        # function square(n) {{
        #     return n * n;
        # }}
        # ```

        # ### Now generate code for the following:

        # **Language:** {{language}}  
        # **Description:** {{description}}  
        # **Output:**
        # """)

        self.code_generation_prompt = PromptTemplate(
            input_variables=["language", "description"],
            template="""
             Act as a Developer
             The code should be consistent, deploy the same architecture and style throughout the solution.
             Align with SOLID principles.
             Write code as simple as possible: KISS.
             Avoid repetition: DRY.
             Delete what is not needed: YAGNI.
             Prefer small methods, with 0-1 argument, having max 2 arguments when necessary reasonable.
             The code should be consistent, deploy the same architecture and style throughout the project.
             The code solution should be followed by a description of why this is the chosen solution and you must also provide pros and cons for the solution together with a description of the limitations in the suggestion solution and how it might be optimized.
             Generate a clean, efficient, and well-commented {{language}}
             program based on the following description:  {{description}}
            """
        )

      

        self.code_generation_chain = self.example_prompt|self.code_generation_prompt|self.model

       
        self.code_generation_tool = Tool(
            name="CodeGenerator",
            func=self.generate_code_tool, 
            description="Generates code in a provided programming language and a description.",
            args_schema=None 
        )

    
        self.agent = initialize_agent(
            tools=[self.code_generation_tool],
            llm=self.model,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )

    def generate_code_tool(self, inputs):
        if isinstance(inputs, str):
            inputs = {"language": inputs, "description": inputs}

        return self.code_generation_chain.invoke(
            {"language": inputs["language"], "description": inputs["description"]}
        )

    def generate_code(self, language, description):
        structured_input = {
            "language": language,
            "description": description
        }
      
        response = self.agent.invoke({"input": structured_input})
        print(f"Response Type: {type(response)}") 
        return response


