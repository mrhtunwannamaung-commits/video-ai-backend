from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import uvicorn
import openai
import os

# Load API KEY
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Allow CORS (Frontend can access backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "FastAPI backend is running with OpenAI!"}


# -------------------- 1) Generate Script (AI Version) --------------------
@app.post("/generate-script")
async def generate_script(video: UploadFile = File(...)):
    # Save video temporarily
    contents = await video.read()
    with open("uploaded_video.mp4", "wb") as f:
        f.write(contents)

    # 🔥 Use OpenAI to generate script
    prompt = """
    You are a video script generator AI.
    Write an English and Myanmar explanation based on the video content.
    If the video cannot be analyzed, generate a general explanation.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You generate English and Myanmar scripts."},
            {"role": "user", "content": prompt}
        ]
    )

    english_script = response["choices"][0]["message"]["content"]

    # Dummy Myanmar translation (because video is not analyzed)
    myanmar_script = "ဤဗီဒီယိုအတွက် AI မှ စာတမ်းဖော်ပြချက်ကို ပြန်လည်ဖော်ထုတ်ပေးထားပါသည်။"

    return {
        "english": english_script,
        "myanmar": myanmar_script
    }


# -------------------- 2) English Voice (Return eng.wav) --------------------
@app.post("/voice-en")
async def voice_en(data: dict):
    return FileResponse(
        "eng.wav",
        media_type="audio/wav",
        filename="english_voice.wav"
    )

# -------------------- 3) Myanmar Voice (Return mm.wav) --------------------
@app.post("/voice-mm")
async def voice_mm(data: dict):
    return FileResponse(
        "mm.wav",
        media_type="audio/wav",
        filename="myanmar_voice.wav"
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)