from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from rembg.bg import remove as remove_bg
from PIL import Image
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Mount the uploads directory
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.post("/remove-background/")
async def remove_background(file: UploadFile = File(...)):
    filename_without_ext = os.path.splitext(file.filename)[0]
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = os.path.join(UPLOAD_FOLDER, f'output_{filename_without_ext}.png')

    # Save uploaded file
    with open(input_path, "wb") as buffer:
        buffer.write(await file.read())

    # Process image
    input_image = Image.open(input_path)
    output = remove_bg(input_image)
    output.save(output_path)

    # Return the processed image file
    return FileResponse(output_path)

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Remove Background</title>
    </head>
    <body>
        <h1>Upload an Image to Remove Background</h1>
        <form action="/remove-background/" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept="image/*" required>
            <button type="submit">Upload</button>
        </form>
    </body>
    </html>
    """

@app.on_event("startup")
async def startup_event():
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting server on port {port}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")