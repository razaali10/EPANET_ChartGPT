FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl wget unzip build-essential cmake git && \
    rm -rf /var/lib/apt/lists/*

# Clone and build EPANET CLI
RUN git clone https://github.com/OpenWaterAnalytics/EPANET && \
    cd EPANET && mkdir build && cd build && \
    cmake .. && make && \
    cp /EPANET/build/bin/runepanet /usr/local/bin/epanet2

# Set working directory
WORKDIR /app

# Copy source code
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose FastAPI port
EXPOSE 5050

# Start the API
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5050"]



