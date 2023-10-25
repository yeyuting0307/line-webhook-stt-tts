import os
import tempfile
from util.gcp_storage import GcpStorage
from linebot.v3.messaging import TextMessage, ImageMessage

project = os.environ.get('GCP_PROJECT_ID')
bucket_name = os.environ.get('GCP_BUCKET_NAME')
gs = GcpStorage(project)

def image_analysis(event, line_bot_api, api_instance):
    # get image message
    user_id = event.source.user_id
    message_id = event.message.id
    img_bytes = api_instance.get_message_content(message_id)

    # save image to GCS
    tmp = tempfile.NamedTemporaryFile()
    gs_path = f"{bucket_name}/{user_id}/tmp_{message_id}.png"
    with tmp:
        tmp.write(img_bytes)
        gs.toStorage(remote_path = gs_path, local_path = tmp.name, make_public=True)

    # get image url
    img_url = f"https://storage.googleapis.com/{gs_path}"

    return ImageMessage(
        original_content_url = img_url,
        preview_image_url = img_url
    )