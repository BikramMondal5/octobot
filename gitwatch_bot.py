import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    JobQueue,
)

# -------------------------
# Load tokens
# -------------------------
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

# Store last check time for each user being tracked
last_checked = {}


# -------------------------
# Helper: Get recent repos
# -------------------------
def get_recent_repos(username: str, since_time: datetime):
    url = f"https://api.github.com/users/{username}/repos?sort=pushed&per_page=30"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        return None, f"❌ Error fetching repos: {response.json().get('message', 'Unknown error')}"

    repos = response.json()
    recent_repos = []

    for repo in repos:
        pushed_at = datetime.strptime(repo["pushed_at"], "%Y-%m-%dT%H:%M:%SZ")
        if pushed_at > since_time:  # Only new pushes
            recent_repos.append(
                {
                    "name": repo["name"],
                    "url": repo["html_url"],
                    "pushed_at": pushed_at,
                    "language": repo.get("language"),
                }
            )

    return recent_repos, None


# -------------------------
# Background Job
# -------------------------
async def check_github(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    username = job.data["username"]
    chat_id = job.chat_id
    last_time = job.data["last_time"]

    repos, error = get_recent_repos(username, last_time)

    if error:
        await context.bot.send_message(chat_id, error)
        return

    if repos:
        msg = f"🚀 New activity by *{username}*:\n\n"
        for repo in repos:
            msg += f"🔹 [{repo['name']}]({repo['url']})\n"
            msg += f"   📅 Pushed: {repo['pushed_at']}\n"
            msg += f"   📝 Language: {repo['language']}\n\n"

        await context.bot.send_message(chat_id, msg, parse_mode="Markdown")

        # Update last checked time
        job.data["last_time"] = datetime.utcnow()


# -------------------------
# Commands
# -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome! Use /watch <github_username> to start tracking.\n"
        "Use /stop to stop tracking."
    )


async def watch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Please provide a GitHub username.\nExample: `/watch torvalds`")
        return

    username = context.args[0]
    chat_id = update.effective_chat.id

    # Start tracking from now
    last_checked[chat_id] = datetime.utcnow()

    # Cancel existing job if already tracking
    current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    for job in current_jobs:
        job.schedule_removal()

    # Create a new job
    context.job_queue.run_repeating(
        check_github,
        interval=120,  # check every 2 minutes
        first=5,  # first run after 5 seconds
        chat_id=chat_id,
        name=str(chat_id),
        data={"username": username, "last_time": last_checked[chat_id]},
    )

    await update.message.reply_text(f"✅ Started tracking `{username}` every 2 minutes.")


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    jobs = context.job_queue.get_jobs_by_name(str(chat_id))

    if not jobs:
        await update.message.reply_text("ℹ️ No active tracking found.")
        return

    for job in jobs:
        job.schedule_removal()

    await update.message.reply_text("🛑 Stopped tracking GitHub activity.")


# -------------------------
# Main Entry
# -------------------------
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Explicitly create job_queue
    job_queue = app.job_queue  

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("watch", watch))
    app.add_handler(CommandHandler("stop", stop))

    app.run_polling()



if __name__ == "__main__":
    main()
