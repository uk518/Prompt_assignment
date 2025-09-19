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
Summarize the following meeting notes. Extract and return the following information as a valid JSON object:
{{
  "attendees": ["string"],
  "action_items": ["string"],
  "decisions": ["string"],
  "date": "string"
}}
Meeting notes:
\"\"\"{notes}\"\"\"
Respond only with valid JSON. Do not include any extra text.
""" 


def extract_information(notes):
    try:
        response=openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": USER_PROMPT_TEMPLATE.format(notes=notes)}
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
    
def build_json_validation_prompt(json_output):
        return f"""
You previously generated the following JSON:

{json_output}

Please validate this JSON for correctness and completeness. Ensure all required keys are present, values are in the expected format, and the information is as complete as possible. Return your validation as a JSON object with these keys:
{{
    \"is_correct\": true/false,
    \"is_complete\": true/false,
    \"missing_keys\": [\"string\"],
    \"issues\": [\"string\"],
    \"suggestions\": [\"string\"]
}}
Respond only with valid JSON. Do not include any extra text.
"""   
    



if __name__=="__main__":
    notes="""
    "Project Kickoff Meeting – September 18, 2025

    Attendees: Alice Johnson, Bob Smith, Carol Lee, David Kim

    Decisions:

    The project will use the Agile methodology.
    Weekly status meetings will be held every Monday at 10 AM.
    Action Items:

    Alice to set up the project repository by September 20.
Bob to prepare the initial project plan.
Carol to gather requirements from stakeholders.
David to organize the next meeting.
Next meeting scheduled for September 22, 2025."
    """
    summarized_data=extract_information(notes)
    print("Final Extracted Data:\n",summarized_data)
    validation_prompt=build_json_validation_prompt(json.dumps(summarized_data, indent=2))
    # Send validation prompt to LLM and print validation result
    try:
        validation_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": validation_prompt}],
            max_tokens=300,
            temperature=0
        )
        validation_content = validation_response.choices[0].message.content.strip()
        try:
            validation_result = json.loads(validation_content)
        except json.JSONDecodeError as e:
            print("Validation JSON parsing error:\n", str(e))
            validation_result = {"error": "JSON parsing error", "details": str(e), "raw_output": validation_content}
    except Exception as e:
        print("Validation API call failed with error:\n", str(e))
        validation_result = {"error": "API call failed", "details": str(e)}
    print("Validation Result:\n", json.dumps(validation_result, indent=2))
