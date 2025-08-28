import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get API key
api_key = os.getenv("MIDDLE_BOT_API_KEY")
if not api_key:
    print("Error: GROQ_API_KEY not found")
    raise ValueError("GROQ_API_KEY environment variable is required")

# Initialize the Groq client
client = Groq(api_key=api_key)

# System message for redaction
system_message = {
    "role": "system",
    "content": """
    You are a redactor whose only responsibility is to scan the provided text for any personal or identifying details and replace them with the placeholder "[REDACTED]". Do not perform any other tasks or modifications.

    Identification of Private Information:
    - Detect personal details such as names, addresses, phone numbers, email addresses, etc.
    - Replace these details with "[REDACTED]".

    Examples:
    - Input: "My name is Joseph and I live in New York City."
      Output: "My name is [REDACTED] and I live in [REDACTED]."
    - Input: "You can reach me at john.doe@example.com or at 123-456-7890."
      Output: "You can reach me at [REDACTED] or at [REDACTED]."

    Preserve original sentence structure and punctuation.
    """
}

# Pydantic model for input validation
class RedactionRequest(BaseModel):
    text: str

@app.post("/redact/")
async def redact_text(request: RedactionRequest):
    try:
        messages = [
            system_message,
            {"role": "user", "content": request.text}
        ]

        response = client.chat.completions.create(
            messages=messages,
            model="mixtral-8x7b-32768",
            temperature=0.5,
            max_tokens=1024,
            top_p=1
        )

        redacted_text = response.choices[0].message.content
        return {"redacted_text": redacted_text}
    except Exception as e:
        print(f"Error in redaction API: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.options("/redact/")
async def options_redact():
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }
    )

