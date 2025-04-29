FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    wget curl unzip build-essential cmake git

RUN git clone https://github.com/OpenWaterAnalytics/EPANET.git && \
    cd EPANET && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make && \
    find . -name "runepanet" -exec cp {} /usr/local/bin/epanet2 \;

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]