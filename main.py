from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
from uuid import uuid4
import os
import json

from hilbert import HilbertDNACodec
from tex_to_dna import text_to_dna, dna_to_text

# ================================
# Setup
# ================================

app = FastAPI(title="Text ↔ DNA ↔ Image API")

codec = HilbertDNACodec()

STORAGE_DIR = "storage"
IMAGE_DIR = os.path.join(STORAGE_DIR, "images")
META_FILE = os.path.join(STORAGE_DIR, "metadata.json")

os.makedirs(IMAGE_DIR, exist_ok=True)

if not os.path.exists(META_FILE):
    with open(META_FILE, "w") as f:
        json.dump({}, f)

# ================================
# Models
# ================================

class TextRequest(BaseModel):
    text: str

# ================================
# Helpers
# ================================

def load_metadata():
    with open(META_FILE, "r") as f:
        return json.load(f)

def save_metadata(data):
    with open(META_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ================================
# ROUTES
# ================================

@app.post("/encode_text")
def encode_text(request: TextRequest):

    # Step 1: Text → DNA
    dna = text_to_dna(request.text)

    # Step 2: DNA → Image
    record_id = str(uuid4())
    image_path = os.path.join(IMAGE_DIR, f"{record_id}.png")

    codec.dna_to_image(dna, image_path)

    # Store locally
    metadata = load_metadata()
    metadata[record_id] = {
        "text": request.text,
        "dna": dna,
        "image": f"{record_id}.png"
    }
    save_metadata(metadata)

    return {
        "id": record_id,
        "image_url": f"/image/{record_id}"
    }


@app.post("/decode_image")
async def decode_image(file: UploadFile = File(...)):

    temp_path = os.path.join(IMAGE_DIR, "temp_decode.png")

    with open(temp_path, "wb") as buffer:
        buffer.write(await file.read())

    # Step 1: Image → DNA

    dna = codec.image_to_dna(temp_path)
    print("Extracted DNA length:", len(dna))
    print("Extracted DNA mod 9:", (len(dna)*2) % 9)


    os.remove(temp_path)

    # Step 2: DNA → Text
    try:
        text = dna_to_text(dna)
    except ValueError as e:
        return {"error": str(e)}


    return {
        "decoded_text": text
    }


@app.get("/image/{record_id}")
def get_image(record_id: str):

    image_path = os.path.join(IMAGE_DIR, f"{record_id}.png")

    if not os.path.exists(image_path):
        return {"error": "Image not found"}

    return FileResponse(image_path, media_type="image/png")


@app.get("/records")
def list_records():
    return load_metadata()


@app.get("/record/{record_id}")
def get_record(record_id: str):

    metadata = load_metadata()

    if record_id not in metadata:
        return {"error": "Record not found"}

    return metadata[record_id]


from fastapi.staticfiles import StaticFiles

app.mount("/", StaticFiles(directory="static", html=True), name="static")
