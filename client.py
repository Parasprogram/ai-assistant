from openai import OpenAI 
client = OpenAI(
   api_key="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" 
)
completion = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role":"system","contant":"you are the virtual assistant jarvis skilled in general task like alexa and google"},
        {"role":"user","contant":"what is the code"}
    ]
)   

print(completion.output[0].message)