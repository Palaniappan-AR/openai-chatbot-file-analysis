import os
import re
import io
import contextlib
import chainlit as cl
import matplotlib.pyplot as plt
from openai import AzureOpenAI

def initialize_openai_client():
    """Initialize and return the Azure OpenAI client."""

    return AzureOpenAI(
        azure_endpoint=os.getenv('azure_endpoint'),  # Fetch endpoint from environment variable
        api_key=os.getenv('openai_api_key'),  # Fetch API key from environment variable
        api_version=os.getenv('api_version')
    )

def get_functions():
    # This function returns a function definition, specifying the expected structure of the code generation request
    return [
        {
            "name": "write_python_code",  # Name of the function
            "description": "Generates Python code for the requested task.",  # Function description
            "parameters": {
                "type": "object",  # Object type to define parameters
                "properties": {
                    "code": {
                        "type": "string",  # The parameter 'code' will be a string
                        "description": "The generated Python code for the task."
                    }
                }
            }
        }
    ]

def get_latest_file_path(message, user_session):
    """Returns the latest file path if available."""
    # This function checks if there is a file attached to the current message.
    if message.elements:
        latest_file_path = message.elements[0].path
        user_session.set("latest_file", latest_file_path)  # Store file path in session
    else:
        # If no file is attached, retrieve the last file path saved in the session
        latest_file_path = user_session.get("latest_file")
    return latest_file_path

def process_code_execution(response_message):    
    """Process and execute the code from the response message."""
    
    if "plot" in response_message:
        response_message = response_message.replace("plt.show()", "").strip()
        exec(response_message)  # Execute the plot code
        fig = plt.gcf() 
        elements = [cl.Pyplot(figure=fig, display="inline")]  # Prepare the plot for display
        return elements, response_message  # Return plot elements and the code

    else:
        # Ensure that the code has a print statement to show output
        if "print" not in response_message:
            lines = response_message.strip().split("\n")
            last_line = lines[-1]
            lines[-1] = f"print({last_line})"  # Wrap the last line in a print statement
            response_message = "\n".join(lines)
        
        output_buffer = io.StringIO()  # Create a buffer to capture the printed output
        with contextlib.redirect_stdout(output_buffer):  # Redirect stdout to the buffer
            exec(response_message)  # Execute the code
        
        exec_output = output_buffer.getvalue()  # Get the captured output
        response_message = f"\n\nExecution result:\n{exec_output}"  # Format the output with a label
        return None, response_message  # No plot to return, only execution result in response message
