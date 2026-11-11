import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

# 1. Load the secret API key from your .env file
load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    raise ValueError("Missing GROQ_API_KEY. Please add it to your .env file.")

# 2. Initialize the FastAPI app and Groq client
app = FastAPI(title="Cultivating Community Backend")
client = Groq(api_key=api_key)

# 3. Enable CORS so your GitHub Pages front-end can fetch data from this server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows your local frontend to hit this backend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Define the incoming data structure
class ChatRequest(BaseModel):
    message: str

# 5. Build the secure chat endpoint
@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    user_message = request.message.strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
    
    try:
        # Call Groq dynamically with Monique's strict persona
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Monique, a helpful, witty, and direct AI companion for 'Cultivating Community', "
                        "a 501(c)(3) nonprofit fostering sustainable local food systems across Washington, D.C. "
                        "Your tone is warm, engaging, lively, playful, and sharp with a touch of dry wit. "
                        "Keep your answers short, natural, and conversational like a human talking over chat. "
                        "Strict Boundaries: You ONLY discuss public community-facing information: Sunday free grocery "
                        "distributions (Sundays 12 PM–2 PM at 3417 14th St. NW), volunteering via Timecounts "
                        "(logistics, distribution, IT, events), programs (urban farm, food rescue, distribution), "
                        "and public donations. Never discuss internal organizational strategy, operational metrics, "
                        "board plans, grants, or financial ledgers. If asked about internal matters, playfully deflect "
                        "and redirect back to community participation."
                    )
                },
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=250
        )
        
        reply = completion.choices[0].message.content
        return {"reply": reply}
        
    except Exception as e:
        print(f"Groq API Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to connect to the AI model.")

if __name__ == "__main__":
    import uvicorn
    # Runs the server on localhost:8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
