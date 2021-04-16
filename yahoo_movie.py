import requests
from bs4 import BeautifulSoup
import math
from datetime import datetime


class YahooMovie:
    """
    Yahoo 上映中電影相關資訊

    Attributes
    ----------
    self.movies : list of dict
        [{
            'title': str,
            'link': str of hyperlink,
            'picture': str of hyperlink,
            'release': str of YYYY-MM-DD,
            'content': str,
            'expectation': str of XX%,
            'satisfaction': str of float
         },
         ...
        ]
    """
    def __init__(self, get_all_movies_or_num_of_movies=False):
        """

        Parameters
        ----------
        get_all_movies_or_num_of_movies : int or bool
            抓取上映中的電影資訊，
            如果是 int 則初始化時自動抓取對應筆數的電影，
            大於目前官網上映中筆數，將只回傳官網上映中最大筆數 (可透過 self.get_movies(int) 再次抓取)
            如果是 True 則自動抓取目前所有上映中電影
        """
        if get_all_movies_or_num_of_movies is True:
            num_of_movies = YahooMovie._get_total_num()
        elif isinstance(get_all_movies_or_num_of_movies, int):
            num_of_movies = min(get_all_movies_or_num_of_movies, YahooMovie._get_total_num())
        else:
            num_of_movies = 10

        self.movies = self.get_movies(num_of_movies)

    # TODO: thread or multiprocessing
    def get_movies(self, num_of_movies):
        """
        取得上映中的電影 (從第一頁第一筆開始)

        Parameters
        ----------
        num_of_movies: int
            要抓取電影的筆數

        Returns
        -------
        self.movies
        """
        pages = math.ceil(num_of_movies / 10)
        self.movies = [movie for i in range(1, pages + 1)
                       for movie in YahooMovie.get_one_page_movies(i)][:num_of_movies]

        return self.movies

    @staticmethod
    def _get_soup(page=1):
        """內部函數，取得網頁原始碼"""
        movie_url = f"https://movies.yahoo.com.tw/movie_intheaters.html?page={page}"  # 上映中
        response = requests.get(movie_url)
        response.encoding = 'utf8'
        return BeautifulSoup(response.text, "html.parser")

    @staticmethod
    def _get_total_num():
        """內部函數，取得目前上映中電影的數目"""
        soup = YahooMovie._get_soup(1)
        text = soup.find('div', class_="release_time _c").text
        toal_num = text[text.find('共') + 1:text.find('筆')]
        return int(toal_num)

    @staticmethod
    def get_one_page_movies(page: int):
        """取得單一頁面的電影資訊(10筆)，靜態函數可提供外部直接調用"""
        soup = YahooMovie._get_soup(page)

        all_movie = soup.find_all('div', class_="release_info")
        all_movie_picture = soup.find_all('div', class_='release_box')[0].find_all('img')

        movies = []
        for i, movie in enumerate(all_movie):
            movies.append(
                {
                    'title': movie.find('a', class_="gabtn").text.split(' ')[-1],
                    'link': movie.find('a', class_="gabtn")['href'],
                    'picture': all_movie_picture[i]['src'],
                    'release': movie.find('div', class_="release_movie_time").text.split(' ： ')[-1],
                    'content': movie.find('span', class_="jq_text_overflow_180 jq_text_overflow_href_list").text,
                    'expectation': movie.find('div', class_='leveltext').text.replace(' ', '').split('\n')[1],
                    'satisfaction': movie.find('span', class_='count')['data-num']
                }
            )
        return movies

    @staticmethod
    def get_movies_rank(choose='台北票房榜'):
        """
        特殊榜單，提供外部直接調用

        Parameters
        ----------
        choose : {'台北票房榜', '全美票房榜', '預告片榜'}

        Returns
        -------
        ranks_of_movies_list : [dict, ...]
            [{
                'title': str,
                'link': str of hyperlink
             },
             ...
            ]

        """
        soup = YahooMovie._get_soup(1)

        # [台北票房榜, 全美票房榜, 預告片榜]
        ranks_of_movies = soup.find_all('ul', class_="ranking_list_r")

        if choose == '台北票房榜':
            i = 0
        elif choose == '全美票房榜':
            i = 1
        elif choose == '預告片榜':
            i = 2
        else:
            raise Exception(f"暫無提供 {choose} 榜單喔~")

        ranks_of_movies_list = []
        for item in ranks_of_movies[i].find_all('a', class_="gabtn"):  # 有英文時會漏抓
            ranks_of_movies_list.append(
                {
                    'title': item['data-ga'].split("'")[-2],  # item.text.replace('\n')
                    'link': item['href']
                }
            )
        return ranks_of_movies_list

    def sorted_movies(self, values='expectation', reverse=True):
        """
        根據網友期待度或是滿意度回傳新的電影排序
        不會變更 self.movies 的排序

        Parameters
        ----------
        values : {'expectation', 'satisfaction', 'release'}
        reverse : bool, default=True
            False 代表數值由小到大
            True 代表數值由大到小

        Returns
        -------
        根據要求的 key 值排序後的 self.movies.copy()
        """
        if values == 'expectation':
            return sorted(self.movies, key=lambda d: float(d['expectation'].strip("%")), reverse=reverse)
        elif values == 'satisfaction':
            return sorted(self.movies, key=lambda d: float(d['satisfaction']), reverse=reverse)
        elif values == 'release':
            return sorted(self.movies, key=lambda d: datetime.strptime(d['release'], "%Y-%m-%d"), reverse=reverse)
        else:
            raise Exception(f"目前還沒推出 {values} 排序功能唷~")


if __name__ == '__main__':
    """初始化方式"""
    # initial
    ym = YahooMovie()
    top_30_online_movies = ym.get_movies(True)
    print(ym._get_total_num())
    # [台北票房榜, 全美票房榜, 預告片榜]
    taipei_top_10 = ym.get_movies_rank('台北票房榜')
    usa_top_10 = ym.get_movies_rank('全美票房榜')  # 全美票房榜 英文的電影沒有超連結 目前是去除的 所以會少於10
    trailer_top_10 = ym.get_movies_rank('預告片榜')

    # 根據網友期待度由大到小排序
    movies_sort_by_expectation = ym.sorted_movies('expectation')
    # 根據網友綜合評分由大到小排序
    movies_sort_by_satisfaction = ym.sorted_movies('satisfaction')
    # 根據上映日期由新到舊排序
    movies_sort_by_release = ym.sorted_movies('release')

    """其他特殊用法"""
    YahooMovie._get_total_num()  # 取得目前上映中電影的筆數
    YahooMovie.get_movies_rank()  # 直接取得排行榜
    YahooMovie.get_one_page_movies(7)  # 直接取得第七頁的電影資訊
