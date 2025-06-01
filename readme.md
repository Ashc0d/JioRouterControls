
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

# Using Systemd to manage automation

This section outlines the setup for running the `jio-router-control` Docker container using systemd timers and services on a Linux system.

## Overview

The setup consists of two systemd unit files:

1.  **`jio-router-control.timer`**: This timer unit is responsible for triggering the service unit at a scheduled time.
2.  **`jio-router-control.service`**: This service unit defines how to run the `jio-router-control` Docker container.

## Unit Files

### 1. `jio-router-control.timer`

This file defines when the `jio-router-control.service` should be executed.

**Location:** `/etc/systemd/system/jio-router-control.timer`

**Content:**

```ini
[Unit]
Description=Run jio-router-control daily at 3 AM

[Timer]
OnCalendar=*-*-* 03:00:00
Unit=jio-router-control.service

[Install]
WantedBy=timers.target
```

**Explanation:**

*   **`[Unit]` Section:**
    *   `Description`: A human-readable description of the timer.
*   **`[Timer]` Section:**
    *   `OnCalendar=*-*-* 03:00:00`: This is the core of the timer. It specifies that the associated unit should be run daily at 3:00:00 AM. The format is `DayOfWeek Year-Month-Day Hour:Minute:Second`. Asterisks (`*`) act as wildcards.
    *   `Unit=jio-router-control.service`: Specifies the service unit that this timer will activate.
*   **`[Install]` Section:**
    *   `WantedBy=timers.target`: This ensures that the timer is enabled and started when the system boots into a state where timers are active.

### 2. `jio-router-control.service`

This file defines the actual command to run the Docker container.

**Location:** `/etc/systemd/system/jio-router-control.service`

**Content:**

```ini
[Unit]
Description=Run jio-router-control Docker container
After=network.target docker.service
Requires=docker.service

[Service]
Type=oneshot
User=root
ExecStart=/usr/bin/docker run --rm --env-file=/etc/jio-router.env -v /etc/timezone:/etc/timezone:ro -v /etc/localtime:/etc/localtime:ro ashc0d/jio-router-control
StandardOutput=append:/var/log/jio-router-control.log
StandardError=append:/var/log/jio-router-control.log
```

**Explanation:**

*   **`[Unit]` Section:**
    *   `Description`: A human-readable description of the service.
    *   `After=network.target docker.service`: Specifies that this service should start after the network is up and the Docker service is running.
    *   `Requires=docker.service`: Declares a dependency on the Docker service. If `docker.service` is not active, this service will not start.
*   **`[Service]` Section:**
    *   `Type=oneshot`: Indicates that this service performs a single task and then exits. Systemd will consider the service active until the `ExecStart` command finishes.
    *   `User=root`: Specifies that the command should be run as the `root` user. This is often necessary for Docker operations.
    *   `ExecStart=/usr/bin/docker run --rm --env-file=/etc/jio-router.env -v /etc/timezone:/etc/timezone:ro -v /etc/localtime:/etc/localtime:ro ashc0d/jio-router-control`: This is the command that will be executed.
        *   `/usr/bin/docker run`: The Docker command to run a container.
        *   `--rm`: Automatically removes the container when it exits.
        *   `--env-file=/etc/jio-router.env`: Loads environment variables from the specified file.
        *   `-v /etc/timezone:/etc/timezone:ro`: Mounts the system's timezone file into the container (read-only) to ensure correct time.
        *   `-v /etc/localtime:/etc/localtime:ro`: Mounts the system's local time file into the container (read-only) for the same reason.
        *   `ashc0d/jio-router-control`: The name of the Docker image to run.
    *   `StandardOutput=append:/var/log/jio-router-control.log`: Appends the standard output of the command to the specified log file.
    *   `StandardError=append:/var/log/jio-router-control.log`: Appends the standard error output of the command to the specified log file.

## Environment File Setup

The `jio-router-control.service` requires an environment file located at `/etc/jio-router.env` to store sensitive information like credentials and the router URL.

**1. Create the Environment File:**

Create the file `/etc/jio-router.env` with the following content, replacing the placeholder values with your actual credentials and router IP:

```env
USERNAME=your_router_username
PASSWORD=your_router_password
ROUTER_URL=http://192.168.29.1
```

**2. Set Permissions:**

It is crucial to restrict access to this file as it contains sensitive credentials. Set the permissions to `600` (read and write for the owner only).

Open your terminal and run the following command:

```bash
sudo chmod 600 /etc/jio-router.env
```

You may also need to ensure the owner is `root` if it isn't already (though creating it with `sudo` usually handles this):

```bash
sudo chown root:root /etc/jio-router.env
```

## Enabling and Starting the Timer

After creating both unit files and the environment file:

1.  **Reload systemd daemon:**
    ```bash
    sudo systemctl daemon-reload
    ```

2.  **Enable the timer to start on boot:**
    ```bash
    sudo systemctl enable jio-router-control.timer
    ```

3.  **Start the timer immediately:**
    ```bash
    sudo systemctl start jio-router-control.timer
    ```

## Verifying the Setup

*   **Check timer status:**
    ```bash
    sudo systemctl list-timers | grep jio-router-control
    ```
    This should show `jio-router-control.timer` and when it's next scheduled to run.

*   **Check service status (after it has run):**
    ```bash
    sudo systemctl status jio-router-control.service
    ```

*   **Check logs:**
    ```bash
    sudo cat /var/log/jio-router-control.log
    ``` 
    or through continuous monitoring
* 
    ```bash
    sudo tail -f /var/log/jio-router-control.log
    ```

## Disabling the Timer

If you need to stop the scheduled task:

1.  **Stop the timer:**
    ```bash
    sudo systemctl stop jio-router-control.timer
    ```

2.  **Disable the timer from starting on boot:**
    ```bash
    sudo systemctl disable jio-router-control.timer
    ```


