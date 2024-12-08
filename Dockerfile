FROM python:3.12.6-slim

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH
WORKDIR $HOME/app
COPY --chown=user . .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["chainlit", "run", "main.py", "-w", "--host", "0.0.0.0"]