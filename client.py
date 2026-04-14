import os
from openai import OpenAI

def main():
    api_key = os.getenv("OPENAI_API_KEY", "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")
    if not api_key:
        print("Assistant reply: API key not set. I am running in basic mode.")
        return

    try:
        client = OpenAI(api_key=api_key)
        completion = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": "you are the virtual assistant jarvis skilled in general task like alexa and google"},
                {"role": "user", "content": "what is the code"},
            ],
        )
        print(completion.choices[0].message.content)
    except Exception as e:
        print(f"Assistant reply: OpenAI service error: {e}")


if __name__ == "__main__":
    main()
