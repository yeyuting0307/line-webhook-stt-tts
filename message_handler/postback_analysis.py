import json
from linebot.v3.messaging import TextMessage

# TODO: Not Test Yet
def postback_analysis(event, line_bot_api):
    postback_data = event.postback.data
    return TextMessage(text = f"postback data: {postback_data}")
