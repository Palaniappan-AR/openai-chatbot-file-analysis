# Importing Required Packages
import json
import chainlit as cl
from utils import initialize_openai_client, get_functions, get_latest_file_path, process_code_execution

client = initialize_openai_client()

#---------------------------------------------------------------------------------------------------------------------------------------------------------#

# This event is triggered when the chat starts
@cl.on_chat_start
async def on_chat_start():
    # Configuring the language model with a specific temperature and max token length
    llm_config = {
        "model": "gpt-3.5-turbo",  
        "temperature": 0.7,         
        "max_tokens": 1000
    }
    
    # Store the configuration in the user session
    cl.user_session.set("llm_config", llm_config)

#---------------------------------------------------------------------------------------------------------------------------------------------------------#

# This event is triggered when a new message is received
@cl.on_message
async def on_message(message: cl.Message):
    # Retrieve the language model configuration and the latest file path from the user session
    llm_config = cl.user_session.get("llm_config")
    latest_file_path = get_latest_file_path(message, cl.user_session)

    session_context = cl.user_session.get("context", "")  # The context of the ongoing conversation
    additional_info = ""  # Information to add to the prompt, if applicable

    # Check if a file has been uploaded and is a CSV file
    if latest_file_path:
        if not latest_file_path.lower().endswith(".csv"):
            await cl.Message(content="Non CSV files are not accepted for analysis at this moment...").send()
            return
        
        if latest_file_path.lower().endswith(".csv"):
            additional_info = (
                f"If you need to analyze or query data, there's a file uploaded to `{latest_file_path}`. "
                "You can execute Python code to analyze the data based on the user's query. "
                "Pandas, Matplotlib, and Seaborn libraries are available for use. "
                "Additionally, generate any supplementary queries required to complete the analysis."
            )

    # Combine the session context, message content, and additional information to form the complete prompt
    prompt = session_context + "\n\n" + message.content + "\n\n" + additional_info

    try:
        # Call OpenAI API to generate a response based on the prompt
        response = client.chat.completions.create(
            **llm_config,  # Pass the language model configuration
            messages=[
                {"role": "system", "content": "You should only call a mentioned function if it's absolutely necessary for completing the user's request. If the task can be solved without the mentioned function, respond with a direct answer."},
                {"role": "user", "content": prompt.strip()}  # The user's prompt
            ],
            functions=get_functions(),  # Retrieve available function definitions for the model to use
            function_call="auto"  # Allow the model to decide if a function needs to be called
        )

        response_message = response.choices[0].message

        # Log the response message for debugging or further analysis
        # with open("Response.txt", "w") as file:
        #     file.write(str(response_message))

        # Check if a function was called (i.e., the response includes a function call)
        if dict(response_message).get('function_call'):
            function_called = response_message.function_call.name
            function_args = json.loads(response_message.function_call.arguments)

            if function_called == "write_python_code":
                response_message = function_args["code"]

            # UI-Drop down which contains executed python code
            async with cl.Step(name="Python_Code") as step:
                step.output = response_message

            elements, response_message = process_code_execution(response_message)
            
            # Update the session context with the latest message
            cl.user_session.set("context", session_context + "\n\n" + response_message)

            # If there are plot elements (i.e., a plot was generated), send them as a response
            if elements:
                await cl.Message(content="Plot based on user query", elements=elements).send()
            else:
                # Otherwise, send the plain response message
                await cl.Message(content=response_message).send()

        else:
            # If no function was called, just respond with the model's content
            response_message = response_message.content
            await cl.Message(content=response_message).send()

    except Exception as e:
        # If an exception occurs during processing, log it for debugging
        # with open("exception.txt", "w") as file:
        #     file.write(str(e) + "\n" + str(latest_file_path))
        
        # Send a message informing the user about the error
        response_message = f"An error occurred while processing your request. {str(e)}.\nPlease try again."
        await cl.Message(content=response_message).send()
