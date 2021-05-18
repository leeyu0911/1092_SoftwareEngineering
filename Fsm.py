from transitions.extensions import GraphMachine
from Fsm_func import *

machine = {}
favorite_state = {}

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

#Initial Menu conditions
    def is_going_to_main_menu(self, event):
        text = event.message.text
        return text.lower() == "back to menu"

    def on_enter_main_menu(self, event):
        main_menu_enter(event)

# Movie Lobby conditions
    def is_going_to_movie_lobby(self, event):
        text = event.message.text
        return text.lower() == 'movie lobby'

    def on_enter_movie_lobby(self, event):
        movie_lobby_enter(event)

# Movie List conditions   
    def is_going_to_movie_list(self,event):
        text = event.message.text
        return text.lower() == 'movie list'

    def on_enter_movie_list(self,event):
        show_movie_list(event)
        self.go_back_movie_lobby(event)

# New Movie conditions
    def is_going_to_new_movie(self, event):
        text = event.message.text
        return text.lower() == "new movies"

    def on_enter_new_movie(self, event):
        show_new_movie(event)
        self.go_back_movie_lobby(event)

# Hot Movie conditions
    def is_going_to_hot_movie(self, event):
        text = event.message.text
        return text.lower() == "hot movies"

    def on_enter_hot_movie(self, event):
        show_hot_movie(event)
        self.go_back_movie_lobby(event)

# Movie LeaderBoard conditions
    def is_going_to_movie_leaderboard(self, event):
        text = event.message.text
        return text.lower() == "movie leaderboard"
    def on_enter_movie_leaderboard(self, event):
        movie_leaderboard_enter(event)
    def go_back_to_movie_lobby(self,event):
        text = event.message.text
        return text.lower() == "back to movie lobby"
    def is_going_to_trailer_rank(self,event):
        text = event.message.text
        return text.lower() == "trailer rank"
    def is_going_to_taipei_rank(self,event):
        text = event.message.text
        return text.lower() == "taipei box office"
    def is_going_to_us_rank(self,event):
        text = event.message.text
        return text.lower() == "us rank"
    def on_enter_trailer_rank(self,event):
        show_trailer_rank(event)
        self.go_back_movie_leaderboard(event)
    def on_enter_taipei_rank(self,event):
        show_taipei_rank(event)
        self.go_back_movie_leaderboard(event)
    def on_enter_us_rank(self,event):
        show_us_rank(event)
        self.go_back_movie_leaderboard(event)

