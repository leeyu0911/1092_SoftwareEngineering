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
        "movie_news",
        "search_movie",
        "add_favorite",
        "my_favorite",
        "show_favorite",
        "leave_favorite",
        "delete_favorite",
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
            "source": "movie_lobby",
            "dest": "movie_list",
            "conditions": "is_going_to_movie_list",
        },
        {
            "trigger": "advance",
            "source": "movie_lobby",
            "dest": "movie_news",
            "conditions": "is_going_to_movie_news",
        },
        {
            "trigger": "advance",
            "source": "movie_lobby",
            "dest": "hot_movie",
            "conditions": "is_going_to_hot_movie",
        },
        {
            "trigger": "advance",
            "source": "movie_lobby",
            "dest": "search_movie",
            "conditions": "is_going_to_search_movie",
        },
        {
            "trigger": "advance",
            "source": "search_movie",
            "dest": "do_search_movie",
        },
        # 從search movie 到 movie_lobby
        {
            "trigger": "advance_postback",
            "source": "search_movie",
            "dest": "movie_lobby",
            "conditions": "is_going_to_movie_lobby_postback",
        },
        # 按下返回主選單
        {
            "trigger": "advance",
            "source": "movie_lobby",
            "dest": "main_menu",
            "conditions": "is_going_to_main_menu",
        },
        # 無條件返回 movie_lobby
        {
            "trigger": "go_back_movie_lobby",
            "source": ["new_movie", "hot_movie", "movie_leaderboard", "movie_news", "do_search_movie", "add_favorite", "leave_favorite","movie_list"],
            "dest": "movie_lobby",
        },
    ],
    "initial" : "init",
    "auto_transitions" : "False",
    "show_conditions" : "False",
}