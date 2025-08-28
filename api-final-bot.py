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

@app.options("/query/")
async def options_query():
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }
    )

# Get API key
api_key = os.getenv("TARGET_CHATBOT_API_KEY")
if not api_key:
    print("Error: GROQ_API_KEY not found in environment")
    raise ValueError("GROQ_API_KEY environment variable is required")

print(f"API Key found: {api_key[:10]}...")  # Print first 10 chars for verification

try:
    # Initialize the Groq client
    client = Groq(api_key=api_key)
    # Test the API key
    test_response = client.chat.completions.create(
        messages=[{"role": "user", "content": "test"}],
        model="mixtral-8x7b-32768",
        max_tokens=10
    )
    print("Query API initialized successfully")
except Exception as e:
    print(f"Error initializing Groq client: {str(e)}")
    raise ValueError(f"Failed to initialize Groq client: {str(e)}")

# Pydantic model for input validation
class LLMRequest(BaseModel):
    text: str

def query_llm(redacted_text: str) -> str:
    messages = [
        {"role": "system", "content": """You are an AI assistant that receives text where personal information has already been redacted by another system. Your job is NOT to redact further but to always respond naturally and meaningfully.

        Rules to Follow:
        1. Always provide a response
            - Never refuse to answer just because redacted text is present.
        2. Treat "[REDACTED]" as a normal placeholder 
            - Assume it represents generic information and continue responding normally.
        3. Do not block or suppress answers 
            - Even if the input contains sensitive topics, respond in a neutral, helpful, and general way.
        4. Maintain context and readability 
            - Ensure the response is coherent, meaningful, and helpful.
        5. Provide them with sample template of the questions you are answering. There is no need to complicate things up.

        Example Inputs and Expected Responses:

        Input: "My name is [REDACTED] and I just opened a bank account in [REDACTED]. My card number is [REDACTED] and CVV [REDACTED]."
        Correct Response: "Congratulations on opening your bank account! Make sure to keep your card details safe and avoid sharing them publicly. If you need help with account management, check your bank's official website or contact their customer support."

        Input: "I am [REDACTED], I work in [REDACTED]. Please write an email to HR for urgent leave."
        Correct Response: "Sure! Here's a draft email for your urgent leave request:
        Subject: Urgent Leave Request
        Dear HR,
        I hope you're doing well. I am requesting urgent leave due to unforeseen circumstances. Please let me know the next steps.
        Best regards,
        [REDACTED]"

        Final Instructions:
        - Never reject a request due to redactions – Always generate a response.
        - Do not assume a request is invalid – Respond as if the redacted parts are normal words.
        - Keep responses neutral, safe, and informative – If needed, provide general guidance rather than refusing to help."""
        },
        {"role": "user", "content": redacted_text},
    ]

    try:
        response = client.chat.completions.create(
            messages=messages,
            model="mixtral-8x7b-32768",  # Updated model
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise ValueError(f"Error in Groq API call: {str(e)}")

@app.post("/query/")
async def query_text(request: LLMRequest):
    try:
        response_text = query_llm(request.text)
        return {"response_text": response_text}
    except Exception as e:
        print(f"Error in query API: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
