from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
import json
import datetime as dt
import time
import schedule


def runPy():
    with open('users.json') as file:
        users = json.load(file)
    with open('default.json') as file:
        messages = json.load(file)

    receiver = []
    def getReceiver():
        now = dt.datetime.now()
        for user, time in messages['users'].items():
            for each in time['inbound']:
                date = each['time']
                if int(date) == now.minute:
                    receiver.append({
                        "content": each['content'].encode(),
                        "receiver": user,
                        "id": len(time['inbound']) - 1
                    })
                else:
                    pass

    getReceiver()
    try:
        recKey = receiver[0]['receiver']
        recId = receiver[0]['id']
        publicKey = users['users'][recKey]['keys']['public_key'].encode('latin-1')

        hashed = hmac.HMAC(publicKey, hashes.SHA256(), backend=default_backend())
        hashed.update(receiver[0]['content'])
        finalized = hashed.finalize()
        messages['users'][recKey]['inbound'][recId]['encrypted'] = str(finalized.decode('latin-1'))
    except ValueError as e:
        print('Error code: ', e)
    
    with open('default.json', 'w') as file:
        json.dump(messages, file, indent=3)

schedule.every(20).seconds.do(runPy)

while True:
    schedule.run_pending()
    time.sleep(1)

"""

        
"""
