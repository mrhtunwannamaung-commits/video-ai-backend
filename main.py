from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI()

# Allow frontend (GitHub Pages) to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allow all domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "FastAPI backend is running!"}

# -------------------------
# 1) Generate Script API
# -------------------------
@app.post("/generate-script")
async def generate_script(video: UploadFile = File(...)):
    # Dummy output
    english = "This is an English script generated from your video."
    myanmar = "ဒီလို မြန်မာ script ကို generate လုပ်ပြီး ပြန်ပေးထားပါတယ်။"
    return {"english": english, "myanmar": myanmar}


# -------------------------
# 2) English Voice API (WAV)
# -------------------------
@app.post("/voice-en")
async def voice_en(data: dict):
    # File eng.wav must exist in GitHub backend repo
    return FileResponse("eng.wav",
                        media_type="audio/wav",
                        filename="english_voice.wav")


# -------------------------
# 3) Myanmar Voice API (WAV)
# -------------------------
@app.post("/voice-mm")
async def voice_mm(data: dict):
    # File mm.wav must exist in GitHub backend repo
    return FileResponse("mm.wav",
                        media_type="audio/wav",
                        filename="myanmar_voice.wav")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)