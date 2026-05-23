import json
import os
from dotenv import load_dotenv
from openai import OpenAI

# ---------------------------
# LOAD ENV VARIABLES
# ---------------------------
load_dotenv()

# ---------------------------
# OPENROUTER CLIENT SETUP
# ---------------------------
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# ---------------------------
# SYSTEM PROMPT
# ---------------------------
SYSTEM_PROMPT = """
You are an AI career roadmap generator.

Generate ONLY valid raw JSON.

DO NOT use markdown.
DO NOT use ```json.
Return pure JSON only.

Rules:
1. Return exactly 7 milestones.
2. Codes must be M01 to M07.

blur_level rules:
M01 = 0
M02 = 0
M03 = 1
M04 = 2
M05 = 3
M06 = 3
M07 = 3

LANGUAGE RULES:
- If language is "en", ALL text must be in English.
- If language is "hi", unlock_statement must be in Hindi.
- Never mix English and Hindi.

Output schema:

{
  "milestones": [
    {
      "code": "M01",
      "title": "",
      "salary_tier": "",
      "unlock_statement": "",
      "blur_level": 0,
      "scenario_count": 0,
      "assessment_count": 0,
      "mock_interview_count": 0
    }
  ]
}

Requirements:
- salary_tier must use Indian LPA format only
- Example:
  "4 LPA → 8 LPA"

- unlock_statement must feel personal and practical
- output must be valid JSON
- no extra explanation text
"""

# ---------------------------
# SAMPLE USER INPUT
# ---------------------------
sample_input = {
    "icp_type": "high_wage",   # change to low_wage
    "name": "Riya Sharma",
    "current_role": "Final year CS student",
    "target_role": "AI Engineer",
    "urgency_months": 6,
    "skills": ["Python", "SQL"],
    "language": "en",   # change to hi

    "vision_profile": {
        "current_life": "Studying for placements",
        "main_blocker": "No project experience",
        "vision_12mo": "Working in a product company",
        "top_motivation": "Want career growth"
    }
}

# ---------------------------
# FINAL PROMPT
# ---------------------------
prompt = f"""
{SYSTEM_PROMPT}

User Input:
{json.dumps(sample_input, indent=2, ensure_ascii=False)}

Generate roadmap JSON now.
"""

# ---------------------------
# API CALL
# ---------------------------
response = client.chat.completions.create(
    model="meta-llama/llama-3.1-8b-instruct",

    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

# ---------------------------
# EXTRACT RESPONSE
# ---------------------------
roadmap_text = response.choices[0].message.content.strip()

# ---------------------------
# REMOVE MARKDOWN IF PRESENT
# ---------------------------
roadmap_text = roadmap_text.replace("```json", "")
roadmap_text = roadmap_text.replace("```", "").strip()

# ---------------------------
# FIX MISSING BRACKET
# ---------------------------
if not roadmap_text.endswith("}"):
    roadmap_text += "\n}"

# ---------------------------
# SAVE OUTPUT
# ---------------------------
with open("output.json", "w", encoding="utf-8") as f:
    f.write(roadmap_text)

# ---------------------------
# PRINT OUTPUT
# ---------------------------
print(roadmap_text)
print("\nRoadmap saved successfully in output.json")