# GPT Tools
让你的GPT上网。由于使用api请求gpt时，gpt无法使用插件进行上网查询，所以构建这个仓库。可以让你用API请求GPT的同时让GPT上网查询。

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
   cd llm-with-tool
