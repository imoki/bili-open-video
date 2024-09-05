
'''
    名称：bilibili合集最新一期视频自动打开
    简介：自动打开浏览器并打开某合集视频中的最新一期视频。可将bat脚本加入开机自启动，开机时自动打开最新一期视频。
    算法：比较最后5个。将日期转成小数，进行比较，取到最新一期视频，若有多个最新期视频，则取其中的第一个。
    作者：imoki
    仓库：https://github.com/imoki/bili-open-video
    更新时间：2024-09-05
'''

import requests
import webbrowser
import re

# 全局变量，可自行修改
bvid = 'BV1fJ4m1T7dN'   # 填写合集的的bvid号
pattern = r"/(\d+\.\d+)】"  # 填写正则匹配。例如标题为：“【论国际/8.27】博弈转折点” ，可提取出其中的日期 8.27
urlDynamic = "https://space.bilibili.com/650014862/dynamic"   # 动态主页。如果找不到视频，则打开默认的动态主页
countCompare = 5    # 比较最后5个视频

def open_bilibili_video(bvid, pattern, urlDynamic, countCompare):
    try:
        # 合集的链接
        url = 'https://api.bilibili.com/x/web-interface/view?bvid=' + bvid
        headers = {
            "priority" : "u=0, i",
            "user-agent" :"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
        }

        # 处理响应结果
        resp = requests.get(url, headers=headers)
        data = resp.json()
        code = data['code']
        bvid = data['data']['bvid']
        ugc_season = data['data']['ugc_season']
        title = ugc_season["title"]
        sections = ugc_season["sections"]
        episodes = sections[0]['episodes']
        episodesLen = len(episodes) # 合集内视频数量
        
        # 匹配算法：将日期转成小数，进行比较，取到最新一期视频，若有多个最新期视频，则取其中的第一个。
        # 只看最后countCompare个
        flagMatch = 0   # 用于判断是否有匹配到的视频，0为未匹配到，1为匹配到
        last_number = 0 # 用于存储最后一个匹配到的视频的日期
        bvid = 0        # 用于存储匹配到的视频的bvid
        # 使用range()，从 episodesLen - 1（最后一个） 到 episodesLen - 7（倒数第五个） 倒序遍历 episodes 列表
        for i in range(episodesLen -1, episodesLen - 2 - countCompare, -1):
            # tilte处理
            title = episodes[i]['title']
            match = re.search(pattern, title)
            if match:
                current_number = float(match.group(1))   # match.group() 则包含所有pattern
                flagMatch = 1
            else:
                current_number = 0
            # 取最前面的最大的
            if current_number >= last_number:
                last_number = current_number
                bvid = episodes[i]['bvid']
            # print(title, bvid)

        if flagMatch:
            print("【+】 正在打开最新一期视频，请稍等...")
            # 打开指定的视频 https://www.bilibili.com/video/ + bvid
            url = "https://www.bilibili.com/video/" + bvid  # 指定要打开的URL
            webbrowser.open(url)    # 使用默认浏览器打开
        else:
            print("【+】 未找到匹配视频，正在打开默认动态主页，请稍等...")
            webbrowser.open(urlDynamic)    # 使用默认浏览器打开动态主页
    except:
        print("【+】 算法处理出错，正在打开默认动态主页，请稍等...")
        webbrowser.open(urlDynamic)    # 使用默认浏览器打开动态主页

if __name__ == "__main__":
    open_bilibili_video(bvid, pattern, urlDynamic, countCompare)