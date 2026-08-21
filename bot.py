import os
import logging
import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
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

# User states (simple in-memory storage)
user_data = {}

# --- Command Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when /start is issued."""
    user = update.effective_user
    welcome_text = (
        f"🤖 *Welcome to RobittAi, {user.first_name}!*\n\n"
        "I'm your friendly AI assistant bot. I can help you with:\n"
        "💡 Answering questions\n"
        "📝 Text generation\n"
        "💬 Casual conversations\n"
        "🔍 Information retrieval\n\n"
        "✨ *Just send me a message* and I'll respond!\n"
        "Use /help to see all available commands."
    )
    
    keyboard = [
        [InlineKeyboardButton("📊 Commands", callback_data='help'),
         InlineKeyboardButton("ℹ️ About", callback_data='about')],
        [InlineKeyboardButton("📢 Channel", url='https://t.me/your_channel')]  # Replace with your channel
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a help message when /help is issued."""
    help_text = (
        "🤖 *Available Commands:*\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/about - About this bot\n"
        "/ping - Check bot status\n"
        "/time - Current server time\n"
        "/feedback - Send feedback\n\n"
        "*How to use:*\n"
        "Simply type any message and I'll respond!\n"
        "I can answer questions, chat, and generate text."
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send an about message when /about is issued."""
    about_text = (
        "🤖 *About RobittAi*\n\n"
        "📌 *Version:* 1.0.0\n"
        "📅 *Created:* 2024\n"
        "⚙️ *Framework:* python-telegram-bot\n\n"
        "*Features:*\n"
        "✅ AI-powered responses\n"
        "✅ Text generation\n"
        "✅ 24/7 availability\n"
        "✅ User-friendly interface\n\n"
        "*Privacy Policy:*\n"
        "This bot does not store your personal data.\n"
        "Messages are processed in real-time only.\n\n"
        "📢 *Contact:*\n"
        "For support, use /feedback"
    )
    await update.message.reply_text(about_text, parse_mode='Markdown')

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check if the bot is alive."""
    await update.message.reply_text("🏓 *Pong!* Bot is active and running.", parse_mode='Markdown')

async def time_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get current server time."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await update.message.reply_text(f"🕐 *Server Time:* `{current_time}`", parse_mode='Markdown')

async def feedback_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle feedback command."""
    feedback_text = (
        "📝 *Send Feedback*\n\n"
        "To send feedback, just type:\n"
        "/feedback Your message here\n\n"
        "Example: `/feedback Great bot!`"
    )
    await update.message.reply_text(feedback_text, parse_mode='Markdown')

# --- Message Handler (AI-like responses) ---

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular text messages."""
    user_message = update.message.text
    user_id = update.effective_user.id
    
    # Store user's last message (optional)
    user_data[user_id] = {'last_message': user_message, 'timestamp': datetime.now()}
    
    # Simple intelligent responses (you can replace with actual AI API)
    response = generate_response(user_message)
    
    await update.message.reply_text(response, parse_mode='Markdown')

def generate_response(message):
    """Generate a response based on user input (mocked AI)."""
    message_lower = message.lower()
    
    # Simple pattern matching (replace with actual AI integration)
    if any(word in message_lower for word in ['hello', 'hi', 'hey']):
        return "👋 Hello there! How can I assist you today?"
    elif 'how are you' in message_lower:
        return "🤖 I'm functioning perfectly, thanks for asking! How can I help you?"
    elif 'thank' in message_lower:
        return "😊 You're welcome! Feel free to ask if you need anything else."
    elif 'help' in message_lower:
        return "🆘 I'm here to help! Use /help to see all my commands."
    elif 'what is' in message_lower or 'explain' in message_lower:
        return "📚 That's an interesting topic! I'd be happy to help explain. Could you be more specific about what you'd like to know?"
    elif 'joke' in message_lower:
        return "😂 Why don't scientists trust atoms? Because they make up everything!"
    elif any(word in message_lower for word in ['bye', 'goodbye']):
        return "👋 Goodbye! Have a great day! Come back anytime."
    else:
        return f"🤔 Interesting! I received your message: *{message[:50]}...*\n\nI'm learning new things every day. For specific questions, try asking more clearly or use /help to see what I can do!"

# --- Callback Query Handler ---

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'help':
        await query.edit_message_text(
            "🤖 *Commands List:*\n\n"
            "/start - Start the bot\n"
            "/help - Show help\n"
            "/about - About this bot\n"
            "/ping - Check status\n"
            "/time - Server time\n"
            "/feedback - Send feedback\n\n"
            "Just send any message to chat with me!",
            parse_mode='Markdown'
        )
    elif query.data == 'about':
        await query.edit_message_text(
            "🤖 *About RobittAi*\n\n"
            "🚀 An AI-powered Telegram bot.\n"
            "💡 Built with python-telegram-bot.\n"
            "🔒 100% Telegram policy compliant.\n\n"
            "Made with ❤️ for the Telegram community.",
            parse_mode='Markdown'
        )

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
    
    # Add message handler for all text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Add callback query handler for buttons
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    print("🤖 Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
