import os  # Import os for file path manipulation
import re  # Import for regular expressions to extract sections
import json  # Import JSON for saving data in a structured format
from utils.file_utils import get_pdf_files  # Import the function for fetching PDF files
from utils.pdf_utils import save_output  # Import function for saving processed output
from config import INPUT_DIR, OUTPUT_FILE  # Import directory and file constants from config
from logger import get_logger  # Import logger configuration
from utils.file_utils import read_pdfs_concurrently  # Import the new concurrent read function
from PyPDF2 import PdfReader  # For extracting metadata

# Set up the logger for the application
logger = get_logger()

def clean_text(content):
    """
    Cleans the extracted content by removing unnecessary whitespace and special characters.
    """
    content = content.strip()  # Remove leading/trailing whitespace
    content = re.sub(r'\s+', ' ', content)  # Replace multiple spaces with a single space
    content = re.sub(r'[^\x00-\x7F]+', ' ', content)  # Remove non-ASCII characters
    return content

def extract_metadata(pdf_file):
    """
    Extracts metadata from a PDF file, such as title, author, and creation date.
    """
    try:
        reader = PdfReader(pdf_file)
        metadata = reader.metadata
        title = metadata.get('/Title', 'Unknown Title')
        author = metadata.get('/Author', 'Unknown Author')
        creation_date = metadata.get('/CreationDate', 'Unknown Date')
        return {'title': title, 'author': author, 'creation_date': creation_date}
    except Exception as e:
        logger.warning(f"Error extracting metadata from {pdf_file}: {e}")
        return {'title': 'Unknown Title', 'author': 'Unknown Author', 'creation_date': 'Unknown Date'}

def process_pdfs():
    """
    Processes all PDF files in the specified input directory and saves the extracted content to an output file.
    
    This function:
    1. Retrieves all PDF files from the input directory specified by INPUT_DIR.
    2. Extracts content from each PDF using `read_pdfs_concurrently` for concurrent reading.
    3. Saves the extracted content to the output file specified by OUTPUT_FILE.
    
    If no PDF files are found or if no content is extracted, appropriate log messages are generated.

    Logs:
        - WARNING if no PDFs are found in the directory.
        - INFO for each PDF file being processed.
        - WARNING if no content is extracted from a file.
        - WARNING if no content is available to save.

    Returns:
        None
    """
    
    # Step 1: Fetch all PDF files from the input directory
    pdf_files = get_pdf_files(INPUT_DIR)

    # If no PDFs were found, log a warning and return early
    if not pdf_files:
        logger.warning("No PDF files found to process in directory: %s", INPUT_DIR)
        return

    all_data = []  # List to hold the extracted data from each PDF

    # Step 2: Process each PDF file concurrently
    pdf_contents = read_pdfs_concurrently(pdf_files)  # Efficient concurrent reading of PDFs

    # Step 3: Process the extracted content
    for pdf_file, content in pdf_contents:
        logger.info(f"Processing file: {pdf_file}")  # Log the file being processed
        
        # Clean the extracted content
        content = clean_text(content)

        # If content was successfully extracted, store it in the all_data list
        if content:
            metadata = extract_metadata(pdf_file)  # Extract metadata
            # Structure the data with metadata and sections
            structured_data = {
                "file_name": os.path.basename(pdf_file),
                "metadata": metadata,
                "content": content,
                "sections": {
                    "header": content[:100],  # Example: First 100 characters as a header (customize as needed)
                    "body": content[100:],    # Rest as body (you could break it further)
                    "footer": content[-100:],  # Example: Last 100 characters as footer (customize as needed)
                }
            }
            all_data.append(structured_data)
            logger.info(f"Content extracted and structured from {pdf_file}")
        else:
            logger.warning(f"No content extracted from file: {pdf_file}")

    # Step 4: Save the output if data was extracted, otherwise log a warning
    if all_data:
        try:
            logger.info(f"Saving extracted data for {len(all_data)} files to output.")
            save_output(all_data, OUTPUT_FILE)  # Save the extracted content to the output file
            logger.info("Processed PDFs and saved content successfully.")
        except Exception as e:
            logger.error(f"Error while saving output to {OUTPUT_FILE}: {e}")
    else:
        logger.warning("No content extracted to save.")

if __name__ == "__main__":
    # Run the PDF processing function when the script is executed
    process_pdfs()
