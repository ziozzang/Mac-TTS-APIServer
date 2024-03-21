from flask import Flask, request, send_file, jsonify
from io import BytesIO
import subprocess
import tempfile
import os
import re

app = Flask(__name__)

@app.route('/models', methods=['GET'])
def get_models():
    # Execute 'say -v ?' command to get the list of voices
    output = subprocess.check_output(['say', '-v', '?']).decode('utf-8')

    # Parse the voice list to extract names and language codes
    models = []
    for line in output.split('\n'):
        if line.strip():
            lang_code_match = re.search(r'[a-z]{2}_[A-Z]{2}', line)
            lang_code = lang_code_match.group() if lang_code_match else ''
            if not lang_code:
                continue
            name = line.split(lang_code)[0].strip()
            models.append({'name': name, 'lang_code': lang_code})

    return jsonify(models)

@app.route('/tts', methods=['POST'])
def text_to_speech():
    # Get text and voice options from the POST request
    text = request.form['text']
    voice = request.form.get('voice')
    speed = float(request.form.get('speed', 1.0))
    sample_rate = int(request.form.get('sample_rate', 44100))

    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix='.aiff', delete=False) as temp_file:
        temp_filename = temp_file.name

    # Generate the command based on the voice options
    command = ['say', text, '-o', temp_filename]

    # Process options
    if voice:
        command.extend(['-v', voice])
    if speed != 1.0:
        command.extend(['-r', str(speed)])
    if sample_rate != 44100:
        command.extend(['--data-format=LEI16@' + str(sample_rate)])
    print('REQ>', command)

    # Execute the command by passing the text through a pipe
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, stderr_output = process.communicate(text.encode('utf-8'))

    if process.returncode != 0:
        print(f"Error: {stderr_output.decode('utf-8')}")
        os.remove(temp_filename)  # Delete the temporary file
        return "Error occurred during TTS conversion", 500

    # Read the audio data from the temporary file
    with open(temp_filename, 'rb') as file:
        audio_data = file.read()

    # Delete the temporary file
    os.remove(temp_filename)

    # Convert the audio data to a BytesIO object
    audio_io = BytesIO(audio_data)

    # Send the WAV file as a response
    return send_file(audio_io, mimetype='audio/x-aiff', as_attachment=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2088, debug=False)