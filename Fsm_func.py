from linebot.models import *
from linebot import LineBotApi
from imgurpython import ImgurClient
import requests
from bs4 import BeautifulSoup
import os
import json
from yahoo_movie import YahooMovie


line_bot_api = LineBotApi('5MhOpkx5/bFYcWmWJtqUUl8eAe52v2S1JFeEbjEiIiB75gGxoyIwhanq4fe/X1Do6ZyIdMiuDsdunHb8mcdwqzZTKDKSy9WQBfYdiF11xnePkZ/Yh+x8wemlSQLYP3HdCPcTbPiyan6j1fOl9fxWlgdB04t89/1O/w1cDnyilFU=')


def push_textmsg(event,text):
    line_bot_api.push_message(event.source.user_id, TextSendMessage(text = text))
    return True
def push_templatemsg(event,template):
    line_bot_api.push_message(event.source.user_id,template)
    return True
def main_menu_enter(event):
    flex_msg = json.load(open('menu.json','r',encoding = 'utf-8'))
    line_bot_api.push_message(event.source.user_id,FlexSendMessage('Menu',flex_msg))

def movie_lobby_enter(event):
    flex_msg = json.load(open('movie_lobby.json','r',encoding = 'utf-8'))
    line_bot_api.push_message(event.source.user_id,FlexSendMessage('Movie Lobby',flex_msg))

def movie_list_enter(event):
    YH = YahooMovie()
    total_movies = YH._get_total_num()
    data = YH.get_movies(total_movies)
    quo = total_movies // 10
    rem = total_movies % 10
    index = 0
    while quo > 0:
        page_arr = []
        movie_list = {
            "type": "carousel",
            "contents": page_arr
        }
        for i in range(0,10):
            page = json.load(open('movie_list_page.json','r+',encoding = 'utf-8'))
            page['hero']['url'] = data[index]['picture']
            page['body']['contents'][0]['text'] = data[index]['title']
            page['body']['contents'][2]['text'] = data[index]['content']
            page['body']['contents'][2]['wrap'] = True
            page['body']['contents'][3]['action']['uri'] = data[index]['link']
            page_arr.append(page)
            index += 1
        line_bot_api.push_message(event.source.user_id, FlexSendMessage('Movie List',movie_list))
        quo -= 1
    for i in range(0,rem):
        page_arr = []
        movie_list = {
            "type": "carousel",
            "contents": page_arr
        }
        page = json.load(open('movie_list_page.json','r+',encoding = 'utf-8'))
        page['hero']['url'] = data[index]['picture']
        page['body']['contents'][0]['text'] = data[index]['title']
        page['body']['contents'][2]['text'] = data[index]['content']
        page['body']['contents'][2]['wrap'] = True
        page['body']['contents'][3]['action']['uri'] = data[index]['link']
        page_arr.append(page)
        index += 1
    line_bot_api.push_message(event.source.user_id, FlexSendMessage('Movie List',movie_list))

   
    
    
    



