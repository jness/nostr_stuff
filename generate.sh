#!/bin/bash

# avoid overwriting our private key
if [ -f ec-priv.pem ] ; then
  echo "ec-priv.pem exists, aborting"
  exit
fi

# create a private key
openssl ecparam -name secp256k1 -genkey -out ec-priv.pem

# make sure not world readable
chmod 600 ec-priv.pem
