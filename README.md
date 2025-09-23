# 🤖📡 GitBot-Tracker

A Telegram bot that tracks GitHub activity in real-time. Perfect for teams, group projects, and organizations to stay updated on commits, merges, and pull requests.

## 🌟 Features
* 🔍 Track any GitHub username  
* 📦 Detect repositories pushed **after you start watching**  
* 📝 Get details like repo name, link, primary language & push time  
* 🌿 See the **branch name** of recent commits  
* 🔀 Detect and notify when branches are **merged** (with date & time)  
* 📥 Stay informed on **pull request activity**  
* ⏱️ Continuous monitoring with automatic updates  
* 🛑 Start and stop tracking easily with bot commands  

## 🛠️ Technologies Used
* **Python** 🐍 – Core logic  
* **python-telegram-bot** 📲 – For Telegram Bot API  
* **Requests** 🌐 – To fetch data from GitHub API  
* **GitHub REST API** 🔧 – Source of all activity data  

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/BikramMondal5/GitHub-Activity-Tracker-Bot.git
```
2. Navigate to the project directory:
```bash
cd GitHub-Activity-Tracker-Bot
```
3. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows
```
4. Install dependencies:
```bash
pip install -r requirements.txt
```
5. Create a `.env` file and add your tokens:
```bash
TELEGRAM_TOKEN=your_telegram_bot_token
GITHUB_TOKEN=your_github_personal_access_token
```
6. Run the bot:
```bash
python gitwatch_bot.py
```

## 🤝 Contribution

**Got ideas? or Found a bug? 🐞**
- Open an issue or submit a pull request — contributions are always welcome!

## 📜 License

This project is licensed under the `MIT License`.

