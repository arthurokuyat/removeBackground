from flask import Flask, render_template, request, send_file
from rembg import remove
from PIL import Image
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            # Get the filename and remove its extension
            filename_without_ext = os.path.splitext(file.filename)[0]
            
            input_path = os.path.join(UPLOAD_FOLDER, file.filename)
            output_path = os.path.join(UPLOAD_FOLDER, 'output_' + filename_without_ext + '.png')
            
            print(output_path)
            file.save(input_path)
            
            input_image = Image.open(input_path)
            output = remove(input_image)
            
            output.save(output_path)
            
            return send_file(output_path, as_attachment=True)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    
# to run docker: docker run -p 5000:5000 remove_bg