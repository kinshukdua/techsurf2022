from flask import Flask, render_template, request
from utils import get_size, convert_size
from algorithms import optimal_compression
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] =  os.path.join('static', 'uploads')

@app.route('/upload_file', methods=['POST'])
def upload_file():
    """
    A function to upload a file to the server.
    Returns the ratio and the compressed image.
    """
    if request.method == "POST":

        image = request.files['file']

        optimal_ratio, final_image = optimal_compression(image)
        filename = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        final_image.save(filename, optimize=True, quality=50)

        original_size = get_size(image)
        new_size = os.stat(filename).st_size

        density = int(100*optimal_ratio)

        optimization = round(100*(original_size-new_size)/original_size,2)

        return render_template("show.html", 
                                user_image=filename, 
                                density=density, old_size=convert_size(original_size),
                                new_size=convert_size(new_size),
                                optimization=optimization)

@app.route('/upload', methods = ['GET'])
def upload_file_html():
    if request.method == "GET":
        return render_template("upload.html")


if __name__ == '__main__':
   app.run(debug = True)