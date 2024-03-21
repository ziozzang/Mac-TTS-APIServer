from flask import Flask, request, send_file, jsonify
from io import BytesIO
import subprocess
import tempfile
import os
import re

app = Flask(__name__)

@app.route('/v1/voices', methods=['GET'])
def get_voices():
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


@app.route('/v1/audio/speech', methods=['POST'])
def text_to_speech():
    # Get text and voice options from the POST request
    data = request.get_json()
    text = data.get('input')
    voice = data.get('voice')
    speed = data.get('speed', 1.0)
    response_format = data.get('response_format', 'mp3')

    # Validate the input
    if not text:
        return jsonify({'error': 'Input text is required'}), 400
    if not voice:
        return jsonify({'error': 'Voice is required'}), 400
    if speed < 0.25 or speed > 4.0:
        return jsonify({'error': 'Invalid speed value. Speed must be between 0.25 and 4.0'}), 400
    if response_format not in ['mp3', 'opus', 'aac', 'flac', 'wav', 'pcm']:
        return jsonify({'error': 'Invalid response format'}), 400

    # Create a temporary file for the AIFF output
    with tempfile.NamedTemporaryFile(suffix='.aiff', delete=False) as temp_aiff_file:
        temp_aiff_filename = temp_aiff_file.name

    # Generate the command based on the voice options
    command = ['say', text, '-o', temp_aiff_filename]

    # Process options
    if voice:
        command.extend(['-v', voice])
    if speed != 1.0:
        command.extend(['-r', str(speed)])

    print('REQ>', command)

    # Execute the command by passing the text through a pipe
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, stderr_output = process.communicate(text.encode('utf-8'))

    if process.returncode != 0:
        print(f"Error: {stderr_output.decode('utf-8')}")
        os.remove(temp_aiff_filename)  # Delete the temporary AIFF file
        return jsonify({'error': 'Error occurred during TTS conversion'}), 500

    # Create a temporary file for the converted output
    with tempfile.NamedTemporaryFile(suffix='.' + response_format, delete=False) as temp_output_file:
        temp_output_filename = temp_output_file.name

    # Convert the AIFF file to the requested format using ffmpeg
    ffmpeg_command = ['ffmpeg', '-i', temp_aiff_filename, '-y', temp_output_filename]
    subprocess.run(ffmpeg_command, check=True)

    # Read the audio data from the temporary output file
    with open(temp_output_filename, 'rb') as file:
        audio_data = file.read()

    # Delete the temporary files
    os.remove(temp_aiff_filename)
    os.remove(temp_output_filename)

    # Convert the audio data to a BytesIO object
    audio_io = BytesIO(audio_data)

    # Determine the MIME type based on the response format
    mime_type = {
        'mp3': 'audio/mpeg',
        'opus': 'audio/ogg',
        'aac': 'audio/aac',
        'flac': 'audio/flac',
        'wav': 'audio/wav',
        'pcm': 'audio/pcm'
    }.get(response_format)

    # Send the audio file as a response
    return send_file(audio_io, mimetype=mime_type, as_attachment=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2088, debug=False)
