from openai import OpenAI
import os
from dotenv import load_dotenv

ex_prompt = """
SYSTEM

You are an expert Prompt Writer for Large Language Models.


Your goal is to improve the prompt given below for {task} :

--------------------

Prompt: {lazy_prompt}

--------------------

Here are several tips on writing great prompts:

-------

Start the prompt by stating that it is an expert in the subject.

Put instructions at the beginning of the prompt and use ### or to separate the instruction and context 

Be specific, descriptive and as detailed as possible about the desired context, outcome, length, format, style, etc 

---------

Here's an example of a great prompt:

As a master YouTube content creator, develop an engaging script that revolves around the theme of "Exploring Ancient Ruins."

Your script should encompass exciting discoveries, historical insights, and a sense of adventure.

Include a mix of on-screen narration, engaging visuals, and possibly interactions with co-hosts or experts.

The script should ideally result in a video of around 10-15 minutes, providing viewers with a captivating journey through the secrets of the past.

Example:

"Welcome back, fellow history enthusiasts, to our channel! Today, we embark on a thrilling expedition..."

-----

Now, improve the prompt.

IMPROVED PROMPT:

"""

#print(ex_prompt)
# print(ex_prompt.format(task="text generation", 
#                        lazy_prompt="Tell me about Muhammad Ali"))



# Load API Key stored in .env
load_dotenv()
# openai.api_key = os.environ['OPENAI_API_KEY']

# llm = "gpt-3.5-turbo-instruct"
# # llm = "gpt-4o"
# # llm = "gpt-3.5-turbo-16k"

# client = OpenAI()

# response = client.completions.create(
#     model=llm,
#     prompt=ex_prompt.format(task="text generation", 
#                        lazy_prompt="Tell me about Muhammad Ali"),
#     temperature=.5, 
# )

# response.choices[0].text
# #print(ex_prompt.format(task="text extraction", 
# #                       lazy_prompt="Tell me about Muhammad Ali"))

# print(response.choices[0].text)

import tiktoken
client = OpenAI()
def count_and_call(fn, max_limit=20, model=None, prompt=None):
    def newfn(model=model, prompt=prompt):
        encoding = tiktoken.encoding_for_model(model)
        print("Model name:", model)
        num_tokens = len(encoding.encode(prompt))
        print("Number of tokens", num_tokens)
        if num_tokens <= max_limit:
            return fn(model=model, prompt=prompt)
        else:
            raise Exception(f"Exceeded token limit. Reduce {num_tokens-max_limit} tokens.")
    return newfn

@count_and_call
def llm_call(model=None, prompt=None, max_limit=100, temperature=.5, n=50):
    result = client.completions.create(
                    prompt=prompt,
                    model=model,
                    temperature=temperature,
                    n=n)
    return result.choices[0].text
myprompt = "Tell me about Muhhammad Ali in 1 sentence"

llm_call(model="gpt-3.5-turbo-instruct", 
         prompt=myprompt)