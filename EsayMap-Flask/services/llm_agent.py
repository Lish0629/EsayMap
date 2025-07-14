import openai  # 或者换成 Qwen API

def call_llm(user_input):
    # 示例: 用 OpenAI 或 Qwen SDK 发请求
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_input}]
    )
    return response['choices'][0]['message']['content']
