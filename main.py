from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI()

# CORS allow frontend
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


# ----------- 1) Generate Script (Dummy Text) -----------
@app.post("/generate-script")
async def generate_script(video: UploadFile = File(...)):
    english = "This is an English script generated from your video."
    myanmar = "ဒါက သင့် video ကနေ generate လုပ်ထားတဲ့ မြန်မာ script ဖြစ်ပါတယ်။"

    return {"english": english, "myanmar": myanmar}


# ----------- 2) English Voice (Return eng.wav) -----------
@app.post("/voice-en")
async def voice_en(data: dict):
    return FileResponse(
        "eng.wav",
        media_type="audio/wav",
        filename="english_voice.wav"
    )


# ----------- 3) Myanmar Voice (Return mm.wav) -----------
@app.post("/voice-mm")
async def voice_mm(data: dict):
    return FileResponse(
        "mm.wav",
        media_type="audio/wav",
        filename="myanmar_voice.wav"
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)