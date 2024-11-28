# GPT Tool Integration with Python Interpreter

This project integrates OpenAI's GPT with a set of custom tools, including a restricted Python interpreter. The Python interpreter is sandboxed to ensure security and prevent unauthorized access to the system while running user-provided code. Additionally, the project supports a variety of tools such as making URL requests and performing internet searches.

## Features

- **GPT-4 Integration**: Utilizes OpenAI's GPT-4 for generating responses based on user input.
- **Python Interpreter**: Executes Python code in a restricted environment with a 5-second timeout limit to avoid long-running processes.
- **Tool Calls**: Supports calling external tools such as `url-get` (fetch webpage content) and `search` (search the web with a keyword).

## Dependencies

- Python 3.x
- OpenAI API (API key required)
- `subprocess` (for running code securely)
- `json` (for handling data serialization)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/LanYangYang321/llm-with-tool
   cd gpt-python-interpreter
