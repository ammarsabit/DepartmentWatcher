# Update Checker

A Python project I built while waiting for my department assignment. This script **automatically checks for department release** and **notifies registered users via Telegram** once the department is announced within 15'.

---

## Features

- Logs into student portal using your credentials  
- Periodically polls the portal to check if your department has been assigned  
- Sends a **Telegram notification** to all users who started the bot  
- Keeps track of registered users in a local file (`bot_users.txt`)  
- Lightweight and easy to deploy  

---

## Requirements

- Python 3.10+  
- Libraries:
  ```text
  requests
  pyTelegramBotAPI
  ```
- Telegram Bot token (from [@BotFather](https://t.me/BotFather))

---

## Setup

1. **Clone the repository**
    ```bash
    git clone https://github.com/ammarsabit/DepartmentWatcher.git
    cd DepartmentWatcher
    ```
2. **Install dependencies**
  ```bash
  pip install -r requirements.txt
  ```

3. **Configure environment variables**

Create environment variables for your credentials and bot token. For example, in Linux/macOS:

```bash
export USER_NAME=your_portal_username
export PASSWORD=your_portal_password
export TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

Or on Windows CMD:

```
set USER_NAME=your_portal_username
set PASSWORD=your_portal_password
set TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```
4. **Run the script**


**Live demo running — will notify students on department release**

**Update** - Notified 75+ students in real time when departments were released.
