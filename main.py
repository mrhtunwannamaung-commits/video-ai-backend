from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI()

# Allow CORS
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


# --------------------- 1) Generate Script ---------------------
@app.post("/generate-script")
async def generate_script(video: UploadFile = File(...)):

    # Video file save temporarily (for future processing)
    contents = await video.read()
    with open("uploaded.mp4", "wb") as f:
        f.write(contents)

    # Dummy text (change this later if using AI)
    english = "Your video was successfully received. English script generated."
    myanmar = "သင့် video ကို backend ကသေချာလက်ခံပြီး မြန်မာ script ကို generate လုပ်ပြီးပြီ။"

    return {"english": english, "myanmar": myanmar}


# --------------------- 2) English Voice ---------------------
@app.post("/voice-en")
async def voice_en(data: dict):
    return FileResponse(
        "eng.wav",
        media_type="audio/wav",
        filename="english_voice.wav"
    )


# --------------------- 3) Myanmar Voice ---------------------
@app.post("/voice-mm")
async def voice_mm(data: dict):
    return FileResponse(
        "mm.wav",
        media_type="audio/wav",
        filename="myanmar_voice.wav"
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)