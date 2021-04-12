import requests
from bs4 import BeautifulSoup
import math


class yahoo_movie:
    def __init__(self, num_of_movies: int = 99):
        """
        :param num_of_movies: 抓前多少筆上映中的電影資訊，如果 num_of_movies 大於目前官網上映中筆數，將只回傳官網上映中最大筆數
        """

        if not isinstance(num_of_movies, int) or num_of_movies <= 0:
            raise Exception("請輸入大於0的整數！")

        self._pages = math.ceil(num_of_movies / 10)
        self.movies = [movie for i in range(1, self._pages + 1)
                       for movie in yahoo_movie.get_one_page_movies(i)][:num_of_movies]

    @staticmethod
    def get_one_page_movies(page: int):
        # 上映中
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

    def sort_movies(self, values='expectation', reverse=True):
        """
        根據網友期待度或是滿意度將電影做排序
        :param values: 'expectation' or 'satisfaction'
        :param reverse: False 代表數值由小到大
        :return: [json, ...]
        """
        if values == 'expectation':
            return sorted(self.movies, key=lambda d: float(d['expectation'].strip("%")), reverse=reverse)
        elif values == 'satisfaction':
            return sorted(self.movies, key=lambda d: float(d['satisfaction']), reverse=reverse)
        else:
            raise Exception(f"目前還沒推出 {values} 排序功能唷~")


if __name__ == '__main__':
    # 抓前30筆上映中的電影資訊
    movies_of_30 = yahoo_movie(30)
    print(movies_of_30.movies)

    # 抓取所有上映中電影
    all_movies = yahoo_movie()
    # 根據網友期待度由大到小排序
    movies_sort_by_expectation = all_movies.sort_movies()
    # 根據網友綜合平分由大到小排序
    movies_sort_by_satisfaction = all_movies.sort_movies(values='satisfaction')
