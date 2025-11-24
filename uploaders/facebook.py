import time
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def upload_facebook(video_path, caption, config):
    options = uc.ChromeOptions()
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")
    
    # Persistent profile
    user_data_dir = os.path.join(os.getcwd(), "selenium_facebook_profile")
    options.add_argument(f"--user-data-dir={user_data_dir}")

    driver = None
    try:
        driver = uc.Chrome(options=options)
        driver.maximize_window()
        driver.get("https://www.facebook.com")
        
        print("Facebook: Please log in if needed. Waiting for home page...")
        
        # Wait for login (check for home icon, create post, or nav bar)
        try:
            WebDriverWait(driver, 120).until(
                EC.presence_of_element_located((By.XPATH, 
                    "//div[@aria-label='Create a post'] | "
                    "//span[text()='What\'s on your mind?'] | "
                    "//div[@aria-label='Account controls and settings'] | "
                    "//div[@role='banner'] | "
                    "//div[@aria-label='Facebook']"
                ))
            )
            print("Facebook: Login verified (or home page loaded).")
        except:
            print("Facebook: Warning - Could not verify login automatically. Proceeding anyway...")

        # Navigate to Reels Create
        print("Facebook: Navigating to Reels creation page...")
        driver.get("https://www.facebook.com/reels/create")
        
        # Upload Video
        print("Facebook: Uploading video file...")
        try:
            # Look for file input
            file_input = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
            )
            file_input.send_keys(os.path.abspath(video_path))
        except:
            return "Error: Could not find Reels file input."

        # Wait for upload processing (Next button becomes clickable)
        print("Facebook: Waiting for video to process...")
        try:
            # Click Next (First time - usually goes to trim/edit)
            next_btn = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Next'] | //span[text()='Next']"))
            )
            driver.execute_script("arguments[0].click();", next_btn)
            
            time.sleep(2)
            
            # Click Next (Second time - usually goes to caption)
            # Sometimes there is only one Next, sometimes two.
            # We can try clicking Next again if it exists.
            try:
                next_btn_2 = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Next'] | //span[text()='Next']"))
                )
                driver.execute_script("arguments[0].click();", next_btn_2)
            except:
                pass # Maybe only one next button needed
                
        except:
            return "Error: Could not find Next button."

        # Caption
        print("Facebook: Setting caption...")
        try:
            caption_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Describe your reel...'] | //div[@contenteditable='true']"))
            )
            caption_box.send_keys(caption)
        except:
            print("Could not set caption (might be skipped)")

        # Publish
        print("Facebook: Clicking Publish...")
        try:
            publish_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Publish'] | //span[text()='Publish']"))
            )
            driver.execute_script("arguments[0].click();", publish_btn)
        except:
            return "Error: Could not find Publish button"

        # Wait for completion
        print("Facebook: Waiting for upload to finish...")
        time.sleep(15)
        
        return "Success (Check browser)"

    except Exception as e:
        return f"Failed: {str(e)}"
    finally:
        if driver:
            time.sleep(5)
            # driver.quit()
