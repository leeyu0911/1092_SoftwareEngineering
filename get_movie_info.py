import requests
from bs4 import BeautifulSoup


page = 1
movie_url = f"https://movies.yahoo.com.tw/movie_intheaters.html?page={page}"

response = requests.get(movie_url)
response.encoding = 'utf8'
soup = BeautifulSoup(response.text, "html.parser")

#%% datatype: bs4.element.ResultSet
all_movie = soup.find_all('div', class_="release_info")
# all_content = soup.find_all('span', class_="jq_text_overflow_180 jq_text_overflow_href_list")
# all_arive_date = soup.find_all('div', class_="release_movie_time")
all_movie_picture = soup.find_all('div', class_='release_box')[0].find_all('img')

#%% datatype: ['str', ...]
movie_title = []         # 電影名稱
movie_link = []          # 電影連結
movie_picture = []       # 電影海報
movie_release = []       # 上映日期
movie_content = []       # 劇情介紹
movie_expectation = []   # 網友期待度
movie_satisfaction = []  # 綜合平分 滿意度

for movie in all_movie:
    movie_title.append(movie.find('a', class_="gabtn").text.split(' ')[-1])
    movie_link.append(movie.find('a', class_="gabtn")['href'])
    movie_release.append(movie.find('div', class_="release_movie_time").text)
    movie_content.append(movie.find('span', class_="jq_text_overflow_180 jq_text_overflow_href_list").text)
    movie_expectation.append(movie.find('div', class_='leveltext').text.replace(' ', '').split('\n')[1])
    movie_satisfaction.append(movie.find('span', class_='count')['data-num'])

for pic in all_movie_picture:
    movie_picture.append(pic['src'])

#%% datatype: [json, ...]

movies = []
for i in range(len(all_movie)):
    movies.append(
        {
            'title': movie_title[i],
            'link': movie_link[i],
            'picture': movie_picture[i],
            'release': movie_release[i],
            'content': movie_content[i],
            'expectation': movie_expectation[i],
            'satisfaction': movie_satisfaction[i]
        }
    )

