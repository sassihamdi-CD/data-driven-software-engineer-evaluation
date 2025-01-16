import logging

def get_logger():
    """
    Set up and configure the logger for the project.
    
    This function sets up a logger for the 'pdf_processor' module, which is configured to log messages to the console. 
    The logger is configured with a logging level of INFO or higher, and the log entries are formatted in a human-readable way.

    The logger will be useful for tracking the execution of the PDF processing steps, errors, warnings, and other 
    important events during runtime. It helps with debugging and understanding the flow of the application.

    Returns:
        logger (logging.Logger): A configured logger instance for the pdf_processor module.

    Example:
        # Retrieve the logger
        logger = get_logger()
        
        # Use it for logging messages
        logger.info('This is an informational message')
        logger.error('An error occurred')

    Notes:
        - The logger writes to the console (stdout) using the `StreamHandler`.
        - The log messages will include a timestamp, the logger name, the log level, and the message itself.
        - The log level is set to `INFO` by default. You can adjust this level by modifying the `logger.setLevel` line 
          if a different level (e.g., DEBUG, WARNING, etc.) is preferred.
    """
    
    # Create a logger for the pdf_processor module
    logger = logging.getLogger('pdf_processor')  
    # The logger name helps with distinguishing logs from different parts of the application
    
    logger.setLevel(logging.INFO)  # Set the default logging level to INFO. Adjust if needed to DEBUG, WARNING, etc.
    
    # Create a stream handler to log messages to the console (stdout)
    ch = logging.StreamHandler()  
    ch.setLevel(logging.INFO)  # Set the level for this handler
    
    # Create a log message format and attach it to the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)  # Use the formatter for the console handler
    
    # Add the handler to the logger so it can output the logs
    logger.addHandler(ch)  # Attach the handler to the logger
    
    return logger  # Return the configured logger instance
