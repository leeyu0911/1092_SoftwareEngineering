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
movie_title = []
movie_link = []
movie_picture = []
movie_release = []
movie_content = []
movie_expectation = []
movie_satisfaction = []

for movie in all_movie:
    movie_title.append(movie.find('a', class_="gabtn").text.split(' ')[-1])
    movie_link.append(movie.find('a', class_="gabtn")['href'])
    movie_release.append(movie.find('div', class_="release_movie_time").text)
    movie_content.append(movie.find('span', class_="jq_text_overflow_180 jq_text_overflow_href_list").text)
    movie_expectation.append(movie.find('div', class_='leveltext').text.replace(' ', '').split('\n')[1])
    movie_satisfaction.append(movie.find('span', class_='count')['data-num'])

for pic in all_movie_picture:
    movie_picture.append(pic['src'])
