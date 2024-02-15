from bs4 import BeautifulSoup
import requests
import os
def main():
    #url = "https://mojim.com/cnh100951.htm"  #歌手的歌曲列表
    url = input("请输入歌曲列表URL:")
    # 发送HTTP请求
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=lambda href: href and href.endswith('.htm'))
            #提取不同歌曲链接
            for link in links:
                getSongLyric("https://mojim.com/"+link['href'])
        else:
            print("请求失败，状态码：", response.status_code)
    except Exception as e:
        print("爬取发生异常:"+str(e))

def write_to_file(path, filename, content):
    # 检查路径是否存在
    full_path = os.path.join(path, filename)
    if not os.path.exists(path):
        # 如果路径不存在，创建目录
        os.makedirs(path)
    with open(full_path, 'w', encoding='utf-8') as file:
        file.write(content)
def getSongLyric(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            lyricNode = soup.find('dl', class_='fsZx1')
            if lyricNode:
                songName = soup.find('dt', class_='fsZx2').text
                for br in lyricNode.find_all("br"):
                    br.replace_with("\n")
                # 获取没有HTML标签的文本
                text_only = lyricNode.get_text()
                write_to_file('lyrics', songName + '.txt', text_only)
                print("歌曲:"+ songName + " 歌词爬取成功")
    except Exception as e:
        print("URL:"+ url +" 爬取发生异常:"+str(e) +"位于行:"+str(e.__traceback__.tb_lineno))

if __name__ == '__main__':
    main()
