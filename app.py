import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq

app = FastAPI(title="Cultivating Community Secure AI Backend")

# Enable CORS so your GitHub Pages frontend can talk securely to your backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, you can lock this down to your exact domain: https://foodsovereigntyforall.com
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq client safely using your environment variable
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Monique, a helpful, witty, and direct AI companion for 'Cultivating Community', "
                        "a 501(c)(3) nonprofit fostering sustainable local food systems across Washington, D.C. "
                        "Your tone is warm, engaging, lively, playful, and sharp with a touch of dry wit. "
                        "Keep your answers short, natural, and conversational like a human talking over voice or chat. "
                        "Strict Boundaries: You ONLY discuss public community-facing information: Sunday free grocery "
                        "distributions (Sundays 12 PM–2 PM at 3417 14th St. NW), volunteering via Timecounts "
                        "(logistics, distribution, IT, events), programs (urban farm, food rescue, distribution), "
                        "and public donations. Never discuss internal organizational strategy, operational metrics, "
                        "board plans, grants, or financial ledgers. If asked about internal matters, playfully deflect "
                        "and redirect back to community participation."
                    )
                },
                {"role": "user", "content": request.message}
            ],
            temperature=0.7,
            max_tokens=300
        )
        
        reply = completion.choices[0].message.content
        return {"reply": reply}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
