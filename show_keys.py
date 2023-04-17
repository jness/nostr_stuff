import os
import re
import subprocess

if not os.path.exists("ec-priv.pem"):
    print("Missing ec-priv.pem, try running generate.sh")

# run openssl to get priv & pub key text
command = 'openssl ec -in ec-priv.pem -text -noout'
output = subprocess.check_output(command.split())

# remove newlines, white space
_res = str(output).replace('\\n', '')
_res = _res.replace(' ', '')

# use regex to fetch private key as hex
private = re.search('priv:(.*)pub:', _res).group(1).replace(':', '')

# use regex to fetch full private key as hex
_public = re.search('pub:(.*)ASN1OID:', _res).group(1)
public = ''.join(_public.split(':')[1:33])

print(f'public: {public}\nprivate: {private}')
