import json
import os
from loguru import logger

def save_output(data, output_file: str):
    """
    Saves the processed data to a JSON file.

    This function ensures the directory exists before attempting to write the data to the specified 
    JSON file. If an error occurs during the saving process, it logs the issue.

    Args:
        data (dict or list): The data to be saved to the JSON file.
        output_file (str): The path to the output file where data will be saved.

    Returns:
        None: This function does not return a value.
    """
    # Ensure the directory exists before saving the file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    try:
        # Open the output file in write mode and dump the data into it
        with open(output_file, "w") as f:
            json.dump(data, f, indent=4)  # Pretty-print the JSON data with indentation
        logger.info(f"Data successfully saved to {output_file}")
    except PermissionError:
        # Log a specific error if there are permission issues
        logger.error(f"Permission denied: Unable to save data to {output_file}")
    except Exception as e:
        # Log a general error for any other issues that occur during the saving process
        logger.error(f"Failed to save output due to: {str(e)}")
