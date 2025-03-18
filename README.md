# AI Code Generator

## Project Overview
This project is an AI-powered application designed to assist developers with code generation, explanation, and translation. It integrates a RESTful API using FastAPI, LangChain for LLM orchestration, and Flet for the user interface. The backend leverages multiple models from Ollama to ensure high-quality AI-driven coding assistance.

## Features
- **Generate Code**: Provide a natural language description and generate well-structured code.
- **Explain Code**: Input a code snippet and receive an explanation, including its logic and potential issues.
- **Translate Code**: Convert code from one programming language to another.
- **User Interface**: A graphical UI built using Flet for ease of interaction.

## Technologies Used
- **FastAPI** - API development framework.
- **LangChain** - Orchestrates different AI models and provides structured AI workflow.
- **Flet** - User interface framework.
- **Ollama Models**:
  - `llama3.2` for classification and decision-making.
  - `qwen2.5-coder` for code generation.
  - `codellama:7b` for code explanation and translation.
- **Pydantic** - Data validation and serialization.
- **Uvicorn** - ASGI server for running FastAPI applications.

## Installation
To install and run the project, follow these steps:

### 1. Clone the Repository
```sh
git clone https://github.com/andriiVIt/Ai-Codificator.git
cd codeGenerator
```

### 2. Install Dependencies
Ensure you have Python installed (preferably 3.11+). Then install the required packages:
```sh
pip install -r requirements.txt
```

### 3. Run the API Server
```sh
python CodeGeneratorServer.py
```
The API should now be running on `http://localhost:8080`.

### 4. Run the User Interface
```sh
python mainPage.py
```
This will launch the UI where you can interact with the AI code assistant.

## API Endpoints
| Endpoint       | Method | Description |
|---------------|--------|-------------|
| `/generateCode` | POST  | Generates code based on a natural language description. |
| `/translate`   | POST  | Translates code between programming languages. |
| `/explain_code` | POST  | Explains a given code snippet. |
| `/agent`       | POST  | Automatically detects the task and invokes the appropriate AI function. |

### Example Request
#### Generate Code
```sh
curl -X POST "http://localhost:8080/generateCode" \
-H "Content-Type: application/json" \
-d '{"language": "Python", "description": "Write a function that reverses a string."}'
```

### Example Response
```json
{
  "response": "def reverse_string(s):\n    return s[::-1]",
  "language": "Python"
}
```

## Future Improvements
- **Enhancing UI**: Improve the Flet-based UI with better error handling and user feedback.
- **More AI Models**: Experiment with additional AI models for better accuracy and performance.
- **User Preferences**: Allow users to set and save coding style preferences.

## Contribution
If you'd like to contribute to the project, feel free to fork the repository and submit pull requests!

## License
This project is licensed under the MIT License.
