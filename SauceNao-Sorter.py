from saucenao_api import SauceNao 
import os
import random
import requests
import time
from saucenao_api.errors import UnknownServerError, LongLimitReachedError

# Define source folders
source_folder = r"path_to_source_folder"
renamed_folder = r"path_to_renamed_folder"
no_Match = r"path_to_no_Match_Folder"

# Initialize SauceNao API
sauce = SauceNao('xxxx')  # Replace 'xxxx' with your actual API key

# Get the number of files to process
file_count = sum(1 for _ in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, _)))
print("Items to scan:", file_count)

# Process each file
for _ in range(file_count):
    rand_file = random.choice(os.listdir(source_folder))  # Choose a random file from the source folder
    print("File Sent -", rand_file)
    
    # Check if the file is a JPG or PNG
    if rand_file.lower().endswith(('.jpg', '.jpeg', '.png')):
        try:
            # Search for similar images using SauceNao
            with open(os.path.join(source_folder, rand_file), 'rb') as f:  # Open the file in binary mode
                results = sauce.from_file(f)  # Get search results from SauceNao
            
            # Handle results
            file_addon = ""  # Initialize an empty string for file tags
            for result in results:
                for url in result.urls:
                    if "https://danbooru.donmai.us/" in url and result.similarity > 85:
                        # Retrieve tags from Danbooru if similarity score is high enough
                        link = url.replace("/post/show/", "/posts/") + ".json"
                        response = requests.get(link)
                        json_data = response.json()
                        # !!IMPORTANT!! - Add/Remove the # to the line that you DONT want, as they share a Variable if both are active the character name will be overwriten by the copyright
                        file_addon = json_data.get("tag_string_character", "")  # Get Character Name(s) tags
                        file_addon = json_data.get("tag_string_Copyright", "")  # Get Copyright tags
                        break
            
            # Rename and move files
            if file_addon:
                # Remove special characters from file tags
                file_addon = file_addon.replace("/", "").replace(":", "").replace("*", "").replace("?", "").replace('"', '').replace("<", "").replace(">", "").replace("|", "")
                # Rename and move the file to the renamed folder
                os.replace(os.path.join(source_folder, rand_file), os.path.join(renamed_folder, file_addon + "_" + rand_file))
                print("Renaming File and moving")
            else:
                # Move the file to the folder for files with no match
                os.replace(os.path.join(source_folder, rand_file), os.path.join(no_booru_folder, rand_file))
                print("No matches")
        
        except UnknownServerError:
            print("Unknown server error occurred. Skipping processing for this file.")
        
        except LongLimitReachedError:
            print("24 hours limit reached. Pausing script execution for 24 hours.")
            time.sleep(86400)  # Sleep for 24 hours (24 * 60 * 60 seconds)
        
        print("-----")
    
    else:
        # If the file is not a JPG or PNG, print a message and skip processing
        print("File format not supported. Skipping processing.")
    
    # Add a sleep to prevent exceeding API limits
    time.sleep(30)  # Sleep for 30 seconds between each file request

print("Finished")
