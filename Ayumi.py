import requests
import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Set the ChatGPT API key and Telegram chat ID as environment variables
os.environ['ChatGPT_API_KEY'] = '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'
os.environ['TELEGRAM_CHAT_ID'] = '-5814700750'
os.environ['TELEGRAM_BOT_API_TOKEN'] = '5814700750:AAHyUMRFj_G4js1juky2jrd4-P141JjrtrU'

# Set up the Telegram bot
bot = telegram.Bot(os.environ['TELEGRAM_BOT_API_TOKEN'])

def start(update, context):
    print('Chat ID is: ${update.effective_chat.id}')
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi there! Send me a message and I'll generate a response.")

def generate_response(message):
    # Define the API endpoint URL
    url = "https://api.openai.com/v1/engines/davinci/completions"

    # Set the request headers with the API key
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ['ChatGPT_API_KEY']}"
    }

    # Set the API request parameters
    data = {
        "prompt": message,
        "temperature": 0.7,
        "max_tokens": 60
    }

    # Send the HTTP POST request to the API endpoint
    response = requests.post(url, json=data, headers=headers)

    # Check if the response was successful
    if response.status_code == 200:
        response_json = response.json()
        message = response_json["choices"][0]["text"]
        return message
    else:
        print(response.status_code)
        print(response.content)
        return "Error: Something went wrong with the request."

def respond(update, context):
    message = update.message.text
    response = generate_response(message)
    print(response)
    if response:
        print('chat_id: ')
        print(os.environ['TELEGRAM_CHAT_ID'])
        context.bot.send_message(chat_id=os.environ['TELEGRAM_CHAT_ID'], text=response)
    else:
        print("Empty response received, not sending message to chat.")

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token=os.environ['TELEGRAM_BOT_API_TOKEN'], use_context=True)
    print("1")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add handlers for the /start and /respond commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, respond))
    print("2")
    # Start the bot
    updater.start_polling()
    print("3")

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
