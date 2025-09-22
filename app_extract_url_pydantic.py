import json
def extract_company_info_from_url(url):
    """
    Fetches the web page, extracts visible text, and returns company info in JSON format.
    """
    page_text = fetch_webpage_text(url)
    if not page_text.strip() or len(page_text.strip()) < 50:
        return json.dumps({"error": "No sufficient text could be extracted from the web page."}, indent=2)
    info = extract_company_info(page_text)
    try:
        return json.dumps(json.loads(info), indent=2)
    except Exception:
        return info
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()


# URL extraction function
import requests
from bs4 import BeautifulSoup

# def extract_text_from_url(url, css_selector=None):
#     """
#     Fetches the web page at the given URL and extracts visible text from:
#     - Title
#     - Meta description
#     - Paragraphs, headings, divs, and spans
#     Optionally, extracts text from a specific CSS selector.
#     Returns the combined text as a string.
#     """
#     try:
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.text, "html.parser")
#         texts = []
#         # Title
#         if soup.title and soup.title.string:
#             texts.append(soup.title.string.strip())
#         # Meta description
#         meta_desc = soup.find("meta", attrs={"name": "description"})
#         if meta_desc and meta_desc.get("content"):
#             texts.append(meta_desc["content"].strip())
#         # Paragraphs, headings, divs, spans
#         for tag in soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6", "div", "span"]):
#             if tag.text:
#                 texts.append(tag.text.strip())
#         # CSS selector (optional, for targeted extraction)
#         if css_selector:
#             for tag in soup.select(css_selector):
#                 if tag.text:
#                     texts.append(tag.text.strip())
#         return "\n".join(texts)
#     except Exception as e:
#         print(f"Error fetching or parsing URL: {e}")
#         return ""
def fetch_webpage_text(url):
    """
    Fetches the web page at the given URL and extracts visible text from:
    - Title
    - Meta description
    - Paragraphs, headings, divs, and spans
    Returns the combined text as a string.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        texts = []
        # Title
        if soup.title and soup.title.string:
            texts.append(soup.title.string.strip())
        # Meta description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"):
            texts.append(meta_desc["content"].strip())
        # Paragraphs, headings, divs, spans
        for tag in soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6", "div", "span"]):
            if tag.text:
                texts.append(tag.text.strip())
        # Fallback: all visible strings
        if not texts:
            texts = list(soup.stripped_strings)
        return "\n".join(texts)
    except Exception as e:
        print(f"Error fetching or parsing URL: {e}")
        return ""

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




if __name__ == "__main__":
    mode = input("Type 'url' to extract from web page or 'text' for sample description: ").strip().lower()

    if mode == "url":
        url = input("Enter the web page URL: ").strip()
        print("\nExtracted company info (JSON):")
        print(extract_company_info_from_url(url))
    else:
        sample_description = "Acme Technologies is a leading provider of innovative software solutions for businesses worldwide. Founded in 2010, Acme specializes in cloud computing, artificial intelligence, and cybersecurity products designed to help organizations streamline operations and enhance digital security. With a global team of experts and a commitment to customer success, Acme Technologies empowers clients to achieve their business goals through cutting-edge technology and exceptional service. The company is headquartered in San Francisco, CA, and led by CEO Jane Doe."
        print(extract_company_info(sample_description))