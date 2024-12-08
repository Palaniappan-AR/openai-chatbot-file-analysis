# OpenAI Chatbot with File Analysis

This repository contains a Python-based chatbot built using the Chainlit framework and OpenAI's GPT-3.5 API. The bot is designed to interact with users and assist with analyzing uploaded CSV files. It supports Python code execution for data analysis tasks and visualizations using libraries such as Pandas, Matplotlib, and Seaborn.

## Screenshots of the app
<img width="958" alt="1" src="https://github.com/user-attachments/assets/35e054f7-8716-4c21-b4b4-9ed13b21757e">

## Features

- **CSV File Upload**: Users can upload CSV files for analysis. The bot can process and analyze data using Python.
- **Python Code Execution**: The bot can execute Python code to perform data analysis and generate visualizations.
- **Dynamic Response Generation**: Based on the user's query, the bot generates responses by calling appropriate functions or providing direct answers.
- **Integration with OpenAI GPT-3.5**: The bot leverages GPT-3.5 for conversational capabilities and intelligent responses.

## Prerequisites

You will also need to set up the following environment variables for connecting to OpenAI's API:

- `azure_endpoint`: Your OpenAI API Azure endpoint (if you're using Azure).
- `openai_api_key`: Your OpenAI API key.
- `api_version`: The version of the API you want to use (e.g., "v1").

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/openai-chatbot-file-analysis.git
   cd openai-chatbot-file-analysis

2. **Create a .env file** in the root directory of the project and add the following environment variables:

    azure_endpoint = "your-openai-api-azure-endpoint"
    openai_api_key = "your-openai-api-key"
    api_version = "your-api-version"

3. Build the Docker image:

    docker build -t openai-chatbot .

4. Run the Docker container, making sure to pass the .env file as environment variables:

    docker run --env-file .env -p 8000:8000 openai-chatbot

This will start the chatbot in the Docker container, and it will be accessible at **http://localhost:8000**
