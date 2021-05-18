FsmData = {
    "states" : 
    [
        "init",
        "main_menu",
        "movie_lobby",
        "new_movie",
        "hot_movie",
        "movie_list",
        "movie_leaderboard",
        "taipei_rank",
        "us_rank",
        "trailer_rank"
    ],
    
    "transitions" : 
    [
        {
            "trigger":"advance",
            "source":"init",
            "dest":"main_menu",
        },
        {
            "trigger": "advance",
            "source": "main_menu",
            "dest": "movie_lobby",
            "conditions": "is_going_to_movie_lobby",
        },
        {
            "trigger": "advance",
            "source": "movie_lobby",
            "dest": "main_menu",
            "conditions": "is_going_to_main_menu",
        },
        {
            "trigger": "advance",
            "source": "movie_lobby",
            "dest": "new_movie",
            "conditions": "is_going_to_new_movie",
        },
        {
            "trigger": "advance",
            "source": "movie_lobby",
            "dest": "movie_leaderboard",
            "conditions": "is_going_to_movie_leaderboard",
        },
        {
            "trigger": "advance",
            "source": "movie_leaderboard",
            "dest": "movie_lobby",
            "conditions": "go_back_to_movie_lobby",
        },
        {
            "trigger": "advance",
            "source": "movie_leaderboard",
            "dest": "trailer_rank",
            "conditions": "is_going_to_trailer_rank",
        },
        {
            "trigger": "advance",
            "source": "movie_leaderboard",
            "dest": "taipei_rank",
            "conditions": "is_going_to_taipei_rank",
        },
        {
            "trigger": "advance",
            "source": "movie_leaderboard",
            "dest": "us_rank",
            "conditions": "is_going_to_us_rank",
        },
        # 無條件返回 movie leaderboard
        {
            "trigger": "go_back_movie_leaderboard",
            "source": ["trailer_rank","taipei_rank","us_rank"],
            "dest": "movie_leaderboard",
        },
        {
            "trigger": "advance",
            "source": "movie_lobby",
            "dest": "movie_list",
            "conditions": "is_going_to_movie_list",
        },
        {
            "trigger": "advance",
            "source": "movie_lobby",
            "dest": "hot_movie",
            "conditions": "is_going_to_hot_movie",
        },   
        # 無條件返回 movie_lobby
        {
            "trigger": "go_back_movie_lobby",
            "source": ["new_movie", "hot_movie","movie_list"],
            "dest": "movie_lobby",
        },
    ],
    "initial" : "init",
    "auto_transitions" : "False",
    "show_conditions" : "False",
}