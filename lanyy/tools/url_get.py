import requests
from bs4 import BeautifulSoup

headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
}
proxy = "http://127.0.0.1:7890"


def url_get(url):
    # Function to fetch the content of the URL
    try:
        response = requests.get(url, proxies={"http": proxy, "https": proxy}, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # 提取所有文本内容
            text = soup.get_text().replace("\n", "")
            return text + f"\nstatus code = {response.status_code}"
        else:
            return f"Error fetching the URL: status code = {response.status_code}, but you can still try to fetch other urls."
    except requests.exceptions.RequestException as e:
        return f"An error occurred when fetching the url: {str(e)}, but you can still try to fetch other urls."

