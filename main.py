from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Enable CORS for frontend
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


# ---------- 1) Generate Script ----------
@app.post("/generate-script")
async def generate_script(video: UploadFile = File(...)):

    # Dummy example output
    english = "This is an English script generated from your video."
    myanmar = "ဒီလိုမျိုး မြန်မာ script ကို generate လုပ်ပြီး ပြန်ပေးထားပါတယ်။"

    # Frontend expects english + myanmar keys
    return {"english": english, "myanmar": myanmar}


# ---------- 2) English Voice ----------
@app.post("/voice-en")
async def voice_en(data: dict):

    # Normally this returns audio file, right now dummy
    return {"url": "https://example.com/eng.mp3"}


# ---------- 3) Myanmar Voice ----------
@app.post("/voice-mm")
async def voice_mm(data: dict):

    # Dummy voice URL again
    return {"url": "https://example.com/mm.mp3"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)