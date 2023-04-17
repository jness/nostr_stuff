# nostr_stuff

This is a very rough example repository showing step by step the process of interacting
with the nostr protocol, and was created more for education than real world usage.

Early exploration can be found at my blog:

  https://nessy.info/post/2023-02-16-deciphering-nostr-and-its-private-keys/

## Generate private key

The nostr protocol uses a private key to sign messages, while the public key
is that users identity.

Our `generate.sh` script merely uses `openssl` to generate this key pair:

```
% ./generate.sh
```

The content of the private key are textual:

```
% cat ec-priv.pem
-----BEGIN EC PARAMETERS-----
BgUrgQQACg==
-----END EC PARAMETERS-----
-----BEGIN EC PRIVATE KEY-----
MHQCAQEEIDfT3ASi9XTBH+zREDACTE+JxX/PEBlrgqWqbfoAcGBSuBBAAK
oUQDQgAEYXa6NRrOVYKvifswh5Z54u8REDACTFv5QhGyJ5myiP2IrTadD/hpnB
9EeQUgsEW+mpak+t4880s8oXgBkKCw==
-----END EC PRIVATE KEY-----
```

If you wish to explore the private key use `openssl`:

```
% openssl ec -in ec-priv.pem -text -noout
read EC key
Private-Key: (256 bit)
priv:
    37:d3:dc:04:a2:f5:74:c1:1f:ec:fa:65:cf:59:4R:
    ED:AC:Tb:49:04:f8:9c:57:fc:f1:01:96:b8:2a:5a:
    a6:df
pub:
    04:61:76:ba:35:1a:ce:55:82:af:89:fb:30:87:96:
    79:e2:ef:18:d1:db:80:23:50:85:bf:94:21:1b:22:
    79:9b:28:8f:d8:8a:d3:69:d0:ff:86:99:c1:f4:47:
    90:52:0b:04:5b:e9:a9:6a:4f:ad:e3:cf:34:b3:ca:
    17:80:19:0a:0b
ASN1 OID: secp256k1
```

# Show private & public key in hex format

The nostr protocol expects 32 byte hex for both the private and public key,
I do some text manipulation in `show_keys.py` to get just that:

```
% python show_keys.py
read EC key
public: 6176ba351ace5582af89fb30879679e2ef18d1db80235085bf94211b22799b28
private: 37d3dc04a2f574c11fecfa65cf594REDACT7b4904f89c57fcf10196b82a5aa6df
```

# Sign a message

Using the public/private key pair we can sign a message, and generate the
nostr protocol command:

```
% python sign.py
public_key: 6176ba351ace5582af89fb30879679e2ef18d1db80235085bf94211b22799b28
private_key: 37d3dc04a2f574c11fecfa65cf594REDACT7b4904f89c57fcf10196b82a5aa6df
Message: nostr is fun

["EVENT",{"kind":1,"created_at":1681743438,"tags":[],"content":"nostr is fun","pubkey":"6176ba351ace5582af89fb30879679e2ef18d1db80235085bf94211b22799b28","id":"da39f0b7f8c76acb3ae229a1ee090279803d9e824d98b0b1832b037f6432408e","sig":"93fb3288012a57845d56043baed59151c679eb089837def9b459808e22ecd7a0bc416f199563c339296e7d390813d92615bd0dd558e41ce9e1b4762854535ba6"}]
```

This is the `EVENT` we can broadcast on the network to send our message.

# Send our signed message

Taking the `EVENT` from sign.py we can use the `send.py` script to broadcast it:

```
% python send.py
payload: ["EVENT",{"kind":1,"created_at":1681743464,"tags":[],"content":"nostr is fun","pubkey":"6176ba351ace5582af89fb30879679e2ef18d1db80235085bf94211b22799b28","id":"8d40f32b1e0a14df2b839e74159cad7ef35014b1a4bd47df63cdcad1b2ea6bef","sig":"bd536b5eca4f0bced4ab3a7508d9b9f7dfa2bd922d2d11fadc3a4c4cfbc9ae8a2fa9146335ce9973e8988406b4653c8c8bce594f92ad6194a4317032d17ea43d"}]
["OK","8d40f32b1e0a14df2b839e74159cad7ef35014b1a4bd47df63cdcad1b2ea6bef",true,""]
```

The response of `OK` is what we are looking for, we did it!

# Reading messages by public key (user)

And finally we can use the `read.py` script to read all messages by our public key:

```
% python read.py
server [wss://relay.snort.social]:
users pubkey: 6176ba351ace5582af89fb30879679e2ef18d1db80235085bf94211b22799b28
minutes [15]:
[2023-04-17 09:57:44][6176ba351ace5582af89fb30879679e2ef18d1db80235085bf94211b22799b28]
 nostr is fun

```