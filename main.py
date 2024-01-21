import logging
import subprocess
import sys
def install_dependencies():
    """Install necessary dependencies."""
    try:
        # Install required Python packages
        subprocess.run([sys.executable, "-m", "pip", "install", "coloredlogs", "pyttsx3", "Pillow", "pyautogui", "numpy", "pyaudio", "wave", "google-generativeai"])

        # Check and install ffmpeg if not present
        if not check_ffmpeg_installation():
            install_ffmpeg()
    except Exception as e:
        logging.error(f"Error installing dependencies: {e}")

def gemini(prompt):
    import google.generativeai as genai
    youtube_api_key, openai_api_key = get_youtube_and_genai_api_keys()
    genai.configure(api_key=openai_api_key)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

def check_ffmpeg_installation():
    """Check if ffmpeg is installed."""
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except FileNotFoundError:
        return False
    except subprocess.CalledProcessError:
        return False


def install_ffmpeg():
    import platform
    """Install ffmpeg."""
    try:
        system_platform = platform.system()
        if system_platform == "Linux":
            subprocess.run(["sudo", "apt-get", "install", "-y", "ffmpeg"])
        elif system_platform == "Darwin":
            subprocess.run(["brew", "install", "ffmpeg"])
        elif system_platform == "Windows":
            # Add Windows installation command if needed
            pass
        else:
            logging.error("Unsupported platform. Cannot install ffmpeg.")
    except Exception as e:
        logging.error(f"Error installing ffmpeg: {e}")


class ScreenRecorder:

    def __init__(self, filename, fps=30.0):
        self.filename = filename
        self.fps = fps
        self.frames = []
        self.audio_frames = []
        self.is_recording = False
        self.audio_thread = None

    def start(self):
        import cv2
        import numpy as np
        import pyaudio
        import wave
        import threading
        import pyautogui
        self.is_recording = True
        self.audio_thread = threading.Thread(target=self.record_audio)
        self.audio_thread.start()

        while self.is_recording:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.frames.append(frame)

    def stop(self):
        import cv2
        import wave
        import pyaudio
        self.is_recording = False
        self.audio_thread.join()

        fourcc = cv2.VideoWriter_fourcc(*"H264")
        out = cv2.VideoWriter(self.filename, fourcc, self.fps, self.frames[0].shape[:2])

        for frame in self.frames:
            out.write(frame)

        out.release()

        wf = wave.open("temp.wav", "wb")
        wf.setnchannels(1)
        wf.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b"".join(self.audio_frames))
        wf.close()

    def record_audio(self):
        import pyaudio
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

        while self.is_recording:
            data = stream.read(1024)
            self.audio_frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

def get_youtube_and_genai_api_keys():
    import os
    youtube_api_key = os.environ.get("YOUTUBE_API_KEY")
    gemini_api_key = os.environ.get("GENAI_API_KEY")

    if not (youtube_api_key):
        logging.error("YouTube API key. Make sure to set environment variables. Exiting. YOUTUBE_API_KEY")
        raise ValueError("API keys not found.")
    if not (gemini_api_key):
        logging.error("Gemini API key not found. Make sure to set environment variables. Exiting. GENAI_API_KEY")
        raise ValueError("API keys not found.")

    return youtube_api_key, gemini_api_key


