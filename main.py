from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Allow frontend access
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
async def generate_script(file: UploadFile = File(...)):

    eng_script = "This is an English script generated from your video."
    mm_script = "ဒီလိုမျိုး မြန်မာ script ကိုပါ generate လုပ်ပြထားပါတယ်။"

    return {"eng": eng_script, "mm": mm_script}


@app.get("/voice-eng")
async def eng_voice():
    return {"url": "https://example.com/eng.mp3"}


@app.get("/voice-mm")
async def mm_voice():
    return {"url": "https://example.com/mm.mp3"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)