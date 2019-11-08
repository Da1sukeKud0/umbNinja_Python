# -*- coding: utf-8 -*-
# GitHub: https://github.com/Da1sukeKud0
from PIL import Image, ImageDraw, ImageFont
import io
import requests
from bs4 import BeautifulSoup
import re
import urllib
import time
import random

year = 2019
baseUrl = "http://ultimatemcbattle.com/2015/img/"

prefectureList = [
    "aichi", "ehime", "ibaraki", "okayama", "okinawa", "iwate", "gifu", "miyazaki", "miyagi", "kyoto", "kumamoto", "gunma", "hiroshima", "kagawa", "kochi", "saga", "saitama", "mie", "yamagata", "yamaguchi", "yamanashi", "shiga", "kagoshima", "akita", "niigata", "kanagawa", "aomori", "shizuoka", "ishikawa", "chiba", "osaka", "oita", "nagasaki", "nagano", "tottori", "shimane", "tokyo", "tokushima", "tochigi", "nara", "toyama", "fukui", "fukuoka", "fukushima", "hyogo", "hokkaido", "wakayama"
]

# フォントの設定
fontsize = 35
font = ImageFont.truetype("meiryob.ttc", size=fontsize) 

def scrape():
    """
    BeautifulSoupにより開催地区、優勝者、画像URLを取得
    """
    req = requests.get("http://ultimatemcbattle.com/2015/event/index2018.html")
    soup = BeautifulSoup(req.content, "html.parser")
    resultSet = soup.find_all('div', class_="main_waku_event")
    champDic = {} # {開催地区:優勝者}
    imgUrlDic = {} # {開催地区:画像のURL}
    for res in resultSet:
        # res.get_text()の内容をリストで取得し空文字要素を削除
        lines = [line.strip() for line in res.get_text().splitlines()]
        lines = [x for x in lines if x]

        if len(lines) >= 2 and 'チャンピオン' in lines[1]:
            # ～チャンピオンは、"*"に決定しました！ の*部分を抽出
            champion = re.search(r'".*"', lines[1]).group(0).strip('"')

            imgUrl = res.find('img')['src']
            
            # 開催地区を取得 ../img/index_*2018.jpg の*部分を抽出
            pre = imgUrl.strip("../img/index")[1:].split('20')[0]

            # 優勝者、画像URLを保存
            champDic[pre] = champion
            imgUrlDic[pre] = baseUrl + imgUrl[7:]
    return champDic,imgUrlDic

def getQuestionStr(prefecture):
    """
    フライヤーの画像URLを生成(一部不規則なものを含む)
    例) http://ultimatemcbattle.com/2015/img/okinawa2019_flyer.jpg
    """
    if prefecture == "kochi":
        return "http://ultimatemcbattle.com/2015/img/kouchi2019_flyer.jpg"
    elif prefecture == "kyoto":
        return "http://ultimatemcbattle.com/2015/img/UMB2019_%E4%BA%88%E9%81%B8_kyoto.jpg"
    elif prefecture == "wakayama":
        return "http://ultimatemcbattle.com/2015/img/UMB2019_%E4%BA%88%E9%81%B8_WAKAYAMA_A.jpg"
    elif (prefecture == "fukuoka"):
        prefecture = "fukuokatenjin"
    return baseUrl + prefecture + str(year) + "_flyer.jpg"


# def __getAnswerImgUrl(prefecture):
#     """
#     優勝者の画像URLを生成(汎用パターンをもとにREQUEST)
#     例) http://ultimatemcbattle.com/2015/img/index_okinawa2018a.jpg
#     """
#     answerUrlPattern = ['a','','b','c','A','_a']
#     for pat in answerUrlPattern:
#         try:
#             url = baseUrl + "index_" + prefecture + str(year-1) + pat +".jpg"
#             urllib.request.urlopen(url) # 画像URLの確認
#         except urllib.error.HTTPError:
#             print('answerUrlPattern is failed')
#             continue
#         else:
#             print('success: ' + url)
#             return url
#     raise Exception


if __name__ == '__main__':
    champDic,imgUrlDic = scrape() # 各地区予選の優勝者を取得
    random.shuffle(prefectureList) # 開催地区リストの順番をシャッフル

    for pre in prefectureList:
        # 質問と解答の画像オブジェクトを生成
        question_img = io.BytesIO(
            urllib.request.urlopen(getQuestionStr(pre)).read())
        answerUrl = imgUrlDic[pre]
        answer_img = io.BytesIO(urllib.request.urlopen(answerUrl).read())


        # 画像を表示する
        with Image.open(question_img) as img:
            draw = ImageDraw.Draw(img)
            img.show()
            time.sleep(3)

        with Image.open(answer_img) as img:
            img = img.resize((int(img.width * 2), int(img.height * 2)))
            draw = ImageDraw.Draw(img)
            # 優勝者を画像に入力して表示
            champion = champDic[pre]
            draw.text((fontsize, int(img.height )- fontsize * 3), champion, font=font, fill=(255,255,0), stroke_width=1, stroke_fill=(255,0,0))
            img.show()
            time.sleep(3)
