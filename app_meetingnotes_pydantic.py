from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from typing import List
from dotenv import load_dotenv
load_dotenv()



# Replace with meeting notes summary model and prompt
class MeetingNotesSummary(BaseModel):
    attendees: List[str] = Field(description="List of attendees")
    action_items: List[str] = Field(description="List of action items")
    decisions: List[str] = Field(description="List of decisions made")
    date: str = Field(description="Date of the meeting")
    confidence: float = Field(description="Confidence score (0-1) for completeness and correctness of extraction")
    evaluation: str = Field(description="Self-assessment of output completeness and correctness")

parser = PydanticOutputParser(pydantic_object=MeetingNotesSummary)

System_Prompt = """
You are a helpful AI assistant that summarizes meeting notes and
returns output in a well-structured JSON format.
"""

prompt_template = """
Summarize the following meeting notes. Extract and return the following information as a valid JSON object. After extraction, evaluate the completeness and correctness of your output and include a confidence score (0-1) and a brief evaluation comment:
{format_instructions}
Meeting notes:
{notes}
Respond only with valid JSON. Do not include any extra text.
"""

prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["notes"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

print(parser.get_format_instructions())
print("---")

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
chain = prompt | ChatOpenAI(temperature=0.1, model="gpt-4-1106-preview")
json=chain.invoke({"notes": "Project Kickoff Meeting – September 18, 2025\nAttendees: Alice Johnson, Bob Smith, Carol Lee, David Kim\nDecisions: The project will use the Agile methodology. Weekly status meetings will be held every Monday at 10 AM.\nAction Items: Alice to set up the project repository by September 20. Bob to prepare the initial project plan. Carol to gather requirements from stakeholders. David to organize the next meeting.\nNext meeting scheduled for September 22, 2025."})
print(json.content)