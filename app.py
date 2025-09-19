#import required modules
import os
import openai
import json
import re
from datetime import datetime

def extract_founding_year(text):
	
	match = re.search(r'(Founded|established|since|started|created)[^\d]*(\d{4})', text, re.IGNORECASE)
	if match:
		return int(match.group(2))
	# Fallback: look for any year between 1800 and current year
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


# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def build_prompt(text):
		return f"""
Extract all person names, organization names, location names, and email addresses from the following text. Return the result as valid JSON in the format:
{{
	\"persons\": [\"string\"],
	\"organizations\": [\"string\"],
	\"locations\": [\"string\"],
	\"emails\": [\"string\"]
}}
Text: \"{text}\"
Respond only with valid JSON. Do not include any extra text.
After extracting the required information, evaluate the completeness 
and accuracy of your results. If any key information is missing or 
uncertain, include a 'confidence' score (0-1) and a brief 'evaluation' 
comment in the JSON output.
"""

def extract_entities(text):
	prompt = build_prompt(text)
	response = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
		messages=[{"role": "user", "content": prompt}],
		max_tokens=300,
		temperature=0
	)
	# Extract the JSON from the response
	content = response["choices"][0]["message"]["content"]
	try:
		result = json.loads(content)
	except Exception:
		result = {"error": "Failed to parse JSON", "raw": content}
	return result

if __name__ == "__main__":
	text = input("Enter text to extract entities from: ")
	output = extract_entities(text)
	age = calculate_company_age(text)
	output["company_age"] = age if age is not None else None
	print(json.dumps(output, indent=2))
