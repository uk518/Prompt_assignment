from dotenv import load_dotenv
load_dotenv()

import openai
import json
import os
# os.environ["OPENAI_API_KEY"]
# Client=openai
openai.api_key = os.getenv("OPENAI_API_KEY")
System_Prompt="""
You are a helpful AI assisstant that summarize meeting notes and 
return output in a well-structured Json format.
"""
USER_PROMPT_TEMPLATE="""
Analyze the following product review and extract the information below. Return your answer as a valid JSON object in this format:
{{
  "product_name": "string",
  "reviewer": "string",
  "rating": "number or string",
  "pros": ["string"],
  "cons": ["string"],
  "overall_stats": "string"
}}
Review text:
\"\"\"{review_text}\"\"\"
Respond only with valid JSON. Do not include any extra text.

""" 

def extract_information(review_text):
    try:
        response=openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": USER_PROMPT_TEMPLATE.format(review_text=review_text)}
            ],
            max_tokens=500,
            temperature=0.2
        )
        output_text=response.choices[0].message.content.strip()
        print("Raw model output:\n",output_text)
        try:
            extracted_data=json.loads(output_text)
            return extracted_data
        except json.JSONDecodeError as e:
            print("JSON parsing error:\n",str(e))
            return {"error":"JSON parsing error","details":str(e),"raw_output":output_text}
        
    except Exception as e:
        print("API call failed with error:\n",str(e))
        return {"error":"API call failed","details":str(e)}

if __name__=="__main__":
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
    summarized_data=extract_information(notes)
    print("Final Extracted Data:\n",summarized_data)



