import telebot, config, strings, database, module, requests, logging, eventlet, json, sys
from threading import Thread, Lock, Timer
from flask_socketio import SocketIO, disconnect
from flask import Flask, render_template, request, Response, abort, jsonify

bot = telebot.TeleBot(config.token)
bot_username = bot.get_me().username
logging.basicConfig(format='%(asctime)s (%(filename)s:%(lineno)d) %(levelname)s:%(name)s:"%(message)s"',
                    datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet', logger=False, engineio_logger=False)


@bot.message_handler(commands=['start'])
def start_handler(message):
	print(message.text)
	if not module.mongo_db_checker(config.users, {'user_id' : message.from_user.id}):
		database.insert_into(config.users, module.new_user(message))
	if len(message.text.split()) >= 2:
		if module.mongo_db_checker(config.messages, {'code' : message.text.split()[1]}):
			message_data = database.get_info(config.messages, {'code' : message.text.split()[1]})[0]
			try:
				if message_data['content_type'] == 'text':
					bot.send_message(message.chat.id, message_data['text'])
				elif message_data['content_type'] == 'photo':
					bot.send_photo(message.chat.id, message_data['photo'], message_data['caption'])				
				elif message_data['content_type'] == 'audio':
					bot.send_audio(message.chat.id, message_data['audio'], message_data['caption'])
				elif message_data['content_type'] in ['document' in 'video_note']:
					bot.send_document(message.chat.id, message_data['document'], message_data['caption'])
				elif message_data['content_type'] == 'sticker':
					bot.send_sticker(message.chat.id, message_data['sticker'])
				elif message_data['content_type'] == 'video':
					bot.send_video(message.chat.id, message_data['video'], message_data['caption'])
				elif message_data['content_type'] == 'voice':
					bot.send_voice(message.chat.id, message_data['voice'], message_data['voice'])
				elif message_data['content_type'] == 'location':
					bot.send_location(message.chat.id, message_data['location']['lat'], message_data['location']['lon'])
				elif message_data['content_type'] == 'contact':
					bot.send_contact(message.chat.id, message_data['contact']['phone_number'], message_data['contact']['first_name'], message_data['contact']['last_name'])
			except Exception as e:
				print(e)
				config.app.forward_messages('@'+bot_username, message_data['channel']['chat_id'], message_data['channel']['message_id'])
				start_handler(message)
			return
	bot.send_message(message.chat.id, strings.WELCOME, parse_mode='html')



@bot.message_handler(content_types=['text', 'audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice', 'location', 'contact'])
def message_handler(message):
	data = module.new_cloud_message(message)
	msg = bot.forward_message(config.channel_id, message.chat.id, message.message_id)
	url = 't.me/{}?start={}'.format(bot_username, data['code'])
	data['channel'] = {'message_id' : msg.message_id, 'chat_id' : msg.chat.id}
	database.insert_into(config.messages, data)
	bot.send_message(message.chat.id, url, disable_web_page_preview=True)

config.app.start()

@app.route('/', methods=['POST'])
def web_hook():
	if request.headers.get('content-type') == 'application/json':
		data = request.get_data().decode("utf-8")
		update = telebot.types.Update.de_json(data)
		user_id = 0
		try:
			user_id = update.message.from_user.id
		except:
			pass
		if user_id == 777000:
			return ''
		if update.message:
		    bot.process_new_messages([update.message])
		if update.callback_query:
		    bot.process_new_callback_query([update.callback_query])
		if update.inline_query:
		    bot.process_new_inline_query([update.inline_query])
		if update.channel_post:
			bot.process_new_channel_posts([update.channel_post])
		if update.edited_channel_post:
			bot.process_new_edited_channel_posts([update.edited_channel_post])
		if update.chosen_inline_result:
			bot.process_new_chosen_inline_query([update.chosen_inline_result])
		return ''
	abort(403)


def bot_polling():
	bot.remove_webhook()
	bot.polling()


def main(argv):
	if config.polling:
		logger.info('starting polling...')
		thread = Thread(target=bot_polling)
		thread.start()
	else:
		logging.info('setting webhook...')
		bot.remove_webhook()
		bot.set_webhook(config.webhook)
	me = bot.get_me()
	logger.info('Me: %s @%s', me.first_name, me.username)
	# init_commands()
	socketio.run(app, host=config.host, port=config.port, use_reloader=False,
	             debug=False)


if __name__ == '__main__':
    main(sys.argv[1:])