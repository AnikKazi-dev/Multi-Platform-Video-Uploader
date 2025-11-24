import time
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def upload_youtube(video_path, caption, config):
    options = uc.ChromeOptions()
    options.add_argument("--disable-popup-blocking")
    
    # Persistent profile
    user_data_dir = os.path.join(os.getcwd(), "selenium_youtube_profile")
    # UC handles user-data-dir a bit differently, but this should work for persistence
    options.add_argument(f"--user-data-dir={user_data_dir}")
    
    # Keep browser open
    # options.add_experimental_option("detach", True) # Not always needed with UC but good practice if using standard selenium

    driver = None
    try:
        # version_main allows to specify chrome version if needed, usually auto is fine
        driver = uc.Chrome(options=options)
        driver.get("https://studio.youtube.com")
        
        print("YouTube: Waiting for dashboard to load...")
        
        # Wait for "Create" button or Login
        # If not logged in, user will be on login page. We wait.
        try:
            # Try multiple selectors for the Create button
            create_btn = WebDriverWait(driver, 120).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='create-icon'] | //*[@id='create-button'] | //*[text()='Create']"))
            )
        except:
            return "Error: Could not find 'Create' button. Did you log in?"

        print("YouTube: Clicking 'Create' button...")
        # Use JS click to avoid interception
        driver.execute_script("arguments[0].click();", create_btn)
        
        # Click "Upload videos"
        try:
            upload_videos_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//tp-yt-paper-item//div[contains(text(), 'Upload videos')] | //*[text()='Upload videos']"))
            )
            driver.execute_script("arguments[0].click();", upload_videos_btn)
        except:
             return "Error: Could not find 'Upload videos' option."

        print("YouTube: Selecting video file...")
        # File Input
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )
        file_input.send_keys(os.path.abspath(video_path))

        print("YouTube: Waiting for upload to process...")
        # Wait for upload to process (Title box appears)
        title_box = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='title-textarea']//div[@contenteditable='true']"))
        )
        
        # Set Title (Clear and Type)
        # YouTube auto-fills filename. We'll just leave it or append caption if needed.
        # Let's try to set the description instead, as title is mandatory and pre-filled.
        
        print("YouTube: Setting description...")
        # Description
        try:
            desc_box = driver.find_element(By.XPATH, "//div[@id='description-textarea']//div[@contenteditable='true']")
            desc_box.send_keys(caption)
        except:
            pass

        # Click Next (Kids option)
        # We need to select "No, it's not made for kids" usually
        print("YouTube: Selecting 'Not made for kids'...")
        try:
            not_kids_radio = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "VIDEO_MADE_FOR_KIDS_NOT_MFK"))
            )
            not_kids_radio.click()
        except:
            pass # Maybe already selected

        # Click Next multiple times until "Visibility" tab
        print("YouTube: Navigating to Visibility tab...")
        for _ in range(3):
            try:
                next_btn = driver.find_element(By.ID, "next-button")
                next_btn.click()
                time.sleep(2)
            except:
                break

        # Visibility: Public
        print("YouTube: Setting visibility to Public...")
        try:
            public_radio = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "PUBLIC"))
            )
            public_radio.click()
        except:
             return "Error: Could not find Public visibility option."

        # Publish
        print("YouTube: Publishing...")
        done_btn = driver.find_element(By.ID, "done-button")
        done_btn.click()

        # Wait for "Video published" dialog
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Video published')] | //h1[contains(text(), 'Video uploaded')]"))
        )
        
        return "Success"

    except Exception as e:
        return f"Failed: {str(e)}"
    finally:
        if driver:
            time.sleep(5) # Give a moment to see result
            # driver.quit() # Keep browser open
