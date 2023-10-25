from linebot.v3.messaging import TextMessage, ImageMessage, FlexMessage
from linebot.v3.messaging.models.buttons_template import ButtonsTemplate
from linebot.v3.messaging.models.message_action import MessageAction
from linebot.v3.messaging.models.uri_action import URIAction
from linebot.v3.messaging.models.template_message import TemplateMessage
from linebot.v3.messaging.models.flex_message import FlexContainer

def text_analysis(event, line_bot_api):
    user_id = event.source.user_id

    profile = line_bot_api.get_profile(user_id)
    profile_json = profile.to_json()

    if event.message.text.lower() in ["uid", "userid", "user id"] :
        return TextMessage(text = f"{event.source.user_id}")
    
    elif event.message.text.lower() in ["userprofile", "user profile"] :
        user_id = event.source.user_id
        button_template_message =ButtonsTemplate(
            thumbnail_image_url=profile_json['pictureUrl'],
            title= profile_json['displayName'],
            text= '您的LINE用戶資訊',
            ratio="1.51:1",
            image_background_color = '#FF0000',
            image_size="cover",
            actions=[
                MessageAction(
                    label='查詢用戶UID', text="uid"
                ),
                URIAction(
                    label='用戶照片連結', uri=profile_json['pictureUrl']
                )
            ]
        )
        return TemplateMessage(
            alt_text="Check on the mobile phone",
            template=button_template_message
        )
    else:
        return TextMessage(text = f"{event.message.text}")

    