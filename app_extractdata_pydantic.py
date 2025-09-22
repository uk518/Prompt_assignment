from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()

# Company info extraction model
class CompanyInfo(BaseModel):
    name: str = Field(description="Company name")
    industry: str = Field(description="Industry sector")
    founded: int = Field(description="Year founded")
    headquarters: str = Field(description="Headquarters location")
    products_services: list[str] = Field(description="Main products or services")
    ceo: str = Field(description="CEO name")
    confidence: float = Field(description="Model's confidence in extraction, 0.0-1.0")
    evaluation: str = Field(description="Model's self-assessment of completeness/reliability")

parser = PydanticOutputParser(pydantic_object=CompanyInfo)

company_prompt_template = """
Analyze the following company description and extract the information below. Return your answer as a valid JSON object in this format:
{{
    "name": "string",
    "industry": "string",
    "founded": 2020,
    "headquarters": "string",
    "products_services": ["string"],
    "ceo": "string",
    "confidence": 0.0,
    "evaluation": "string"
}}
Company description:
{company_text}
Respond only with valid JSON. Do not include any extra text.
{format_instructions}
"""

prompt = PromptTemplate(
    template=company_prompt_template,
    input_variables=["company_text"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

def extract_company_info(company_text):
    chain = prompt | ChatOpenAI(temperature=0.1, model="gpt-4-1106-preview")
    result = chain.invoke({"company_text": company_text})
    return result.content

# Example usage
if __name__ == "__main__":
    sample_description = "Acme Technologies is a leading provider of innovative software solutions for businesses worldwide. Founded in 2010, Acme specializes in cloud computing, artificial intelligence, and cybersecurity products designed to help organizations streamline operations and enhance digital security. With a global team of experts and a commitment to customer success, Acme Technologies empowers clients to achieve their business goals through cutting-edge technology and exceptional service. The company is headquartered in San Francisco, CA, and led by CEO Jane Doe."
    print(extract_company_info(sample_description))