import mongoengine
# mongodb://<dbuser>:<dbpassword>@ds141490.mlab.com:41490/dragon15098
host = "ds141490.mlab.com"
port = 41490
db_name = "dragon15098"
username = "dragon15098"
password = "987654321"
def connect():
    mongoengine.connect(db_name, host=host, port=port, username=username, password=password)

def list2json(l):
    import json
    return [json.loads(item.to_json()) for item in l]

def item2json(item):
    import json
    return json.loads(item.to_json())