class YouTubeAPI:
    OPENAI_API_ENDPOINT = "https://api.openai.com/v1/engines/davinci/completions"
    YOUTUBE_API_ENDPOINT = "https://www.googleapis.com/youtube/v3/channels"
    DEFAULT_THUMBNAIL_PATH = "default_thumbnail.jpg"
    DEFAULT_VIDEO_PATH = "default_video.mp4"
    IMAGE_WIDTH = 1280
    IMAGE_HEIGHT = 720
    FONT_NAME = "arial.ttf"
    VIDEO_START_TIME = "00:00:01"

    def __init__(self, api_key):
        """Initialize YouTubeAPI instance."""
        self.api_key = api_key
        self.default_thumbnail_path = self.DEFAULT_THUMBNAIL_PATH

    def get_previous_video_title(self, channel_id):
        import requests
        """Get the title of the previous video uploaded to the specified YouTube channel."""
        url = f"{self.YOUTUBE_API_ENDPOINT}?part=contentDetails&id={channel_id}&key={self.api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            previous_video_title = data.get("items", [{}])[0].get("contentDetails", {}).get("upload", {}).get("videoId")
            return previous_video_title
        except requests.exceptions.RequestException as err:
            logging.error(f"Error getting previous video title: {err}")
            return None

    def upload_video_details(self, video_title, video_description, video_thumbnail_path):
        import requests
        """Upload video details to YouTube."""
        url = f"{self.YOUTUBE_API_ENDPOINT}?part=snippet,status&key={self.api_key}"
        headers = {"Content-Type": "application/json"}

        with open(video_thumbnail_path, "rb") as thumbnail_file:
            thumbnail_data = thumbnail_file.read()

        data = {
            "snippet": {
                "title": video_title,
                "description": video_description,
                "thumbnails": {
                    "default": {"data": thumbnail_data.decode("utf-8")},
                }
            },
            "status": {
                "privacyStatus": "public"
            }
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            logging.info(f"Video details uploaded successfully: {video_title}")
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred during video details upload: {http_err}")
        except requests.exceptions.RequestException as req_err:
            logging.error(f"Error uploading video details: {req_err}")
        except Exception as err:
            logging.error(f"An unexpected error occurred during video details upload: {err}")

    def upload_video_file(self, video_file_path):
        import requests
        """Upload video file to YouTube."""
        url = f"{self.YOUTUBE_API_ENDPOINT}?part=snippet,status&key={self.api_key}"
        headers = {"Content-Type": "application/json"}

        files = {"file": open(video_file_path, "rb")}

        try:
            response = requests.post(url, headers=headers, files=files)
            response.raise_for_status()
            logging.info(f"Video file uploaded successfully: {video_file_path}")
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred during video file upload: {http_err}")
        except requests.exceptions.RequestException as req_err:
            logging.error(f"Error uploading video file: {req_err}")
        except Exception as err:
            logging.error(f"An unexpected error occurred during video file upload: {err}")

    def upload_video(self, video_title, video_description, video_thumbnail_path, video_file_path):
        """Upload video to YouTube."""
        self.upload_video_details(video_title, video_description, video_thumbnail_path)
        self.upload_video_file(video_file_path)

    def process_video_script_section(self, video_script_section):
        """Process a video script section."""
        explanation = video_script_section["explanation"]
        command = video_script_section["command"]

        logging.info(f"Processing video script section: {explanation}")
        text_to_speech(explanation)

        logging.info(f"Executing command: {command}")
        success = open_terminal_and_run_command(command)

        if not success:
            logging.warning(f"Error executing command. Skipping section: {explanation}")

    def generate_video_thumbnail(self, video_script_sections):
        import logging
        from PIL import Image, ImageDraw, ImageFont
        """Generate a video thumbnail."""
        if not video_script_sections:
            logging.error("Empty video script sections. Cannot generate thumbnail.")
            return None

        image = Image.new("RGB", (self.IMAGE_WIDTH, self.IMAGE_HEIGHT), (255, 255, 255))

        title = video_script_sections[0]["explanation"]
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(self.FONT_NAME, 32)
        draw.text((10, 10), title, font=font)

        first_frame = video_script_sections[1]["command"]

        try:
            subprocess.run(["ffmpeg", "-i", first_frame, "-ss", self.VIDEO_START_TIME, "-vframes", "1", self.DEFAULT_THUMBNAIL_PATH], check=True)
            thumbnail_image = Image.open(self.DEFAULT_THUMBNAIL_PATH)
            image.paste(thumbnail_image, (10, 50))
        except subprocess.CalledProcessError as e:
            logging.error(f"Error generating video thumbnail: {e}")
            logging.warning("Cannot continue with default thumbnail.")
            return None

        return image

def configure_logging():
    import coloredlogs
    """Configure logging settings."""
    coloredlogs.install(level="INFO")

def genai_prompt(video_title):
    """Generate a prompt for gemini."""
    prompt = f"""
    Generate a video script in sections. Each section should be in JSON format and include an explanation and a command. video's title is "{video_title}". Please respond with the sections in the following format:

    {{
        "sections": [
            {{"explanation": "Explanation 1", "command": "Command 1"}},
            {{"explanation": "Explanation 2", "command": "Command 2"}},
            ...
        ]
    }}
    """
    return gemini(prompt)

def generate_video_script_sections(genai_response):
    """Generate video script sections from ChatGPT response."""
    sections = []

    if isinstance(genai_response, dict):
        # Assuming 'sections' is the key containing the relevant text data
        paragraphs = genai_response.get('sections', '').split("\n")

        for paragraph in paragraphs:
            section = {}

            explanation, _, command = paragraph.partition(".")

            section["explanation"] = explanation.strip()
            section["command"] = command.strip()

            sections.append(section)

    return sections


def text_to_speech(text):
    import pyttsx3
    """Convert text to speech."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def run_terminal_command(command):
    """Run a command in the terminal."""
    try:
        subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running command: {e}")
        return False

def open_terminal_and_run_command(command):
    import platform
    """Open terminal and run a command."""
    system_platform = platform.system()
    if system_platform == "Linux":
        terminal_command = f"xterm -e {command}"
    elif system_platform == "Windows":
        terminal_command = f"start cmd /c {command}"
    else:
        logging.error("Unsupported platform. Cannot open terminal.")
        return False

    return run_terminal_command(terminal_command)


def start_screen_recording():
    recorder = ScreenRecorder("default_video.mp4")
    recorder.start()

def main():
    import json
    import os
    import requests
    import logging
    from PIL import Image
    install_dependencies()
    """Main function."""
    configure_logging()
    logging.info("Starting the script...")
    try:
        youtube_api_key, openai_api_key = get_youtube_and_genai_api_keys()
        youtube_api = YouTubeAPI(youtube_api_key)
        #channel_id = input("Enter your YouTube channel ID: ").strip()
        channel_id = "UC5N_8t5SzEyJrTx1bC66Kpw"

        if not channel_id:
            logging.warning("Invalid channel ID. Exiting.")
            return
        previous_video_title = youtube_api.get_previous_video_title(channel_id)
        title = gemini(f"my previous video is {previous_video_title} generate a title for which related to previous video. please give me only title")
        discription=gemini(f"write discription for this video {title}")

        sections = genai_prompt(title)

        if not title or discription:
            logging.warning("Invalid ChatGPT response. Continuing with default.")
            gemini_response = {"title": "Default Title", "description": "Default Description"}

        video_script_sections = generate_video_script_sections(type(sections))
        recorder = ScreenRecorder("output.mp4")
        recorder.start()
        for section in video_script_sections:
            youtube_api.process_video_script_section(section)
        recorder.stop()

        video_thumbnail = youtube_api.generate_video_thumbnail(video_script_sections)

        if not video_thumbnail:
            logging.warning("Thumbnail not generated. Using default thumbnail.")
            video_thumbnail = Image.new("RGB", (youtube_api.IMAGE_WIDTH, youtube_api.IMAGE_HEIGHT), (255, 255, 255))

        thumbnail_path = input(f"Enter the path to save the generated thumbnail (or press Enter to use default: {YouTubeAPI.DEFAULT_THUMBNAIL_PATH}): ").strip() or YouTubeAPI.DEFAULT_THUMBNAIL_PATH

        video_thumbnail.save(thumbnail_path)

        video_path = input(f"Enter the path to the video file (or press Enter to use default: {YouTubeAPI.DEFAULT_VIDEO_PATH}): ").strip() or YouTubeAPI.DEFAULT_VIDEO_PATH
        youtube_api.upload_video(title, discription, thumbnail_path, video_path)

    except KeyboardInterrupt:
        logging.debug("Script interrupted by user. Performing cleanup.")
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")

    finally:
        # Cleanup temporary files
        if os.path.exists(YouTubeAPI.DEFAULT_THUMBNAIL_PATH):
            os.remove(YouTubeAPI.DEFAULT_THUMBNAIL_PATH)
        if os.path.exists(YouTubeAPI.DEFAULT_VIDEO_PATH):
            os.remove(YouTubeAPI.DEFAULT_VIDEO_PATH)

if __name__ == "__main__":
    main()
