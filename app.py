import os
import sys
from flask import Flask, jsonify, request, abort

from linebot import LineBotApi, WebhookHandler,WebhookParser
from linebot.exceptions import InvalidSignatureError

from linebot.models import *

from Fsm import TocMachine
from Fsm_data import FsmData


app = Flask(__name__)
user_machines = {} # record all user

# Channel Access Token
line_bot_api = LineBotApi('5MhOpkx5/bFYcWmWJtqUUl8eAe52v2S1JFeEbjEiIiB75gGxoyIwhanq4fe/X1Do6ZyIdMiuDsdunHb8mcdwqzZTKDKSy9WQBfYdiF11xnePkZ/Yh+x8wemlSQLYP3HdCPcTbPiyan6j1fOl9fxWlgdB04t89/1O/w1cDnyilFU=')
# Channel Secret
parser = WebhookParser('bf869b631079fa93fe7332c8a08c31f0')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    for event in events:
        if event.source.user_id not in user_machines:
            user_machines[event.source.user_id] = TocMachine(
                states=FsmData["states"],
                transitions=FsmData["transitions"],
                initial=FsmData["initial"],
                auto_transitions=FsmData["auto_transitions"],
                show_conditions=FsmData["show_conditions"]
                )
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        print(f"\nFSM Source: {user_machines[event.source.user_id].state}")
        print(f"REQUEST BODY: \n{body}")
        response = user_machines[event.source.user_id].advance(event)
        print(f"\nFSM Dest: {user_machines[event.source.user_id].state}")
        if response == False:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Not Entering any State"))
    return 'OK'

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
