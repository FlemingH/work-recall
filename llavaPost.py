import base64  
from pathlib import Path  
import requests
import json

def find_images_in_folder(folder_path, extensions=('.png')):  
    """  
    Traverse the given folder and return a list of Path objects to all image files.  
  
    :param folder_path: The path to the folder to traverse, as a string or Path object.  
    :param extensions: A tuple of image file extensions to consider, defaults to ('.png').  
    :return: A list of Path objects to image files.  
    """  
    image_files = []  
    folder_path = Path(folder_path)  
    for file in folder_path.rglob('*'):  
        if file.suffix.lower() in extensions:  
            image_files.append(file)  
    return image_files 

def image_to_base64(image_path):  
    """  
    Convert an image file to a Base64 encoded string.  
      
    :param image_path: The path to the image file.  
    :return: A string containing the Base64 encoded image data.  
    """  
    with open(image_path, "rb") as image_file:  # Open the image file in binary read mode  
        encoded_string = base64.b64encode(image_file.read())  # Encode the binary data to Base64  
    return encoded_string.decode('utf-8')  # Decode the bytes to a UTF-8 string  
  
# Usage example
folder_path = 'screenshots'
images = find_images_in_folder(folder_path)
for image in images:
    base64_encoded_image = image_to_base64(image)

    ollama_url = ''

    ollama_data_obj = {  
        'model': "llava",  
        'prompt': "Playing as a personal assistant, you are now looking at a person's computer desktop information, analyzing the information on the desktop and extracting useful content",  
        'images': [base64_encoded_image]  
    }

    headers = {'Content-Type': 'application/json'} 

    response = requests.post(ollama_url, json=ollama_data_obj, headers=headers) 
  
    multi_line_response = response.text.splitlines() 

    full_response = ""    
    for line in multi_line_response:
        ollama_line = json.loads(line)
        if not ollama_line['done']:
            full_response += ollama_line['response']
    
    print(full_response)

