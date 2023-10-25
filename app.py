# ---------------------------------- Modules ----------------------------------
import os 
from flask import Flask, request, abort
from linebot.v3.webhook import WebhookHandler
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    MessagingApiBlob,
    ReplyMessageRequest,
)
from linebot.v3.webhooks import (
    MessageEvent,
    PostbackEvent,
    TextMessageContent,
    ImageMessageContent,
    AudioMessageContent,
)
from message_handler.text_analysis import text_analysis
from message_handler.postback_analysis import postback_analysis
from message_handler.image_analysis import image_analysis
from message_handler.audio_analysis import audio_analysis

# ---------------------------------- App init ----------------------------------
# Flask app
app = Flask(__name__)
app.config.from_object('config.development.DevelopmentConfig')

CHANNEL_ACCESS_TOKEN = os.environ.get('CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.environ.get('CHANNEL_SECRET')

configuration = Configuration(access_token = CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(channel_secret = CHANNEL_SECRET)

# ---------------------------------- Routers ----------------------------------
@app.route("/", methods=['GET', 'POST'])
def HealthCheck():
    return "Success!"

@app.route('/callback', methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# ---------------------------------- Message Handler ----------------------------------
@handler.add(MessageEvent, message=TextMessageContent)
def handle_text(event):
    print("Text Process")
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        reply_list = text_analysis(event, line_bot_api) 
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[reply_list]
            )
        )

@handler.add(PostbackEvent)
def handle_postback(event):
    print("Postback Process")
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        reply_list = postback_analysis(event, line_bot_api) 
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[reply_list]
            )
        )
    
    
@handler.add(MessageEvent, message= ImageMessageContent)
def handle_image(event):
    print("Image Process")
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api_blob = MessagingApiBlob(api_client)
        reply_list = image_analysis(event, line_bot_api, line_bot_api_blob) 
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[reply_list]
            )
        )

@handler.add(MessageEvent, message= AudioMessageContent)
def handle_image(event):
    print("Audio Process")
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api_blob = MessagingApiBlob(api_client)
        reply_list = audio_analysis(event, line_bot_api, line_bot_api_blob) 
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=list(reply_list)
            )
        )

# ==============================================================================
if __name__ == "__main__":
    app.run(port=5001,debug=False)