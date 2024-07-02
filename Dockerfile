FROM python:3.12-slim

WORKDIR /app

COPY . .

# Essentials for installing the llama-cpp-python library
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    cmake

RUN pip install --upgrade pip && pip3 install --quiet -r requirements.txt

# Download llama 2 binaries
RUN huggingface-cli download TheBloke/Llama-2-7B-GGUF llama-2-7b.Q4_K_M.gguf --local-dir .

EXPOSE 8501

# Check that the program is running
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Command used to run the program
# testing:
ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.runOnSave=true"]
# development:
# ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.runOnSave=true"]
