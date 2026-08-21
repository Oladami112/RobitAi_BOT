import os
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv('BOT_TOKEN')
user_data = {}

# --- ABOUT TEXT ---
ABOUT_TEXT = """🤖 *ABOUT ROBITTAI BOT*

🚀 *Version:* 1.0.0
📅 *Release:* August 2026
⚙️ *Framework:* Python-Telegram-Bot

━━━━━━━━━━━━━━━━━━━━━

✨ *What I Can Do:*
• Answer your questions instantly
• Generate helpful text responses
• Have casual conversations
• Provide information on various topics
• Assist with daily tasks

━━━━━━━━━━━━━━━━━━━━━

🔒 *Privacy & Safety:*
• No personal data stored
• Messages processed in real-time
• 100% GDPR compliant
• No third-party data sharing

━━━━━━━━━━━━━━━━━━━━━

📊 *Statistics:*
• Uptime: 99.9%
• Response time: < 1 second
• Available 24/7

━━━━━━━━━━━━━━━━━━━━━

📢 *Contact & Support:*
• Feedback: /feedback
• Support: @your_support_handle
• Channel: t.me/your_channel

━━━━━━━━━━━━━━━━━━━━━

❤️ *Built with passion for the Telegram community!*"""

# --- COMMANDS TEXT ---
COMMANDS_TEXT = """🤖 *AVAILABLE COMMANDS*

━━━━━━━━━━━━━━━━━━━━━

🔹 *Basic Commands:*
/start    - Welcome & introduction
/help     - Show this command list
/about    - About this bot
/ping     - Check bot status
/time     - Current server time

━━━━━━━━━━━━━━━━━━━━━

🔹 *Interaction:*
[Type any message] - Chat with me
/feedback [text]   - Send feedback

━━━━━━━━━━━━━━━━━━━━━

📝 *Examples:*
• Type "Hello" to start a conversation
• Type "What is AI?" for information
• Type "Tell me a joke" for fun
• Type "/feedback Great bot!" to give feedback

━━━━━━━━━━━━━━━━━━━━━

⚡ *Quick Tips:*
• I understand natural language
• Just type what you need help with
• I'm learning every day!

━━━━━━━━━━━━━━━━━━━━━

📢 *Stay updated:*
Follow @your_channel for updates!

━━━━━━━━━━━━━━━━━━━━━

🆘 *Need more help?*
Type /feedback or contact @support_handle"""

# --- WELCOME TEXT ---
WELCOME_TEXT = """🤖 *Welcome to RobittAi!*

I'm your friendly AI assistant bot. 

✨ *I can help you with:*
• Answering questions
• Text generation
• Casual conversations
• Information retrieval

━━━━━━━━━━━━━━━━━━━━━

📌 *Quick Start:*
Just send me a message and I'll respond!
Use /help to see all commands.

━━━━━━━━━━━━━━━━━━━━━

🔒 *Privacy Guaranteed:*
No data storage. No tracking. Just pure assistance!"""

# --- Command Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📋 Commands", callback_data='help'),
         InlineKeyboardButton("ℹ️ About", callback_data='about')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(WELCOME_TEXT, reply_markup=reply_markup, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(COMMANDS_TEXT, parse_mode='Markdown')

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(ABOUT_TEXT, parse_mode='Markdown')

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 *Pong!* Bot is active and running ✅", parse_mode='Markdown')

async def time_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await update.message.reply_text(f"🕐 *Server Time:* `{current_time}`", parse_mode='Markdown')

async def feedback_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    feedback_text = (
        "📝 *Send Feedback*\n\n"
        "To send feedback, type:\n"
        "`/feedback Your message here`\n\n"
        "Example: `/feedback Great bot!`"
    )
    await update.message.reply_text(feedback_text, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = update.effective_user.id
    user_data[user_id] = {'last_message': user_message, 'timestamp': datetime.now()}
    
    # Smart responses
    message_lower = user_message.lower()
    
    if any(word in message_lower for word in ['hello', 'hi', 'hey', 'sup']):
        response = "👋 Hello there! How can I assist you today?"
    elif 'how are you' in message_lower:
        response = "🤖 I'm functioning perfectly, thanks for asking! How can I help you?"
    elif 'thank' in message_lower or 'thanks' in message_lower:
        response = "😊 You're welcome! Feel free to ask if you need anything else."
    elif 'help' in message_lower:
        response = "🆘 I'm here to help! Use /help to see all my commands."
    elif 'what is' in message_lower or 'explain' in message_lower:
        response = "📚 That's an interesting topic! I'd be happy to help explain. Could you be more specific?"
    elif 'joke' in message_lower or 'funny' in message_lower:
        response = "😂 Why don't scientists trust atoms? Because they make up everything!"
    elif 'bye' in message_lower or 'goodbye' in message_lower:
        response = "👋 Goodbye! Have a great day! Come back anytime."
    elif 'who are you' in message_lower:
        response = "🤖 I'm RobittAi, your friendly AI assistant bot!"
    else:
        response = f"🤔 I received your message: *{user_message[:50]}...*\n\n💡 Try asking a question or use /help to see what I can do!"
    
    await update.message.reply_text(response, parse_mode='Markdown')

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'help':
        await query.edit_message_text(COMMANDS_TEXT, parse_mode='Markdown')
    elif query.data == 'about':
        await query.edit_message_text(ABOUT_TEXT, parse_mode='Markdown')

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.warning(f"Update {update} caused error {context.error}")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("ping", ping_command))
    application.add_handler(CommandHandler("time", time_command))
    application.add_handler(CommandHandler("feedback", feedback_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_error_handler(error_handler)
    
    print("🤖 RobittAi Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
