import cv2
from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from image_processor import process_image
from database import init_db, insert_metadata, get_metadata
from datetime import datetime
from flask import send_from_directory

app = Flask(__name__)
# Local upload folder
app.config['UPLOAD_FOLDER'] = 'app/images/uploads'
# Local processed folder       
app.config['PROCESSED_FOLDER'] = 'app/images/processed'  

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

# Initialize the database
init_db()

@app.route('/')
def index():
    # Fetch metadata
    metadata = get_metadata()
    return render_template('dashboard.html', metadata=metadata)

@app.route('/upload', methods=['Get', 'POST'])
def upload_file():
    file = request.files['file']
    if file:
        # Save uploaded file locally
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Get the size of the original image in bytes
        original_image_size_bytes = os.path.getsize(file_path)
        # Convert size to kilobytes
        original_image_size_kb = round(original_image_size_bytes / 1024, 2)

        # Process the uploaded file
        processed_image = process_image(file_path)

        # Define processed file name
        processed_filename = 'processed_' + filename
        processed_file_path = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)
            
        # Save processed image
        cv2.imwrite(processed_file_path, processed_image)

        # Get the size of the processed image in bytes
        processed_image_size_bytes = os.path.getsize(processed_file_path)
        # Convert size to kilobytes
        processed_image_size_kb = round(processed_image_size_bytes / 1024, 2)

        # Additional metadata
        upload_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        description = request.form.get('description', '')

        # Insert metadata into the database
        insert_metadata(filename, original_image_size_kb, processed_filename, processed_image_size_kb, upload_date, description)

        # Redirect to index route to display updated data
        return redirect(url_for('index'))

    # Redirect to index route to display updated data
    return redirect(url_for('index'))

@app.route('/processed/<filename>')
def download_file(filename):
    processed_folder = os.path.abspath(app.config['PROCESSED_FOLDER'])
    return send_from_directory(processed_folder, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
