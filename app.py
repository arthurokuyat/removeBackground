from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from rembg.bg import remove as remove_bg
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

    # Use a more powerful model like ISNet or U2Net for background removal
    input_image = Image.open(input_path)
    output = remove_bg(input_image, session_name="u2net")  # Correct the argument name
    output.save(output_path)

    return FileResponse(output_path, media_type="image/png", filename=f"output_{filename_without_ext}.png")

@app.get("/", response_class=HTMLResponse)
def root():
    return """<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Remove Image Background</title>
</head>
<body>
    <h1>Upload an Image to Remove Background</h1>
    <form action=\"/remove-background/\" method=\"POST\" enctype=\"multipart/form-data\">
        <input type=\"file\" name=\"file\" accept=\"image/*\" required>
        <button type=\"submit\">Upload and Remove Background</button>
    </form>
</body>
</html>"""

# To run the app: uvicorn app:app --host 0.0.0.0 --port 8000