import pyautogui  
import schedule  
import time  
import os  
from datetime import datetime  
import zipfile  
  
# Define the directory to save screenshots  
screenshot_dir = 'screenshots'  
  
# Ensure the screenshot directory exists  
if not os.path.exists(screenshot_dir):  
    os.makedirs(screenshot_dir)  
  
# Function to capture and save a screenshot  
def capture_screenshot():  
    # Get the current time to use as the filename  
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  
    filename = f"{current_time}.png"  
    filepath = os.path.join(screenshot_dir, filename)  
      
    # Take a screenshot and save it  
    pyautogui.screenshot(filepath)  
    print(f"Screenshot saved as {filename}")  
  
# Scheduled task to capture a screenshot  
def job():  
    capture_screenshot()  
  
# Function to zip screenshots at the end of each day  
def zip_screenshots():  
    today_date = datetime.now().strftime("%Y-%m-%d")  
    zip_filename = f"{today_date}_screenshots.zip"  
    zip_filepath = os.path.join(screenshot_dir, zip_filename)  
      
    with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:  
        for root, dirs, files in os.walk(screenshot_dir):  
            for file in files:  
                if file.startswith(today_date):  
                    file_path = os.path.join(root, file)  
                    zipf.write(file_path, os.path.relpath(file_path, screenshot_dir))  
    print(f"Zipped screenshots into {zip_filename}")  
  
# Schedule the zip_screenshots function to run at the end of each day  
schedule.every().day.at("23:59").do(zip_screenshots)  
  
# Schedule the job function to run every 10 seconds  
schedule.every(10).seconds.do(job)  
  
# Run all scheduled tasks continuously  
while True:  
    schedule.run_pending()  
    time.sleep(1)