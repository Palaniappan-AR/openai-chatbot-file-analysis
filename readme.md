# OpenAI Chatbot with File Analysis

This repository contains a Python-based chatbot built using the Chainlit framework and OpenAI's GPT-3.5 API. The bot is designed to interact with users and assist with analyzing uploaded CSV files. It supports Python code execution for data analysis tasks and visualizations using libraries such as Pandas and Matplotlib.

## Screenshots of the app
**Note: I added a chainlit - dropdown feature to help frontend users better understand the thought process and code used by GPT in the backend.**
<img width="958" alt="1" src="https://github.com/user-attachments/assets/35e054f7-8716-4c21-b4b4-9ed13b21757e">
<img width="378" alt="2" src="https://github.com/user-attachments/assets/7c7b42a8-6274-48dd-b195-650292537d69">
<img width="383" alt="3" src="https://github.com/user-attachments/assets/8bf7bcdd-a4a6-4d80-9534-82ac930e2a79">
<img width="382" alt="4" src="https://github.com/user-attachments/assets/6b6e9482-e1da-4936-ab25-b81e200efae8">

## Features

- **CSV File Upload**: Users can upload CSV files for analysis. The bot can process and analyze data using Python.
- **Python Code Execution**: The bot can execute Python code to perform data analysis and generate visualizations.
- **Dynamic Response Generation**: Based on the user's query, the bot generates responses by calling appropriate functions or providing direct answers.
- **Integration with OpenAI GPT-3.5**: The bot leverages GPT-3.5 for conversational capabilities and intelligent responses.

## Prerequisites

You will also need to set up the following environment variables for connecting to OpenAI's API:

- `azure_endpoint`: Your OpenAI API Azure endpoint.
- `openai_api_key`: Your OpenAI API key.
- `api_version`: The version of the API you want to use.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Palaniappan-AR/openai-chatbot-file-analysis.git
   cd openai-chatbot-file-analysis

2. **Create a .env file** in the root directory of the project and add the following environment variables:

    azure_endpoint = "your-openai-api-azure-endpoint"<br />
    openai_api_key = "your-openai-api-key"<br />
    api_version = "your-api-version"<br />

3. Build the Docker image:

    docker build -t openai-chatbot .

4. Run the Docker container, making sure to pass the .env file as environment variables:

    docker run --env-file .env -p 8000:8000 openai-chatbot

This will start the chatbot in the Docker container, and it will be accessible at **http://localhost:8000**
