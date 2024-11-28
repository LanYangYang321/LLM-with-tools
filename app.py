import json
from bs4 import BeautifulSoup
import openai
import requests
from tools.baidu import baidu_search
from tools.url_get import url_get

proxy = "http://127.0.0.1:7890"

# 设置 OpenAI API 密钥
openai.api_base = 'https://chatapi.littlewheat.com/v1'
openai.proxy = {
    "http": proxy,
    "https": proxy,
}

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
}


def gpt_with_requests(api_key, question, messages=None, recursion_depth=0, max_recursion_depth=3):
    openai.api_key = api_key
    # Make request to OpenAI ChatCompletion API
    if messages is None:
        messages = [{"role": "user", "content": question}]
    # Check for tool call
    print("[info]携带的历史信息:", messages)
    if recursion_depth == max_recursion_depth:
        print("[info]本次请求不提供工具")
        # 到达递归深度上线，不提供工具
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # or gpt-3.5-turbo
            messages=messages,
            tool_choice="auto",
            temperature=0.7,  # 控制生成文本的随机性
            max_tokens=1000  # 设置回答的最大长度
        )
    else:
        print("[info]本次请求提供工具")
        # 未到达深度上线，提供工具
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # or gpt-3.5-turbo
            messages=messages,
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "url-get",
                        "description": "Request a specific url, returns the status code and the webpage content",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "url": {
                                    "type": "string",
                                    "description": "The website url to request, e.g. https://www.github.com"
                                }
                            },
                            "required": ["url"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "search",
                        "description": "Search the internet with a keyword, returns relevant website urls",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "keyword": {
                                    "type": "string",
                                    "description": "The keyword you want to search, e.g. apple"
                                }
                            },
                            "required": ["keyword"]
                        }
                    }
                }
            ],
            tool_choice="auto",
            temperature=0.7,  # 控制生成文本的随机性
            max_tokens=1000  # 设置回答的最大长度
        )
        tool_calls = response['choices'][0]['message'].get('tool_calls', 'None')

        # If tool_calls is not None, convert it to a clean JSON string
        if tool_calls != 'None':
            tool_calls_json = json.dumps(tool_calls, ensure_ascii=False,
                                         indent=None)  # Ensures no extra spaces or indentation
            messages.append({"role": "assistant", "content": f"call_tools: {tool_calls_json}"})
            print(f"[info]GPT:{tool_calls_json}")
        else:
            content = response['choices'][0]['message']['content']
            messages.append({"role": "assistant", "content": f"{content}"})
            print(f"[info]GPT:{content}")

    tool_calls = response['choices'][0]['message'].get('tool_calls', [])

    # 持续递归调用工具，直到停止或达到次数上限
    if tool_calls:
        for tool_call in tool_calls:
            if not (isinstance(tool_call, dict) and tool_call['type'] == 'function'):
                return "[error]GPT工具调用格式错误"
            if tool_call['function']['name'] == 'url-get':
                # Deserialize the 'arguments' string to a dictionary
                arguments = json.loads(tool_call['function']['arguments'])
                url = arguments.get('url')
                if url:
                    # Fetch the content of the URL
                    url_content = url_get(url)
                    # Append the fetched content to messages for the next recursion
                    messages.append({"role": "url-get", "content": url_content})
                    # Recursively call the function with updated messages
                else:
                    messages.append({"role": "url-get", "content": "No URL found in tool call arguments."})
            if tool_call['function']['name'] == 'search':
                # Deserialize the 'arguments' string to a dictionary
                arguments = json.loads(tool_call['function']['arguments'])
                keyword = arguments.get('keyword')
                if keyword:
                    # Search keyword on baidu
                    url_content = baidu_search(keyword)
                    # Append the fetched content to messages for the next recursion
                    messages.append({"role": "search", "content": url_content})
                    # Recursively call the function with updated messages
                else:
                    messages.append({"role": "search", "content": "No keyword found in tool call arguments."})

        return gpt_with_requests(api_key, question, messages, recursion_depth=recursion_depth + 1)

    # If no tool call, just return the content generated by the model
    return response['choices'][0]['message']['content']


if __name__ == "__main__":
    # 输入 OpenAI API 密钥和问题
    api_key = "sk-Boq4p7UH7lbzybrEQPmve7HJA01QAwgoFuCKjgQZbBPzCDqS"  # 替换为你的 OpenAI API 密钥
    question = "英伟达最新股价"

    # 调用函数获取回答
    answer = gpt_with_requests(api_key, question)
    print("[final]AI 的回答:")
    print(answer)
