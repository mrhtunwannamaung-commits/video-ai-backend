from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "FastAPI backend is running!"}

@app.post("/generate-script")
async def generate_script(video: UploadFile = File(...)):
    english = "This is an English script generated from your video."
    myanmar = "ဒီလိုမျိုး မြန်မာ script ကို generate လုပ်ပြီး ပြန်ပေးထားပါတယ်။"
    return {"english": english, "myanmar": myanmar}

@app.post("/voice-en")
async def voice_en(data: dict):
    return FileResponse("eng.mp3", media_type="audio/mpeg", filename="english_voice.mp3")

@app.post("/voice-mm")
async def voice_mm(data: dict):
    return FileResponse("mm.mp3", media_type="audio/mpeg", filename="myanmar_voice.mp3")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)