from transitions.extensions import GraphMachine
from Fsm_func import *

machine = {}
favorite_state = {}

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_main_menu(self, event):
        text = event.message.text
        return text.lower() == "back to menu"

    def on_enter_main_menu(self, event):
        main_menu_enter(event)

    def is_going_to_movie_lobby(self, event):
        text = event.message.text
        return text.lower() == 'movie lobby'

    def is_going_to_movie_lobby_postback(self, event):
        text = event.postback.data
        return text.lower() == "back to movie lobby"

    def on_enter_movie_lobby(self, event):
        movie_lobby_enter(event)
    
    def is_going_to_movie_list(self,event):
        text = event.message.text
        return text.lower() == 'movie list'

    def on_enter_movie_list(self,event):
        movie_list_enter(event)
        self.go_back_movie_lobby(event)
    
    def is_going_to_new_movie(self, event):
        text = event.message.text
        return text.lower() == "new movies"

    def on_enter_new_movie(self, event):
        text = 'Enter new_movie state'
        push_textmsg(event, text)
        self.go_back_movie_lobby(event)

    def is_going_to_movie_leaderboard(self, event):
        text = event.message.text
        return text.lower() == "movie leaderboard"

    def on_enter_movie_leaderboard(self, event):
        text = 'Enter leaderboard state'
        push_textmsg(event, text)
        self.go_back_movie_lobby(event)

    def is_going_to_hot_movie(self, event):
        text = event.message.text
        return text.lower() == "hot movies"

    def on_enter_hot_movie(self, event):
        text = 'Enter hot_movie state'
        push_textmsg(event, text)
        self.go_back_movie_lobby(event)

    def is_going_to_movie_news(self, event):
        text = event.message.text
        return text.lower() == "movie news"

    def on_enter_movie_news(self, event):
        text = 'Enter movie_news state'
        push_textmsg(event, text)
        self.go_back_movie_lobby(event)

    def is_going_to_search_movie(self, event):
        text = event.message.text
        return text.lower() == "search movie"

    def on_enter_search_movie(self, event):
        text = 'Enter search_movie state'
        push_textmsg(event, text)

    def on_enter_do_search_movie(self, event):
        text = 'Enter do_search_movie state'
        push_textmsg(event, text)
        self.go_back_movie_lobby(event)