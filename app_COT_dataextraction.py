import requests
from bs4 import BeautifulSoup
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
load_dotenv()
# 🔹 Step 1: Fetch webpage text
def extract_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove script and style content
    for script in soup(["script", "style"]):
        script.decompose()

    return soup.get_text(separator=" ", strip=True)

# 🔹 Step 2: Define CoT-style prompt
prompt = PromptTemplate(
    input_variables=["document"],
    template="""
    You are an expert in company data extraction.

    Follow this reasoning process step by step:
    Step 1: Read the text carefully.
    Step 2: Identify company names and entities.
    Step 3: For each company, extract details if available:
        - Company Name
        - Website/URL
        - Location (HQ or branch)
        - Industry / Sector
        - Contact Info (email, phone)
        - Key Executives (CEO, Founder, etc.)
        - Products / Services
    Step 4: Present results in clean JSON format.

    Input text:
    {document}
    """
)

# 🔹 Step 3: LLM Chain
llm = ChatOpenAI(model="gpt-4", temperature=0)
chain = LLMChain(llm=llm, prompt=prompt)

# 🔹 Step 4: Run Extraction
def extract_company_data(url):
    text = extract_text_from_url(url)
    result = chain.run(document=text)
    return result


# Example Usage
if __name__ == "__main__":
    url = "https://www.ibm.com/about"  # try with any company webpage
    data = extract_company_data(url)
    print("📊 Extracted Company Data:\n", data)
