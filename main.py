from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "AI Backend is running!"}


# ------------------------------ 1) Generate Script ------------------------------
@app.post("/generate-script")
async def generate_script(video: UploadFile = File(...)):

    # 1. Save uploaded video temporarily
    video_bytes = await video.read()
    with open("uploaded_video.mp4", "wb") as f:
        f.write(video_bytes)

    # 2. Whisper Speech-to-Text
    audio_file = open("uploaded_video.mp4", "rb")
    transcript = openai.audio.transcriptions.create(
        model="gpt-4o-transcribe",
        file=audio_file
    )

    raw_text = transcript.text

    # 3. Generate English Script (GPT)
    english_script = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Rewrite into a clear, smooth narration script for a video."},
            {"role": "user", "content": raw_text}
        ]
    ).choices[0].message.content

    # 4. Translate to Myanmar
    myanmar_script = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Translate to Myanmar language."},
            {"role": "user", "content": english_script}
        ]
    ).choices[0].message.content

    return {"english": english_script, "myanmar": myanmar_script}


# ------------------------------ 2) English Voice ------------------------------
@app.post("/voice-en")
async def voice_en(data: dict):

    text = data["text"]

    speech = openai.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    )

    with open("eng_voice.mp3", "wb") as f:
        f.write(speech.read())

    return FileResponse("eng_voice.mp3", media_type="audio/mp3", filename="english_voice.mp3")


# ------------------------------ 3) Myanmar Voice ------------------------------
@app.post("/voice-mm")
async def voice_mm(data: dict):

    text = data["text"]

    speech = openai.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    )

    with open("mm_voice.mp3", "wb") as f:
        f.write(speech.read())

    return FileResponse("mm_voice.mp3", media_type="audio/mp3", filename="myanmar_voice.mp3")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)