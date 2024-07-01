# Automated YouTube Video Creator

Automated-YouTube-Video-Creator is a Python script designed to streamline the process of generating YouTube video scripts, recording the screen, and uploading videos to YouTube. This project leverages various Python libraries and APIs to automate the creation of engaging video content.

## Features

- **YouTube API Integration:** Interacts with the YouTube API to retrieve previous video details and upload new video information.
- **Gemini Integration:** Utilizes the Google Generative AI library (Gemini) to generate video scripts based on prompts provided to ChatGPT.
- **Screen Recording:** Implements a screen recording feature to capture visual content for the generated video.
- **Text-to-Speech:** Converts text-based explanations into speech using the pyttsx3 library.
- **Thumbnail Generation:** Generates video thumbnails using the PIL library and FFmpeg.

## Prerequisites

Ensure you have the following before running the script:

- Python installed on your machine.
- API keys for YouTube and Gemini (Google Generative AI).

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/Automated-YouTube-Video-Creator.git
    cd Automated-YouTube-Video-Creator
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up API keys:
    - Obtain a YouTube API key from the [YouTube Developer Console](https://console.developers.google.com/).
    - Get a Gemini API key from [Gemini](https://gemini.google.com/).

    Set these keys as environment variables or directly in the script.

## Usage

1. Run the main script:
    ```bash
    python main.py
    ```

2. Follow the prompts to input your YouTube channel ID and receive automated assistance in generating and uploading a video.

## Customization

Feel free to customize the script to meet your specific needs or extend its functionality. You may want to explore additional features, tweak the video script generation process, or enhance error handling.

## Contributing

Contributions are welcome! If you have suggestions, feature requests, or bug reports, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

---

**Note:** Make sure to adhere to YouTube's policies and guidelines when using automated tools for content creation and uploading.

Project by Likith