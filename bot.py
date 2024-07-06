import telebot
import time
from TiktokToMp3 import TikTok_to_Mp3
from telebot.types import ForceReply
from keep_alive import keep_alive

keep_alive()
user_states = {}

BOT_TOKEN = '7329754916:AAEaAy9N_LycAjcisyNuzY4WpzcZt_bVFnI'
CHANNEL_USERNAME = '@mangtermux'
GROUP_ID = "-4227551363"
bot = telebot.TeleBot(BOT_TOKEN)

# Membuat Reply Keyboard
markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button_continue = telebot.types.KeyboardButton('Continue')
markup.add(button_continue)

@bot.message_handler(commands=['start'])
def send_welcome(message):
  username = message.from_user.username
  teks = f"Welcome *@{username}*! Please subscribe my channel *{CHANNEL_USERNAME}* for support me before continue."
  bot.send_chat_action(message.chat.id, "typing")
  time.sleep(0.5)
  bot.reply_to(message, teks, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == 'Continue')
def check_subscription(message):
  chat_id = message.chat.id
  username = message.from_user.username
  try:
    user_status = bot.get_chat_member(CHANNEL_USERNAME, message.from_user.id).status
    if user_status in ['member', 'administrator', 'creator']:
      teks = f"Hai boss! @{username} sudah subscribe channel kamu."
      bot.send_chat_action(message.chat.id, "typing")
      time.sleep(0.5)
      markup = ForceReply(selective=False)
      
      bot.send_message(GROUP_ID, teks)
      bot.send_message(message.chat.id, "Send me your tiktok video url?", reply_markup=markup)
      
      user_states[chat_id] = "tiktok_url"
    else:
      bot.send_chat_action(message.chat.id, "typing")
      time.sleep(0.5)
      bot.reply_to(message, f"Sorry, you must subscribe to *{CHANNEL_USERNAME}* before continuing.", parse_mode="Markdown")
  except telebot.apihelper.ApiTelegramException as e:
    pass

@bot.message_handler(func=lambda message: user_states.get(message.chat.id, None) == "tiktok_url")
def main_process(message):
  chat_id = message.chat.id
  tiktok_url = message.text
  file_audio = TikTok_to_Mp3(tiktok_url)
  with open(file_audio, "rb") as audio:
    bot.send_chat_action(chat_id, "upload_audio")
    time.sleep(0.5)
    bot.send_audio(chat_id, audio, caption="This is your tiktok audio file!", reply_to_message_id=message.message_id)

bot.infinity_polling()
