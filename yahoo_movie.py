import requests
from bs4 import BeautifulSoup
import math


class yahoo_movie:
    def __init__(self, num_of_movies: int):

        if not isinstance(num_of_movies, int) or num_of_movies <= 0:
            raise Exception("請輸入大於0的整數！")

        self.pages = math.ceil(num_of_movies / 10)
        self.movies = [movie for i in range(1, self.pages + 1)
                       for movie in yahoo_movie.get_one_page_movies(i)][:num_of_movies]

    @staticmethod
    def get_one_page_movies(page: int):
        movie_url = f"https://movies.yahoo.com.tw/movie_intheaters.html?page={page}"
        response = requests.get(movie_url)
        response.encoding = 'utf8'
        soup = BeautifulSoup(response.text, "html.parser")

        all_movie = soup.find_all('div', class_="release_info")
        all_movie_picture = soup.find_all('div', class_='release_box')[0].find_all('img')

        movies = []
        for i, movie in enumerate(all_movie):
            movies.append(
                {
                    'title': movie.find('a', class_="gabtn").text.split(' ')[-1],
                    'link': movie.find('a', class_="gabtn")['href'],
                    'picture': all_movie_picture[i]['src'],
                    'release': movie.find('div', class_="release_movie_time").text,
                    'content': movie.find('span', class_="jq_text_overflow_180 jq_text_overflow_href_list").text,
                    'expectation': movie.find('div', class_='leveltext').text.replace(' ', '').split('\n')[1],
                    'satisfaction': movie.find('span', class_='count')['data-num']
                }
            )
        return movies


if __name__ == '__main__':
    movies = yahoo_movie(30)  # 抓前30筆上映中的電影資訊
    print(movies.movies)



