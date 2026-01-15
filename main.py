from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/generate-script")
async def generate_script(video: UploadFile = File(...)):

    # Save temp file
    contents = await video.read()
    temp_video = "uploaded.mp4"
    with open(temp_video, "wb") as f:
        f.write(contents)

    # Send video to OpenAI for transcription
    audio_file = open(temp_video, "rb")
    transcript = client.audio.transcriptions.create(
        model="gpt-4o-transcribe",  # Whisper v3
        file=audio_file
    )

    english = transcript.text

    # Translate to Burmese
    translate = client.responses.create(
        model="gpt-4o-mini",
        input=f"Translate this to Myanmar language:\n\n{english}"
    )

    myanmar = translate.output[0].content[0].text

    return {"english": english, "myanmar": myanmar}