import logging

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


class PDFProcessingError(Exception):
    """
    Custom exception raised when there is an error during PDF processing.

    This exception is used to signal errors encountered while processing PDF files,
    such as invalid file format, corrupted files, or any unexpected issues during
    the extraction process.

    Attributes:
        message (str): A description of the error encountered during PDF processing.
    """

    def __init__(self, message: str) -> None:
        """
        Initializes the PDFProcessingError with a custom error message.

        Args:
            message (str): The description of the error encountered during PDF processing.
        """
        super().__init__(message)  # Call the parent class constructor with the error message

    def __str__(self):
        return f"PDFProcessingError: {self.args[0]}"  # Return a custom string representation


class FileNotFoundErrorCustom(Exception):
    """
    Custom exception raised when a file is not found.

    This exception is raised when a file specified for processing does not exist
    or cannot be located on the system.

    Attributes:
        file_path (str): The path of the file that could not be found.
        message (str): A description of the error encountered.
    """

    def __init__(self, file_path: str) -> None:
        """
        Initializes the FileNotFoundErrorCustom with the file path and custom error message.

        Args:
            file_path (str): The path of the file that was not found.
        """
        self.file_path = file_path  # Store the path of the file that caused the error
        self.message = f"File not found: {file_path}"  # Create a custom error message
        super().__init__(self.message)  # Call the parent class constructor with the custom message

    def __str__(self):
        return f"FileNotFoundErrorCustom: {self.message}"  # Custom string representation


class PDFReadError(Exception):
    """
    Custom exception raised when an error occurs while reading a PDF file.

    This exception is used to signal issues encountered during the process of reading
    a PDF file, such as permission errors or file corruption.

    Attributes:
        file_path (str): The path of the PDF file that failed to be read.
        message (str): A description of the error encountered while reading the PDF file.
    """

    def __init__(self, file_path: str, message: str) -> None:
        """
        Initializes the PDFReadError with the file path and custom error message.

        Args:
            file_path (str): The path of the problematic PDF file.
            message (str): A description of the error encountered while reading the file.
        """
        self.file_path = file_path  # Store the path of the problematic PDF file
        self.message = f"Error reading PDF file {file_path}: {message}"  # Custom error message
        super().__init__(self.message)  # Call the parent class constructor with the custom message

    def __str__(self):
        return f"PDFReadError: {self.message}"  # Custom string representation


class FileSaveError(Exception):
    """
    Custom exception raised when there is an error saving data to a file.

    This exception is raised when the process of saving extracted data to a file fails,
    such as due to permissions issues or insufficient disk space.

    Attributes:
        file_path (str): The path of the file where the data could not be saved.
        message (str): A description of the error encountered while saving data.
    """

    def __init__(self, file_path: str, message: str) -> None:
        """
        Initializes the FileSaveError with the file path and custom error message.

        Args:
            file_path (str): The path of the file where data could not be saved.
            message (str): A description of the error encountered while saving data.
        """
        self.file_path = file_path  # Store the path of the file where the data was supposed to be saved
        self.message = f"Error saving data to file {file_path}: {message}"  # Custom error message
        super().__init__(self.message)  # Call the parent class constructor with the custom message

    def __str__(self):
        return f"FileSaveError: {self.message}"  # Custom string representation


def handle_malformed_pdf_error(pdf_file: str, error_message: str) -> None:
    """
    Handles errors related to malformed PDF files.

    Args:
        pdf_file (str): The PDF file where the error occurred.
        error_message (str): The error message describing the issue.
    """
    logger.error(f"Malformed PDF error in file {pdf_file}: {error_message}")
    raise PDFProcessingError(f"Malformed PDF file: {pdf_file}. Error: {error_message}")


def handle_invalid_content_error(pdf_file: str, content: str) -> None:
    """
    Handles errors related to invalid content extracted from a PDF.

    Args:
        pdf_file (str): The PDF file where the invalid content was extracted.
        content (str): The content that was deemed invalid.
    """
    logger.error(f"Invalid content extracted from file {pdf_file}: {content}")
    raise PDFProcessingError(f"Invalid content in PDF: {pdf_file}")

class InvalidContentError(Exception):
    """
    Custom exception raised when invalid content is found in a PDF.

    This exception is used when the extracted content from a PDF is considered invalid,
    such as when the content doesn't meet the expected format or requirements.

    Attributes:
        file_path (str): The path of the file where the invalid content was found.
        content (str): A description of the invalid content.
    """

    def __init__(self, file_path: str, content: str) -> None:
        """
        Initializes the InvalidContentError with the file path and invalid content description.

        Args:
            file_path (str): The path of the PDF where invalid content was found.
            content (str): A description of the invalid content.
        """
        self.file_path = file_path  # Store the path of the file with invalid content
        self.content = content  # Store the invalid content
        self.message = f"Invalid content in PDF file {file_path}: {content}"  # Custom message
        super().__init__(self.message)  # Call the parent class constructor
    
    def __str__(self):
        return f"InvalidContentError: {self.message}"  # Custom string representation
