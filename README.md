# TTS (Text-to-Speech) Server (For MacOS) User Manual

## Introduction
This document explains how to use the TTS server. This server provides the functionality to convert text into speech.

## Requirements
- only works in MacOSX. this program use OSX's tts model to run.
- need python and flask.
```
pip install flask
```

- tested on Sonoma 14.2 & python 3.11

## Author
- Jioh L. Jung (with Claude3 opus assisted)
- Test/Sample project to test AI performance.

## LICENSE
MIT License (any use permitted)

## Usage

### Get the list of voice models
- Endpoint: /models
- Method: GET
- Response: List of voice models (JSON format)

### Convert text to speech
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

- Response: The generated audio file (audio/x-aiff format)
