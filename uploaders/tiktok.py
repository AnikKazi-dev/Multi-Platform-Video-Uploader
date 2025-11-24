import time
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def upload_tiktok(video_path, caption, config):
    # Config can contain 'cookies_path' or similar
    
    options = uc.ChromeOptions()
    options.add_argument("--disable-popup-blocking")
    
    # Use a persistent profile to save login state
    user_data_dir = os.path.join(os.getcwd(), "selenium_tiktok_profile")
    options.add_argument(f"--user-data-dir={user_data_dir}")

    driver = None
    try:
        driver = uc.Chrome(options=options)
        driver.maximize_window()
        
        driver.get("https://www.tiktok.com/upload?lang=en")
        
        # Check if logged in (look for upload frame or login button)
        # This is a naive check. Better to let user log in if needed.
        print("Please log in to TikTok in the browser if not already logged in.")
        
        # Wait for the file input to be present. If it takes too long, maybe we are at login screen.
        # We'll give the user 60 seconds to log in manually if needed.
        try:
            file_input = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
            )
        except:
            return "Error: Could not find upload input. Did you log in?"

        # Upload file
        file_input.send_keys(os.path.abspath(video_path))
        
        # Wait for upload to complete (progress bar)
        # This is tricky. We'll wait for the "Post" button to be clickable.
        
        # Set Caption
        # TikTok's caption editor is a contenteditable div usually
        try:
            caption_div = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'public-DraftEditor-content')]"))
            )
            caption_div.send_keys(caption)
        except:
            print("Could not set caption automatically")

        # Click Post
        # This selector changes often.
        try:
            post_btn = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Post']"))
            )
            post_btn.click()
        except:
             return "Error: Could not find Post button"

        # Wait for success message
        time.sleep(10) 
        return "Success (Check browser to confirm)"

    except Exception as e:
        return f"Failed: {str(e)}"
    finally:
        if driver:
            # driver.quit()
            pass
