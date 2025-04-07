from flask import Flask, request, send_file, render_template
from gtts import gTTS
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def audiobook1():
    # Check if a file is uploaded
    if 'aufile' not in request.files:
        return "No file uploaded!", 400
    file = request.files['aufile']
    if file.filename == '':
        return "No file selected!", 400
    
    try:
        # Read the content of the uploaded file
        text = file.read().decode('utf-8')  # Decode bytes to string
        if not text.strip():  # Ensure file is not empty or whitespace
            return "The file is empty. No audiobook created."
        
        # Create audio from the text
        tts = gTTS(text)
        
        # Save the audio to a buffer
        buffer = BytesIO()
        tts.write_to_fp(buffer)  # Save directly to the buffer
        buffer.seek(0)  # Reset the buffer pointer to the beginning

        # Return the audio file for download
        return send_file(
            buffer,
            mimetype="audio/mpeg",
            as_attachment=True,
            download_name="audiobook.mp3"
        )
    except Exception as e:
        return f"An error occurred while processing the file: {str(e)}", 500

@app.route('/write', methods=['POST'])
def audiobook2():
    # Check if the form field 'itext' exists
    if 'itext' not in request.form:
        return "No input text!", 400

    # Retrieve the text from the form field
    text = request.form['itext']

    try:
        # Create audio from the text
        tts = gTTS(text)
        
        # Save the audio to a buffer
        buffer = BytesIO()
        tts.write_to_fp(buffer)  # Save directly to the buffer
        buffer.seek(0)  # Reset the buffer pointer to the beginning

        # Return the audio file for download
        return send_file(
            buffer,
            mimetype="audio/mpeg",
            as_attachment=True,
            download_name="audiobook.mp3"
        )
    except Exception as e:
        return f"An error occurred while processing the file: {str(e)}", 500

    
if __name__ == '__main__':
    app.run(debug=True)
