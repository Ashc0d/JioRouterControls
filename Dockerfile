FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

#xvfb
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg2 ca-certificates \
    python3 python3-pip \
    libglib2.0-0 libx11-xcb1 libxcomposite1 libxcursor1 \
    libxkbcommon0 libxdamage1 libxrandr2 libasound2 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdbus-1-3 libdrm2 libxss1 libxtst6 libxshmfence1 \
    libx11-6 libxext6 libgbm1 fonts-liberation \
    libnss3 libgtk-3-0 libpango-1.0-0 \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Install latest Chrome and ChromeDriver
RUN CHROME_VERSION=$(curl -sS https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json | grep -A2 linux64 | grep -oP 'https://.*?chrome-linux64.zip' | head -n 1 | sed 's|https://storage.googleapis.com/chrome-for-testing-public/||;s|/.*||') && \
    echo "Installing Chrome version $CHROME_VERSION" && \
    wget https://storage.googleapis.com/chrome-for-testing-public/$CHROME_VERSION/linux64/chrome-linux64.zip && \
    wget https://storage.googleapis.com/chrome-for-testing-public/$CHROME_VERSION/linux64/chromedriver-linux64.zip && \
    unzip chrome-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    mv chrome-linux64 /opt/chrome && \
    mv chromedriver-linux64/chromedriver /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver && \
    ln -s /opt/chrome/chrome /usr/bin/google-chrome && \
    rm -rf *.zip chromedriver-linux64


WORKDIR /app
COPY . /app


RUN pip3 install -r requirements.txt

#ENTRYPOINT ["/bin/bash"]
#ENTRYPOINT ["/bin/bash","/bin/xvfb-run", "--auto-servernum", "--server-args=-screen 0 1920x1080x24", "/bin/python3", "main.py"]
ENTRYPOINT ["/bin/python3", "main.py"]
