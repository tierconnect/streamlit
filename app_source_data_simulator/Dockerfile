FROM python:3.8.13

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /src/requirements.txt
RUN pip3 install -r /src/requirements.txt
COPY *.py /src
ENTRYPOINT ["streamlit", "run", "/src/app.py", "--server.port=8080", "--server.address=0.0.0.0"]
