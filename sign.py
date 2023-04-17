import os
import time
from hashlib import sha256
import json
import secp256k1

public_key = input("public_key: ")
private_key = input("private_key: ")

# build event hash
_event = {
    'kind': 1,
    'created_at': int(time.time()),  # set time to now
    'tags': [],
    'content': input("Message: "),
    'pubkey': public_key
}

# per documentation our id is built by hashing the known data_struct format
data_struct = [
  0,
  _event['pubkey'],
  _event['created_at'],
  _event['kind'],
  _event['tags'],
  _event['content'],
]

# serialize our data_struct and remove white spaces
serialized_json = json.dumps(data_struct, separators=(',', ':')).encode('utf-8')

# hash our serialized_json using sha256
_hash_ = sha256()
_hash_.update(serialized_json)
event_id = _hash_.hexdigest()

# append our hashed value as id
_event['id'] = event_id

# do signing
sk = secp256k1.PrivateKey(private_key, raw=False)
event_id = bytes.fromhex(event_id)

_event['sig'] = sk.schnorr_sign(event_id, None, raw=True).hex()

event = ["EVENT", _event]

event_json = json.dumps(event, separators=(',', ':')).encode('utf-8')
print()
print(event_json.decode('utf-8'))