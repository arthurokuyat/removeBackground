from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from rembg.bg import remove as remove_bg
from PIL import Image
import os

app = FastAPI()

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Cache for storing processed images
cache = {}

@app.post("/remove-background/")
async def remove_background(file: UploadFile = File(...)):
    # Get the filename and remove its extension
    filename_without_ext = os.path.splitext(file.filename)[0]

    # Check if the image is already cached
    if file.filename in cache:
        return JSONResponse(content={"processed_image_url": cache[file.filename]})

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = os.path.join(UPLOAD_FOLDER, f'output_{filename_without_ext}.png')

    with open(input_path, "wb") as buffer:
        buffer.write(await file.read())

    # Use a more powerful model like ISNet or U2Net for background removal
    input_image = Image.open(input_path)
    output = remove_bg(input_image, session_name="u2net")  # Correct the argument name
    # Save the processed image
    output.save(output_path)

    # Generate the processed image URL
    processed_image_url = f"https://your-cloud-run-url/uploads/{os.path.basename(output_path)}"

    # Cache the result
    cache[file.filename] = processed_image_url

    return JSONResponse(content={"processed_image_url": processed_image_url})

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)