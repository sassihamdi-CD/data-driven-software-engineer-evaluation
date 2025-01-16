import os

# Define the base directory for the project
BASE_DIR = os.getcwd()
"""
BASE_DIR is the base directory where the project is being executed. This is typically the current working 
directory of the project or script.

Example:
>>> BASE_DIR
'/home/user/project_folder'
"""

# Define the directory where PDF files are stored
INPUT_DIR = os.path.join(BASE_DIR, 'pdfs')  
"""
INPUT_DIR specifies the directory that contains the input PDF files. These are the files that will be processed 
by the application.

Example:
>>> INPUT_DIR
'/home/user/project_folder/pdfs'

Notes:
- If the 'pdfs' folder does not exist in the base directory, you may need to create it manually or adjust the path 
  according to your project structure.
"""

# Define the directory where output files will be saved
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')  
"""
OUTPUT_DIR defines the directory where the processed output files (e.g., JSON, extracted data) will be saved.

Example:
>>> OUTPUT_DIR
'/home/user/project_folder/output'

Notes:
- The 'output' directory is created automatically if it does not exist.
"""

# Define the path to the output JSON file
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'output.json')  
"""
OUTPUT_FILE specifies the full path to the output JSON file where the final results (e.g., extracted content) 
will be stored.

Example:
>>> OUTPUT_FILE
'/home/user/project_folder/output/output.json'

Notes:
- This file will be created if it does not already exist.
"""

# Ensure that the output directory exists, if not, create it
os.makedirs(OUTPUT_DIR, exist_ok=True)  
"""
os.makedirs is used to ensure that the output directory exists. If the directory does not exist, it will be created.
The 'exist_ok=True' parameter ensures that no error is raised if the directory already exists.

Example Usage:
>>> os.makedirs(OUTPUT_DIR, exist_ok=True)

Notes:
- This is an essential step to avoid errors when saving files to the 'output' directory.
"""

