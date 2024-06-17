from google.colab import drive
drive.mount('/content/drive')
!pip install openai tiktoken session-info --quiet
# Import all Python packages required to access the Azure Open AI API
import openai
import json
import tiktoken
import session_info
session_info.show()
# Azure Open AI redentials and the id of the deployed chat model are stored as
# key value pairs in a json file

with open('/content/config.temp.json', 'r') as az_creds:
    data = az_creds.read()
    # Credentials to authenticate to the personalized Open AI model server
openai.api_key = creds["AZURE_OPENAI_KEY"]
openai.api_base = creds["AZURE_OPENAI_ENDPOINT"]
openai.api_type = creds["AZURE_OPENAI_APITYPE"]
openai.api_version = creds["AZURE_OPENAI_APIVERSION"]

# Deployment id of the ChatCompletion endpoint
chat_model_id = creds["tryinggptopenai"]
response = openai.ChatCompletion.create(
    deployment_id=chat_model_id,
    messages=[
        {"role": "system", "content": "You are a helpful ai assistant."},
        {"role": "user", "content": "Tell me about history of settlement in  Nigeria?"},
        #{"role": "assistant", "content": "Yes, at the moment there is restricted access to mult-modal inputs (e.g., text + images)."},
        #{"role": "user", "content": "What else does the Azure Open AI service support?"}
    ]
)
def num_tokens_from_messages(messages):

    """
    Return the number of tokens used by a list of messages.
    Adapted from the Open AI cookbook token counter
    """

    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

    # Each message is sandwiched with <|start|>role and <|end|>
    # Hence, messages look like: <|start|>system or user or assistant{message}<|end|>

    tokens_per_message = 3 # token1:<|start|>, token2:system(or user or assistant), token3:<|end|>

    num_tokens = 0

    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))

    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>

    return num_tokens
prompt = [
    {"role": "system", "content": "You are a helpful ai assistant."},
    {"role": "user", "content": "Tell me the history of Nigeria?"},
    #{"role": "assistant", "content": "Yes, at the moment there is restricted access to mult-modal inputs (e.g., text + images)."},
    #{"role": "user", "content": "What else does the Azure Open AI service support?"}
]
def get_completion(prompt, chat_model_id, max_tokens=10, temperature=0.9):

    completion_messages = [{"role": "user", "content": prompt}]

    # compute number of prompt tokens before presenting it to the API
    num_prompt_tokens = num_tokens_from_messages(completion_messages)

    print(f"Number of tokens in prompt: {num_prompt_tokens}\n")

    response = openai.ChatCompletion.create(
        deployment_id=chat_model_id,
        messages=completion_messages,
        max_tokens=max_tokens,
        temperature=temperature
    )

    # read the number of completion tokens from the response
    num_completion_tokens = response["usage"]["completion_tokens"]

    print(f"Number of tokens in completion: {num_completion_tokens}\n")

    return response.choices[0].message["content"]
prompt =
"""You are a marketer for the gaming company Razer.
Below is the metadata about the Razer Ornata V3 X gaming keyboard:
Brand: Razer
Series: Ornata V3 X
Item model number: RZ03-04470200-R3U1
Hardware Platform: PC
Operating System: Microsoft Windows
Item Weight: 2.97 pounds
Product Dimensions: 17.46 x 5.68 x 1.23 inches
Item Dimensions LxWxH: 17.46 x 5.68 x 1.23 inches
Color: Classic Black
Manufacturer: Razer
Language: English
ASIN: B09X6GJ691
Special Features: Low-Profile Keys, Spill Resistant, Ergonomic Wrist Rest, Chroma RGB Lighting, Silent Membrane Switches, Cable Routing Options
With this information, write a sleek "About this item" description that will be used on its Amazon product page.
Use bullet points to delineate key features mentioned in the description.
"""