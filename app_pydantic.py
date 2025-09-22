from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from typing import List
from dotenv import load_dotenv
load_dotenv()
class CryptoCurrencySummary(BaseModel):
    name: str
    high: float
    low: float

class Summary(BaseModel):
    date: str = Field(description="date of yesterday with the format YYYY-MM-DD")
    crypto_currencies: List[CryptoCurrencySummary] = Field(description="list of 10 best cryptocurrencies summary of yesterday")

parser = PydanticOutputParser(pydantic_object=Summary)

prompt_template = """
        You're an expert about cryptocurrency.
        Your role is to extract yesterday's high and low about the 10 best cryptocurrencies.
        The date format should be in the format YYYY-MM-DD
                                
        {format_instructions}
    """

prompt = PromptTemplate(
    template=prompt_template,
    input_variables=[],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | ChatOpenAI(temperature=0.1, model="gpt-4-1106-preview")
json = chain.invoke({})

print(json.content)