import openai

openai.api_key = "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"

def judge_client(prompt) -> str:

     # Get response from text-davinci-003
     response =  openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
     responseText = response.choices[0].text

     return responseText


