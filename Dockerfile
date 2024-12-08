FROM python:3.12.6-slim
 
RUN useradd -m -u 1000 chatbot
 
USER chatbot
 
ENV HOME=/home/chatbot \
    PATH=/home/chatbot/.local/bin:$PATH
 
WORKDIR $HOME/app
 
COPY --chown=chatbot . .
 
RUN pip install -r requirements.txt
 
EXPOSE 8000
 
CMD ["chainlit", "run", "main.py", "-w", "--host", "0.0.0.0"]
