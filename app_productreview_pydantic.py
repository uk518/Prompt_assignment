from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from typing import List
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
load_dotenv()

class ProductReviewSummary(BaseModel):
        product_name: str = Field(description="Name of the product")
        reviewer: str = Field(description="Name of the reviewer")
        rating: str = Field(description="Rating given to the product")
        pros: List[str] = Field(description="List of pros")
        cons: List[str] = Field(description="List of cons")
        overall_stats: str = Field(description="Overall summary or stats of the product")
        confidence: float = Field(description="Confidence score (0-1) for completeness and correctness of extraction")
        evaluation: str = Field(description="Self-assessment of output completeness and correctness")

System_Prompt = """
You are a helpful AI assistant that analyzes product reviews and
returns output in a well-structured JSON format.
"""
prompt_template = """
Analyze the following product review and extract the information below. Return your answer as a valid JSON object in this format. After extraction, evaluate the completeness and correctness of your output and include a confidence score (0-1) and a brief evaluation comment:
{{
    "product_name": "string",
    "reviewer": "string",
    "rating": "number or string",
    "pros": ["string"],
    "cons": ["string"],
    "overall_stats": "string",
    "confidence": 0.0,
    "evaluation": "string"
}}
Review text:
{review_text}
Respond only with valid JSON. Do not include any extra text.
"""



parser = PydanticOutputParser(pydantic_object=ProductReviewSummary)

prompt = PromptTemplate(
    template=prompt_template,
    input_variables=[],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)


notes="""
   "I recently purchased the SoundMax Pro Wireless Headphones, 
   and I am very impressed with their performance. As an avid
   music lover, I appreciate the deep bass and clear treble these 
   headphones deliver. The battery life is outstanding, lasting over
   20 hours on a single charge. The reviewer, John Doe, found the 
   headphones comfortable for long listening sessions and praised 
   the easy Bluetooth connectivity. However, the ear cups can feel 
   a bit warm after extended use, and the price is slightly higher 
   compared to similar models. Overall, the SoundMax Pro offers excellent 
   sound quality and durability, making it a top choice for audiophiles."
    """
chain = prompt | ChatOpenAI(temperature=0.1, model="gpt-4-1106-preview")
json = chain.invoke({"review_text": notes})

print(json.content)