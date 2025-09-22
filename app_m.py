from dotenv import load_dotenv
load_dotenv()

import langchain
from langchain_core.prompts import PromptTemplate



# template = """Question: {question}

# Answer: """

# prompt = PromptTemplate(
#             template=template,
#             input_variables=['question']
# )

# # user question
# question = "Where was 1996 Olympics held?"
# print(prompt.format(question=question))


from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Please respond to the user's request only based on the given context."),
    ("user", "Question: {question}\nContext: {context}")
])

model = ChatOpenAI(model="gpt-3.5-turbo")
output_parser = StrOutputParser()

chain = prompt | model | output_parser

question = "Can you summarize this morning's meetings?"
context = "During this morning's meeting, we solved all world conflict."
chain.invoke({"question": question, "context": context})






