from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from rembg import remove
from PIL import Image
import os

app = FastAPI()

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.post("/remove-background/")
async def remove_background(file: UploadFile = File(...)):
    # Get the filename and remove its extension
    filename_without_ext = os.path.splitext(file.filename)[0]

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = os.path.join(UPLOAD_FOLDER, f'output_{filename_without_ext}.png')

    with open(input_path, "wb") as buffer:
        buffer.write(await file.read())

    input_image = Image.open(input_path)
    output = remove(input_image)
    output.save(output_path)

    return FileResponse(output_path, media_type="image/png", filename=f"output_{filename_without_ext}.png")

# To run the app: uvicorn app:app --host 0.0.0.0 --port 8000