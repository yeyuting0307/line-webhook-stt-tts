import os
from typing import List
from vertexai.preview.language_models import ChatModel, InputOutputTextPair

def palm2_chat(question:str, chat_examples : List[InputOutputTextPair] = None) -> str:
    '''Use PaLM2 to chat with user.
    chat_examples: [
             InputOutputTextPair(
                 input_text="How many moons does Mars have?",
                 output_text="The planet Mars has two moons, Phobos and Deimos.",
             ),
         ],
    '''
    chat_model = ChatModel.from_pretrained(os.environ.get("PALM2_CHAT_MODEL", "chat-bison"))

    # override these parameters as needed:
    parameters = {
        "temperature": float(os.environ.get("PALM2_TEMPERATURE", 0.2)),  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": int(os.environ.get("PALM2_MAX_OUTPUT_TOKENS", 256)),  # Token limit determines the maximum amount of text output.
        "top_p": float(os.environ.get("PALM2_TOP_P", 0.95)),  # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
        "top_k": int(os.environ.get("PALM2_TOP_K", 40)),  # A top_k of 1 means the selected token is the most probable among all tokens.
    }

    chat = chat_model.start_chat(
        context=os.environ.get("PALM2_START_CHAT_CONTEXT", "You are an voice customer service, reply answers as short as possible."),
        examples= chat_examples
    )

    response = chat.send_message(
        question , **parameters
    )
    print(f"Response from PaLM : {response.text}")
    return response.text
