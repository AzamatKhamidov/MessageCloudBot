
def get_info(connecter, data):
    print(data)
    if data:
        return connecter.find(data)
    return connecter.find()

def update_info(connecter, by_data, set_data):
    connecter.update_many(by_data,{'$set' : set_data})
    
def insert_into(connecter, data):
    connecter.insert_one(data)