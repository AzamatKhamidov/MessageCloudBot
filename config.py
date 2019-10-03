import pymongo, pyrogram


app = pyrogram.Client(
	"Account",
	api_id=app_id,
	api_hash=app_has
)

token = token
channel_id = channel_id
mongo_db = pymongo.MongoClient()
main_data = mongo_db['MessageCloudBot']
users = main_data['users']
messages = main_data['messages']