from linebot.models import *
from linebot import LineBotApi
from imgurpython import ImgurClient
import requests
from bs4 import BeautifulSoup
import os
import json
from yahoo_movie import YahooMovie


line_bot_api = LineBotApi('5MhOpkx5/bFYcWmWJtqUUl8eAe52v2S1JFeEbjEiIiB75gGxoyIwhanq4fe/X1Do6ZyIdMiuDsdunHb8mcdwqzZTKDKSy9WQBfYdiF11xnePkZ/Yh+x8wemlSQLYP3HdCPcTbPiyan6j1fOl9fxWlgdB04t89/1O/w1cDnyilFU=')

# default Function
def push_textmsg(event,text):
    line_bot_api.push_message(event.source.user_id, TextSendMessage(text = text))
    return True
def push_templatemsg(event,template):
    line_bot_api.push_message(event.source.user_id,template)
    return True

# Menu enter Function    
def main_menu_enter(event):
    flex_msg = json.load(open('menu.json','r',encoding = 'utf-8'))
    line_bot_api.push_message(event.source.user_id,FlexSendMessage('Menu',flex_msg))

# Movie Lobby enter Function
def movie_lobby_enter(event):
    flex_msg = json.load(open('movie_lobby.json','r',encoding = 'utf-8'))
    line_bot_api.push_message(event.source.user_id,FlexSendMessage('Movie Lobby',flex_msg))

# Movie List Function
def show_movie_list(event):
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

# Movie Leaderboard Functions
def movie_leaderboard_enter(event):
    flex_msg = json.load(open('leaderboard.json','r',encoding = 'utf-8'))
    line_bot_api.push_message(event.source.user_id,FlexSendMessage('Movie LeaderBoard',flex_msg))
def show_taipei_rank(event):
    ym = YahooMovie()
    taipei_top_10 = ym.get_movies_rank('台北票房榜')
    total_movies = ym.get_total_num()
    all_mov = ym.get_movies(total_movies)
    page = []
    rank_num = 1
    top_list = {
            "type": "carousel",
            "contents": page
        }
    for mov in taipei_top_10:
        flex_msg = json.load(open('rank_page.json','r',encoding = 'utf-8'))
        flex_msg['body']['contents'][0]['url'] =  mov['photo']
        flex_msg['body']['contents'][1]['contents'][0]['contents'][0]['text'] = mov['title']
        flex_msg['body']['contents'][1]['contents'][1]['contents'][0]['action']['uri'] = mov['link']
        flex_msg['body']['contents'][2]['contents'][0]['text'] = 'Rank '+str(rank_num)
        page.append(flex_msg)
        rank_num += 1
    line_bot_api.push_message(event.source.user_id,FlexSendMessage('Taipei Rank',top_list))
def show_us_rank(event):
    ym = YahooMovie()
    taipei_top_10 = ym.get_movies_rank('全美票房榜')
    total_movies = ym.get_total_num()
    all_mov = ym.get_movies(total_movies)
    page = []
    rank_num = 1
    top_list = {
            "type": "carousel",
            "contents": page
        }
    for mov in taipei_top_10:
        flex_msg = json.load(open('rank_page.json','r',encoding = 'utf-8'))
        flex_msg['body']['contents'][0]['url'] =  mov['photo']
        flex_msg['body']['contents'][1]['contents'][0]['contents'][0]['text'] = mov['title']
        flex_msg['body']['contents'][1]['contents'][1]['contents'][0]['action']['uri'] = mov['link']
        flex_msg['body']['contents'][2]['contents'][0]['text'] = 'Rank '+str(rank_num)
        page.append(flex_msg)
        rank_num += 1
    line_bot_api.push_message(event.source.user_id,FlexSendMessage('Us Rank',top_list))
def show_trailer_rank(event):
    ym = YahooMovie()
    taipei_top_10 = ym.get_movies_rank('預告片榜')
    total_movies = ym.get_total_num()
    all_mov = ym.get_movies(total_movies)
    page = []
    rank_num = 1
    top_list = {
            "type": "carousel",
            "contents": page
        }
    for mov in taipei_top_10:
        flex_msg = json.load(open('rank_page.json','r',encoding = 'utf-8'))
        flex_msg['body']['contents'][0]['url'] =  mov['photo']
        flex_msg['body']['contents'][1]['contents'][0]['contents'][0]['text'] = mov['title']
        flex_msg['body']['contents'][1]['contents'][1]['contents'][0]['action']['uri'] = mov['link']
        flex_msg['body']['contents'][2]['contents'][0]['text'] = 'Rank '+str(rank_num)
        page.append(flex_msg)
        rank_num += 1
    line_bot_api.push_message(event.source.user_id,FlexSendMessage('Trailer Rank',top_list))

def match_mov_name(mov_name,all_mov):
    ret = "https://i.imgur.com/p97kdN3.png"
    for mov in all_mov:
        if(mov['title'][:len(mov_name)] == mov_name):
            ret = mov['picture']
            break
        if(mov['title'] == mov_name[:len(mov['title'])]):
            ret = mov['picture']
            break
    return ret
 
# Hot Movies Function
def show_hot_movie(event):
    ym = YahooMovie(True)
    data = ym.sorted_movies('satisfaction')
    page_arr = []
    top_list = {
            "type": "carousel",
            "contents": page_arr
        }
    index = 0
    for i in range(0,10):
            page = json.load(open('movie_list_page.json','r+',encoding = 'utf-8'))
            page['hero']['url'] = data[index]['picture']
            page['body']['contents'][0]['text'] = data[index]['title']
            page['body']['contents'][2]['text'] = data[index]['content']
            page['body']['contents'][2]['wrap'] = True
            page['body']['contents'][3]['action']['uri'] = data[index]['link']
            page_arr.append(page)
            index += 1
    line_bot_api.push_message(event.source.user_id,FlexSendMessage('Hot movies',top_list))

# New Movies Function
def show_new_movie(event):
    ym = YahooMovie(True)
    data = ym.sorted_movies('release')
    page_arr = []
    top_list = {
            "type": "carousel",
            "contents": page_arr
        }
    index = 0
    for i in range(0,10):
            page = json.load(open('movie_list_page.json','r+',encoding = 'utf-8'))
            page['hero']['url'] = data[index]['picture']
            page['body']['contents'][0]['text'] = data[index]['title']
            page['body']['contents'][2]['text'] = data[index]['content']
            page['body']['contents'][2]['wrap'] = True
            page['body']['contents'][3]['action']['uri'] = data[index]['link']
            page_arr.append(page)
            index += 1
    line_bot_api.push_message(event.source.user_id,FlexSendMessage('New movies',top_list))
