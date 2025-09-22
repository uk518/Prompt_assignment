from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

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


# PDF extraction function
import pdfplumber
import os


# OCR support for scanned/image PDFs
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        if text.strip():
            return text
    except Exception as e:
        print("pdfplumber error:", e)

    # Fallback to OCR if no text extracted
    print("No text found with pdfplumber, trying OCR...")
    try:
        from pdf2image import convert_from_path
        import pytesseract
        images = convert_from_path(pdf_path)
        for img in images:
            ocr_text = pytesseract.image_to_string(img)
            text += ocr_text + "\n"
        return text
    except Exception as e:
        print("OCR extraction failed:", e)
        return ""

if __name__ == "__main__":
    print("If you want to use OCR for scanned PDFs, make sure you have installed:")
    print("- pdf2image: pip install pdf2image")
    print("- pytesseract: pip install pytesseract")
    print("- Tesseract OCR: Download from https://github.com/tesseract-ocr/tesseract and add to your PATH")
    print()
    mode = input("Type 'pdf' to extract from PDF or 'text' for sample description: ").strip().lower()
    if mode == "pdf":
        pdf_path = input("Enter path to company PDF: ").strip()
        if not os.path.exists(pdf_path):
            print("PDF file not found.")
        else:
            pdf_text = extract_text_from_pdf(pdf_path)
            if not pdf_text.strip():
                print("No text could be extracted from the PDF. If this is a scanned document, ensure Tesseract OCR is installed and configured.")
            else:
                print("Extracted text from PDF:\n", pdf_text[:500], "...\n")
                print("\nExtracted company info:")
                print(extract_company_info(pdf_text))
    else:
        sample_description = "Acme Technologies is a leading provider of innovative software solutions for businesses worldwide. Founded in 2010, Acme specializes in cloud computing, artificial intelligence, and cybersecurity products designed to help organizations streamline operations and enhance digital security. With a global team of experts and a commitment to customer success, Acme Technologies empowers clients to achieve their business goals through cutting-edge technology and exceptional service. The company is headquartered in San Francisco, CA, and led by CEO Jane Doe."
        print(extract_company_info(sample_description))