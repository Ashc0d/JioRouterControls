
## 📶 Jio Router Reboot Automation
This script automates logging into your Jio router’s admin panel and reboots the device to ensure stability after long uptime sessions.
(for now it does reboot. I can expand it, if I am in mood.)

---

### 🔐 `.env` Format

Create a `.env` file in the same directory as `main.py` or you can hardcode in 'main.py'

```
ROUTER_URL=http://192.168.29.1
USERNAME=your_router_username
PASSWORD=your_router_password
```

> ⚠️ Keep this file secure. Do **not** commit `.env` to version control.

---

### 📦 Requirements

* Python 3.9+
* Google Chrome or Chromium
* ChromeDriver compatible with your Chrome version
* Linux system (headless capable)

Install dependencies:

```bash
pip install -r requirements.txt
```

Install additional system packages (Ubuntu/Debian):

```bash
sudo apt update && sudo apt install -y \
  chromium-browser \
  chromium-driver \
  fonts-liberation \
  libatk-bridge2.0-0 libatk1.0-0 libcups2 libdbus-1-3 \
  libgdk-pixbuf2.0-0 libnspr4 libnss3 libx11-xcb1 \
  libxcomposite1 libxdamage1 libxrandr2 libxss1 xdg-utils
```

---

### 🚀 How to Run

```bash
python main.py
```

This will:

1. Log in to the router admin panel
2. Navigate to the **Maintenance** section
3. Click the **Reboot** button and accept the confirmation alert

---

### ⏰ Automating with `cron`

To schedule this script to run every day at **3:00 AM**, edit your crontab:

```bash
crontab -e
```

Add:

```bash
0 3 * * * /usr/bin/python3 /path/to/main.py >> /var/log/jio-reboot.log 2>&1
```

---

### 🛡️ Notes

* Runs in **headless mode** (no GUI required).
* Script handles alert dialogs and router protections.
* All interaction is automated using Selenium.

---
### 🧪 Development Setup (Optional: Using `.venv`)

To isolate dependencies and avoid polluting your system Python environment, create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies inside the virtual environment:

```bash
pip install -r requirements.txt
```

> If you're using an IDE like VS Code, it will automatically detect the `.venv` folder if placed in the root of the project.

To deactivate when you're done:

```bash
deactivate
```

To remove the virtual environment later (optional):

```bash
rm -rf .venv
```

---

### 📦 Build the Docker Image (For Headless deployment)

```bash
docker build -t jio-router-control .
```
### 🚀 Run the Container

To run the container with environment variables:

```bash
docker run --rm \
  -e USERNAME=your_router_username \
  -e PASSWORD=your_router_password \
  -e ROUTER_URL=http://192.168.29.1 \
  jio-router-control
```

* `USERNAME`: Your router's login username
* `PASSWORD`: Your router's login password
* `ROUTER_URL`: The base URL of your router (e.g., `http://192.168.29.1`)

---

