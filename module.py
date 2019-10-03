import config, random, time, database



def generate_password(m):
    pass1 = 'ABCDEFGHJKLMNPQRSTUVWXYZ'
    pass2 = 'abcdefghijkmnpqrstuvwxyz'
    pass3 = '23456789'
    pass4 = ''
    pass5 = [1,2,3]
    pass6 = 'abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'
    for i in range(3):
        v = random.choice(pass5)
        if v == 1:
            pass4 += random.choice(pass1)
        elif v == 2:
            pass4 += random.choice(pass2)
        else:   
            pass4 += random.choice(pass3)
        if i == 0:
            if v == 1:
                pass5.remove(1)
            if v == 2:
                pass5.remove(2)
            if v == 3:
                pass5.remove(3)
        elif i == 1:
            if 3 in pass5:
                if 2 in pass5:
                    if v == 2:
                        pass5.remove(2)
                    else:
                        pass5.remove(3)
                else:
                    if v == 1:
                        pass5.remove(1)
                    else:
                        pass5.remove(3)
            else:
                if v == 1:
                    pass5.remove(1)
                else:
                    pass5.remove(2)
    for i in range(m-3):
        pass7 = random.choice(pass6)
        pass4 += pass7
    return pass4


def make_code(n, m):
    pass8 = []
    for i in range(n):
        q = generate_password(m)
        while q in pass8:
            q = generate_password(m)
        pass8.append(q)
    return pass8 


def mongo_db_checker(connector, data):
	try:
		database.get_info(connector, data)[0]
		return True
	except Exception as e:
		print(e)
		return False



def generate_code(connector, checker, length):
	code = make_code(1, length)[0]
	if not mongo_db_checker(connector, {checker : code}):
		return code
	else:
		generate_code(connector, checker, length)


def new_cloud_message(message):
	data = {'creator_id':message.from_user.id, 'code' : generate_code(config.messages, 'code', 10), 'content_type' : message.content_type}
	if message.content_type == 'text':
		data['text'] = message.text
	elif message.content_type == 'photo':
		data['photo'] = message.photo[-1].file_id
		data['caption'] = message.caption
	elif message.content_type == 'audio':
		data['audio'] = message.audio.file_id
		data['caption'] = message.caption
	elif message.content_type == 'video_note':
		data['video_note'] = message.video_note.file_id
	elif message.content_type == 'document':
		data['document'] = message.document.file_id
		data['caption'] = message.caption
	elif message.content_type == 'sticker':
		data['sticker'] = message.sticker.file_id
	elif message.content_type == 'video':
		data['video'] = message.video.file_id
		data['caption'] = message.caption
	elif message.content_type == 'voice':
		data['voice'] = message.voice.file_id
	elif message.content_type == 'location':
		data['location'] = {
			'lat' : message.location.latitude,
			'lon' : message.location.longitude
		}
	elif message.content_type == 'contact':
		data['contact'] = {
			'phone_number': message.contact.phone_number,
			'first_name': message.contact.first_name,
			'last_name': message.contact.last_name
		}
	return data 

def new_user(message):
	return {
		'user_id' : message.from_user.id,
		'first_name' : message.from_user.first_name,
		'last_name' : message.from_user.last_name,
		'username' : message.from_user.username,
		'time' : time.time()
	}