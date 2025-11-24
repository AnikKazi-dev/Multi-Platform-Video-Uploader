# Multi-Platform Video Uploader

A powerful desktop application to upload short-form videos (Shorts, Reels, TikToks) to multiple platforms simultaneously with a single click.

![App Screenshot](screenshot.png)

## Features

- **Multi-Platform Support**: Upload to YouTube Shorts, Instagram Reels, Facebook Reels, and TikTok.
- **Simultaneous Uploads**: Runs uploads in parallel to save time.
- **Browser Automation**: Uses Selenium with `undetected-chromedriver` to bypass bot detection and handle complex login flows (YouTube, Facebook, TikTok).
- **API Integration**: Uses `instagrapi` for robust Instagram uploads.
- **Persistent Sessions**: Saves your login sessions (cookies) locally so you don't have to log in every time.
- **GUI Interface**: Clean and easy-to-use interface built with `customtkinter`.

## Prerequisites

- Python 3.8 or higher
- Google Chrome installed

## Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/AnikKazi-dev/Multi-Platform-Video-Uploader.git
    cd Multi-Platform-Video-Uploader
    ```

2.  **Install Dependencies**
    It is recommended to use a virtual environment (like Conda or venv).
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configuration**
    - Rename `config.example.json` to `config.json`.
    - Open `config.json` and update the fields:
        - **Instagram**: Add your username and password.
        - **Others**: The app primarily uses browser automation for YouTube, Facebook, and TikTok, so you will log in interactively the first time.

## Usage

1.  **Run the Application**
    You can use the provided batch file for easy launching:
    ```bash
    run.bat
    ```
    Or run with Python directly:
    ```bash
    python main.py
    ```

2.  **First Time Setup (Browser Login)**
    - When you run an upload for YouTube, Facebook, or TikTok for the first time, a browser window will open.
    - **Log in** to your account manually in that window.
    - The app will save your session profile locally (`selenium_*_profile` folders).
    - Future uploads will use these saved sessions automatically.

3.  **Uploading**
    - Select your video file.
    - Enter a caption.
    - Check the platforms you want to upload to.
    - Click **"Upload to All Selected"**.
    - The app will open browsers for each platform and handle the upload process automatically.

## Notes

- **Facebook**: The app navigates to the Reels creation page. Ensure you are logged into the correct page/profile.
- **YouTube**: Uploads as "Public" by default.
- **Instagram**: Uses the private API. Use with caution and avoid spamming to prevent account flags.

## License

[MIT](LICENSE)
