# TTS (Text-to-Speech) Server (For MacOS) User Manual

## Introduction
This is a Python-based Text-to-Speech (TTS) API server that converts text to audio using the built-in say command on macOS. The server supports various audio formats and voice options.


There's two version of server type.
- api_server.py: initial version/simple.
- api_server2.py: OpenAI speech API compatible.

## Requirements
- only works in MacOSX. this program use OSX's tts model to run.
- need python and flask. (api_server2.py need ffmpeg to convert output file format)

```
pip install flask

# to use api_server2, ffmpeg is needed
brew install ffmpeg

```

- tested on Sonoma 14.2 & python 3.11

## Author
- Jioh L. Jung (with Claude3 opus assisted)
- Test/Sample project to test AI performance.

## LICENSE
MIT License (any use permitted)

# Usage (api_server2.py)
- openAI's speech API compatible.

## Get Available Voices
- Comment: Getting Voices API is added to get installed voices.

- Endpoint: /v1/voices
- Method: GET
- Description: Retrieves the list of available voices.
- Response: JSON array of voice names.
- Example using cURL:

```
curl -X GET "http://localhost:2088/v1/voices"
```

## Convert Text to Speech
- Endpoint: /v1/audio/speech
- Method: POST
- Description: Converts the provided text to speech using the specified voice and audio format.

- Request Body:
 - input (string, required): The text to be converted to speech.
 - voice (string, required): The name of the voice to use for the speech.
 - response_format (string, optional): The desired audio format. Supported formats are: mp3, wav, aac, flac, opus, pcm. Default is mp3.
 - speed (number, optional): The speed of the speech. Value range is 0.25 to 4.0. Default is 1.0.
- Response: The generated audio file in the specified format.

```
curl -X POST "http://localhost:2088/v1/audio/speech" \
     -H "Content-Type: application/json" \
     -d '{"input": "Hello, this is a test.", "voice": "Shelley", "response_format": "mp3"}' \
     -o output.mp3
```

- Note: Replace "Shelley" with the desired voice name obtained from the /v1/voices endpoint.


## Error Handling
The API returns appropriate error responses with corresponding HTTP status codes in case of invalid requests or server errors. The error responses are in JSON format.

# Usage (api_server.py)

## Get the list of voice models
- Endpoint: /models
- Method: GET
- Response: List of voice models (JSON format)

## Convert text to speech
- Endpoint: /tts
- Method: POST
- Request parameters:
  - text (required): The text to be converted
  - voice (optional): The name of the voice model to use
  - speed (optional): The speed of the speech (default: 1.0)
  - sample_rate (optional): The audio sample rate (default: 44100)
 - Response: The generated audio file (audio/x-aiff format)

## Examples
### Get the list of voice models
```
GET /models
```

- Response example:

```
[
  {
    "name": "Alex",
    "lang_code": "en_US"
  },
  {
    "name": "Yuna",
    "lang_code": "ko_KR"
  }
]
```

###  Convert text to speech

```
POST /tts
Content-Type: application/x-www-form-urlencoded

text=Hello&voice=Alex&speed=0.8&sample_rate=22050
```


# Limitations
The server relies on the say command, which is available on macOS. It may not work on other operating systems without modifications.
The available voices and supported formats may vary depending on the system configuration.
# Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.



- Response: The generated audio file (audio/x-aiff format)
