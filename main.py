from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.get("/")
def home():
    return {"message": "Backend is running!"}


# ---------------- 1) Generate Script ----------------
@app.post("/generate-script")
async def generate_script(video: UploadFile = File(...)):

    # save video temporarily
    contents = await video.read()
    with open("video.mp4", "wb") as f:
        f.write(contents)

    # 1️⃣ Transcribe the video into English
    transcription = client.audio.transcriptions.create(
        file=open("video.mp4", "rb"),
        model="whisper-1"
    )
    english = transcription.text

    # 2️⃣ Translate English → Myanmar
    mm_prompt = f"Translate this into Myanmar:\n\n{english}"
    mm_resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": mm_prompt}]
    )
    myanmar = mm_resp.choices[0].message.content

    return {"english": english, "myanmar": myanmar}


# ---------------- 2) English Voice ----------------
@app.post("/voice-en")
async def voice_en(data: dict):

    text = data.get("text", "")
    speech = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    )

    with open("english_voice.wav", "wb") as f:
        f.write(speech.read())

    return FileResponse(
        "english_voice.wav",
        media_type="audio/wav",
        filename="english_voice.wav"
    )


# ---------------- 3) Myanmar Voice ----------------
@app.post("/voice-mm")
async def voice_mm(data: dict):

    text = data.get("text", "")
    speech = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    )

    with open("myanmar_voice.wav", "wb") as f:
        f.write(speech.read())

    return FileResponse(
        "myanmar_voice.wav",
        media_type="audio/wav",
        filename="myanmar_voice.wav"
    )


# ---------------- Start ----------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000) 