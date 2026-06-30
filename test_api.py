from openai import OpenAI

client = OpenAI(
    api_key="sk-a1615d3c519a48ac8bd2ab7aa5f44dd7",
    base_url="https://api.deepseek.com"
)

messages = [
    {"role":"user","content":"初次相遇，很高兴认识你"}
]
response = client.chat.completions.create(
    model = "deepseek-chat",
    messages = messages
)
print(response.choices[0].message.content)