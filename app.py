from flask import Flask, request, render_template, send_file, flash, redirect, url_for, jsonify
import os
import tempfile
import shutil
from werkzeug.utils import secure_filename
from pydub import AudioSegment
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.id3 import APIC, ID3, error
import zipfile
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Change this in production
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

ALLOWED_EXTENSIONS = {'flac', 'wav'}
UPLOAD_FOLDER = 'temp_uploads'
CONVERTED_FOLDER = 'temp_converted'

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def attach_cover_art(mp3_file, image_file):
    """Attach cover art to MP3 file"""
    mp3 = MP3(mp3_file, ID3=ID3)
    
    try:
        mp3.add_tags()
    except error:
        pass
    
    with open(image_file, 'rb') as img:
        mp3.tags.add(APIC(
            encoding=3,
            mime='image/jpeg' if image_file.lower().endswith('.jpg') or image_file.lower().endswith('.jpeg') else 'image/png',
            type=3,
            desc='Cover',
            data=img.read()
        ))
    
    mp3.save()

def convert_to_mp3(input_file, output_file, input_extension, image_file=None):
    """Convert audio file to MP3"""
    try:
        # Load audio with pydub
        audio = AudioSegment.from_file(input_file, format=input_extension)
        
        # Fetch metadata for FLAC files
        tags = {}
        if input_extension == "flac":
            try:
                metadata = FLAC(input_file)
                tags = {
                    "title": metadata.get("title", [None])[0],
                    "artist": metadata.get("artist", [None])[0],
                    "album": metadata.get("album", [None])[0],
                    "date": metadata.get("date", [None])[0],
                    "genre": metadata.get("genre", [None])[0],
                }
                # Remove None values
                tags = {k: v for k, v in tags.items() if v is not None}
            except Exception as e:
                print(f"Warning: Could not read metadata from {input_file}: {e}")
        
        # Convert audio to MP3 at 320 kbps
        audio.export(output_file, format="mp3", bitrate="320k", tags=tags)
        
        # Attach cover art if provided
        if image_file and os.path.exists(image_file):
            try:
                attach_cover_art(output_file, image_file)
            except Exception as e:
                print(f"Warning: Could not attach cover art: {e}")
        
        return True, None
    except Exception as e:
        return False, str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        return jsonify({'error': 'No files selected'}), 400
    
    files = request.files.getlist('files')
    
    if not files or all(file.filename == '' for file in files):
        return jsonify({'error': 'No files selected'}), 400
    
    # Create unique session folder
    session_id = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    session_upload_folder = os.path.join(UPLOAD_FOLDER, session_id)
    session_converted_folder = os.path.join(CONVERTED_FOLDER, session_id)
    os.makedirs(session_upload_folder, exist_ok=True)
    os.makedirs(session_converted_folder, exist_ok=True)
    
    uploaded_files = []
    conversion_results = []
    
    # Save uploaded files
    for file in files:
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            if allowed_file(filename) or filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                filepath = os.path.join(session_upload_folder, filename)
                file.save(filepath)
                uploaded_files.append(filename)
    
    # Convert audio files
    for filename in uploaded_files:
        if allowed_file(filename):
            input_file = os.path.join(session_upload_folder, filename)
            base_filename = os.path.splitext(filename)[0]
            output_file = os.path.join(session_converted_folder, f"{base_filename}.mp3")
            
            # Look for cover art with same base name
            image_file = None
            for ext in ['.jpg', '.jpeg', '.png']:
                potential_image = os.path.join(session_upload_folder, base_filename + ext)
                if os.path.exists(potential_image):
                    image_file = potential_image
                    break
            
            # Determine input format
            input_extension = "flac" if filename.lower().endswith(".flac") else "wav"
            
            # Convert file
            success, error_msg = convert_to_mp3(input_file, output_file, input_extension, image_file)
            
            conversion_results.append({
                'filename': filename,
                'success': success,
                'error': error_msg,
                'output_filename': f"{base_filename}.mp3" if success else None
            })
    
    return jsonify({
        'session_id': session_id,
        'results': conversion_results
    })

@app.route('/download/<session_id>')
def download_files(session_id):
    session_converted_folder = os.path.join(CONVERTED_FOLDER, session_id)
    
    if not os.path.exists(session_converted_folder):
        flash('Session not found or expired')
        return redirect(url_for('index'))
    
    # Get all MP3 files in the session folder
    mp3_files = [f for f in os.listdir(session_converted_folder) if f.endswith('.mp3')]
    
    if not mp3_files:
        flash('No converted files found')
        return redirect(url_for('index'))
    
    if len(mp3_files) == 1:
        # Single file - send directly
        return send_file(
            os.path.join(session_converted_folder, mp3_files[0]),
            as_attachment=True,
            download_name=mp3_files[0]
        )
    else:
        # Multiple files - create zip
        zip_filename = f"converted_audio_{session_id}.zip"
        zip_path = os.path.join(session_converted_folder, zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for mp3_file in mp3_files:
                zipf.write(
                    os.path.join(session_converted_folder, mp3_file),
                    mp3_file
                )
        
        return send_file(
            zip_path,
            as_attachment=True,
            download_name=zip_filename
        )

@app.route('/cleanup/<session_id>')
def cleanup_session(session_id):
    """Clean up session files"""
    session_upload_folder = os.path.join(UPLOAD_FOLDER, session_id)
    session_converted_folder = os.path.join(CONVERTED_FOLDER, session_id)
    
    try:
        if os.path.exists(session_upload_folder):
            shutil.rmtree(session_upload_folder)
        if os.path.exists(session_converted_folder):
            shutil.rmtree(session_converted_folder)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
