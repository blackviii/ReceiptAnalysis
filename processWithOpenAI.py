
from openai import OpenAI
import os


def process_string_with_openai(input_string):
    
    client = OpenAI()
    client.api_key=os.getenv("OPENAI_API_KEY")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "你会把小票里显示的购买物品的名称，价格罗列出来，每个物品为一行"},
            {"role": "user", "content": input_string}
        ]
    )

    formatted_result = response.choices[0].message
    return formatted_result
