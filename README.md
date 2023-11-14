# Video Automation Toolkit

## Overview
The Video Automation Toolkit is a Python script (`main.py`) designed to streamline the process of creating and uploading videos to YouTube. This automation tool integrates with OpenAI's GPT (ChatGPT) for script generation and the YouTube API for uploading video details, thumbnails, and files.

## Features
1. **Dependency Installation:**
   - Installs required Python packages and checks/installs `ffmpeg`.

2. **Screen Recording:**
   - Captures screen frames using `pyautogui` and records audio with `pyaudio`.
   
3. **YouTube API Integration:**
   - Manages YouTube API interactions for uploading video details, thumbnails, and files.
   - Retrieves the title of the previous video from a specified channel.

4. **ChatGPT Interaction:**
   - Utilizes ChatGPT to generate a video script based on a prompt.
   - Converts script sections to speech using `pyttsx3`.
   - Executes terminal commands and opens a terminal for specific actions.

5. **Logging and Configuration:**
   - Configures logging settings for improved visibility.

6. **Cleanup:**
   - Removes temporary files after script execution.

## Usage
1. Clone the repository.
2. Install dependencies using `python main.py`.
3. Run `main.py` and follow the prompts to enter the YouTube channel ID and paths for saving generated files.
4. The script will generate a video script using ChatGPT, process it, and upload the video to YouTube.

## Requirements
- Python 3.x
- YouTube API key
- OpenAI API key
- Internet connection

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/video-automation-toolkit.git
   cd video-automation-toolkit
   python main.py
'
## Configuration
Set your YouTube API key and OpenAI API key as environment variables (YOUTUBE_API_KEY and OPENAI_API_KEY).

## Acknowledgments
Thanks to the developers of OpenAI's GPT and YouTube API for their valuable contributions.
