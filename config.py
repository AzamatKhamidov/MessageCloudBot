import pymongo, pyrogram


app = pyrogram.Client(
	"Account",
	api_id=api_id,
	api_hash=api_hash
)

token = token
port = port
webhook = webhook
polling = False
host = '127.0.0.1'
channel_id = -1001314753712
mongo_db = pymongo.MongoClient()
main_data = mongo_db['MessageCloudBot']
users = main_data['users']
messages = main_data['messages']