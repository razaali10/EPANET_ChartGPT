FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    curl wget unzip build-essential cmake git && \
    rm -rf /var/lib/apt/lists/*

# Install EPANET CLI
RUN git clone https://github.com/OpenWaterAnalytics/EPANET && \
    cd EPANET && mkdir build && cd build && \
    cmake .. && make && cp bin/runepanet /usr/local/bin/epanet2

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5050

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5050"]
