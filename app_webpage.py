import os
import openai
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

openai.api_key = os.getenv("OPENAI_API_KEY")

def fetch_webpage_text(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'html.parser')
	texts = soup.stripped_strings
	return ' '.join(texts)

def build_prompt(text):
		return f"""
Extract all person names, organization names, location names, email addresses, and founding year from the following text. After extraction, evaluate the completeness and accuracy of your results. Return the result as valid JSON in the format:
{{
	\"persons\": [\"string\"],
	\"organizations\": [\"string\"],
	\"locations\": [\"string\"],
	\"emails\": [\"string\"],
	\"company_age\": int or null,
	\"confidence\": float,
	\"evaluation\": \"string\"
}}
Text: \"{text}\"
Respond only with valid JSON. Do not include any extra text.
"""

def extract_entities(text):
	prompt = build_prompt(text)
	response = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
		messages=[{"role": "user", "content": prompt}],
		max_tokens=400,
		temperature=0
	)
	content = response["choices"][0]["message"]["content"]
	try:
		result = json.loads(content)
	except Exception:
		result = {"error": "Failed to parse JSON", "raw": content}
	# Ensure 'locations' key exists and is a list, even if missing
	if "locations" not in result or not isinstance(result["locations"], list):
		result["locations"] = []
	return result

def extract_founding_year(text):
	match = re.search(r'(Founded|established|since|started|created)[^\d]*(\d{4})', text, re.IGNORECASE)
	if match:
		return int(match.group(2))
	years = re.findall(r'(18\d{2}|19\d{2}|20\d{2}|21\d{2})', text)
	current_year = datetime.now().year
	for year in years:
		y = int(year)
		if 1800 <= y <= current_year:
			return y
	return None

def calculate_company_age(text):
	year = extract_founding_year(text)
	if year:
		return datetime.now().year - year
	return None

if __name__ == "__main__":
	url = input("Enter the web page URL: ")
	page_text = fetch_webpage_text(url)
	output = extract_entities(page_text)
	if "company_age" not in output or output["company_age"] is None:
		age = calculate_company_age(page_text)
		output["company_age"] = age if age is not None else None
	print(json.dumps(output, indent=2))
 
 
 
