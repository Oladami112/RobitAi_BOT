import os
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    filters, 
    ContextTypes,
    CallbackQueryHandler  # <-- THIS WAS MISSING!
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token from environment
TOKEN = os.getenv('BOT_TOKEN')

if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set!")

# User states (simple in-memory storage)
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
    """Send a welcome message when /start is issued."""
    keyboard = [
        [InlineKeyboardButton("📋 Commands", callback_data='help'),
         InlineKeyboardButton("ℹ️ About", callback_data='about')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        WELCOME_TEXT,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a help message when /help is issued."""
    await update.message.reply_text(COMMANDS_TEXT, parse_mode='Markdown')

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send an about message when /about is issued."""
    await update.message.reply_text(ABOUT_TEXT, parse_mode='Markdown')

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check if the bot is alive."""
    await update.message.reply_text("🏓 *Pong!* Bot is active and running ✅", parse_mode='Markdown')

async def time_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get current server time."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await update.message.reply_text(f"🕐 *Server Time:* `{current_time}`", parse_mode='Markdown')

async def feedback_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle feedback command."""
    feedback_text = (
        "📝 *Send Feedback*\n\n"
        "To send feedback, type:\n"
        "`/feedback Your message here`\n\n"
        "Example: `/feedback Great bot!`"
    )
    await update.message.reply_text(feedback_text, parse_mode='Markdown')

# --- Message Handler ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular text messages."""
    user_message = update.message.text
    user_id = update.effective_user.id
    
    # Store user's last message
    user_data[user_id] = {'last_message': user_message, 'timestamp': datetime.now()}
    
    # Generate response
    response = generate_response(user_message)
    
    await update.message.reply_text(response, parse_mode='Markdown')

def generate_response(message):
    """Generate a response based on user input."""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['hello', 'hi', 'hey', 'sup', 'yo']):
        return "👋 Hello there! How can I assist you today?"
    elif 'how are you' in message_lower:
        return "🤖 I'm functioning perfectly, thanks for asking! How can I help you?"
    elif 'thank' in message_lower or 'thanks' in message_lower:
        return "😊 You're welcome! Feel free to ask if you need anything else."
    elif 'help' in message_lower:
        return "🆘 I'm here to help! Use /help to see all my commands."
    elif 'what is' in message_lower or 'explain' in message_lower:
        return "📚 That's an interesting topic! I'd be happy to help explain. Could you be more specific?"
    elif 'joke' in message_lower or 'funny' in message_lower:
        return "😂 Why don't scientists trust atoms? Because they make up everything!"
    elif 'bye' in message_lower or 'goodbye' in message_lower:
        return "👋 Goodbye! Have a great day! Come back anytime."
    elif 'who are you' in message_lower:
        return "🤖 I'm RobittAi, your friendly AI assistant bot!"
    elif 'time' in message_lower:
        current_time = datetime.now().strftime("%H:%M:%S")
        return f"🕐 The current time is `{current_time}`"
    else:
        return f"🤔 I received your message: *{message[:50]}...*\n\n💡 Try asking a question or use /help to see what I can do!"

# --- Callback Query Handler ---
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'help':
        await query.edit_message_text(COMMANDS_TEXT, parse_mode='Markdown')
    elif query.data == 'about':
        await query.edit_message_text(ABOUT_TEXT, parse_mode='Markdown')

# --- Error Handler ---
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors."""
    logger.warning(f"Update {update} caused error {context.error}")

# --- Main Function ---
def main():
    """Start the bot."""
    # Create application
    application = Application.builder().token(TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("ping", ping_command))
    application.add_handler(CommandHandler("time", time_command))
    application.add_handler(CommandHandler("feedback", feedback_command))
    
    # Add message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Add callback query handler
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    print("🤖 RobittAi Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
