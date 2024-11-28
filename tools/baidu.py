import requests
from bs4 import BeautifulSoup
import re
import time
from random import choice


# 创建headers字段
def baidu_search(keyword, pagenum=1):
    def createUA():
        # 运行该程序前：请打开浏览器前往"https://www.baidu.com"手动登录自己的百度账户，按F12打开开发者模式，选择最上面一排Network/网络选项卡
        # 接着按F5刷新本网页，捕获到的请求里一直往上翻到最顶端，选择第一次请求（即名称为www.baidu.com的请求）。
        # 再选择右侧标头选项卡，往下滑到请求标头处，将Cookie字段的值全部复制下来（有很长一段的）替换掉下行的****** 替换后可直接运行该文件
        ua = {'Host': 'www.baidu.com',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54'}
        return ua
        # 程序运行无数据返回爬不了的时候，浏览器直接刷新继续按上述方法换字典里的Cookie值就完事了


    # 将百度搜索链接给予的加密URL转化为真实的URL
    def convertRealUrl(url, s2):
        try:
            headers = createUA()
            realR = s2.get(url=url, headers=headers, allow_redirects=False)
            # 当请求加密链接，初两次响应的Http报文往往告知浏览器需要重定向，最初两次的响应报文里才有Location属性来告知浏览器需要重定向到的真实网站链接。
            # 此时我们不允许会话自动根据给出的Location重定向跳转，因为允许重定向后会自动跳到最新的真实的URL站点，这时就只返回最新站点的响应HTTP报文（已完成重定向后），此时响应标头里不再有指示重定向url的Location字段。此方法就会失效！
            return realR.headers['Location']
        except:
            return None  # 如果找不到Location头部字段无法返回真实链接，那么就返回原来的加密链接


    # 获取搜索页
    def getSearchPage(keyword, pn, s1):
        headers = createUA()
        url = 'http://www.baidu.com/s'
        payload = {'wd': keyword, 'pn': pn}
        try:
            r = s1.get(url, headers=headers, params=payload, timeout=30)
            r.raise_for_status()
            r.encoding = 'utf-8'
            return r.text
        except:
            return "状态码异常"


    # 升级！爬取一页的标题和真实链接
    def upgradeCrawler(html, s2):
        soup = BeautifulSoup(html, 'lxml')
        titles = []
        links = []
        for h3 in soup.find_all('h3', {'class': re.compile('c-title t')}):
            try:
                # a.text为获取该路径下所有子孙字符串吧。可能刚好a元素和em元素间没有换行符，所以抓取的字符串里没有\n换行符
                g_title = h3.a.text.replace('\n', '').replace(',', ' ').strip()  # 去掉换行和空格，部分标题中还有逗号会影响CSV格式存储，也要去除。
                g_url = h3.a.attrs['href']
                g_url = convertRealUrl(g_url, s2)
                if g_url:
                    titles.append(g_title)
                    links.append(g_url)
            except:
                pass
        return titles, links


    # 顶层设计

    titles = []
    links = []
    # s1会话用于获取搜索结果页
    s1 = requests.session()
    # s2会话用于转真实URL
    s2 = requests.session()
    # 第1页为0，第2页为10，第3页为20，依次类推
    num = pagenum * 10
    for pn in range(0, num, 10):
        html = getSearchPage(keyword, pn, s1)
        ti, li = upgradeCrawler(html, s2)
        titles += ti
        links += li
        time.sleep(5)
    result = []
    i = 0
    for title in titles:
        #result.append(f"{title} {links[i]}")
        result.append(f"{links[i]}")
        i += 1
    print("baidu success")
    return result


if __name__ == '__main__':
    print(baidu_search("编程"))
