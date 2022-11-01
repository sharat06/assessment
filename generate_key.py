#!/usr/bin/env python3

from gnupg import GPG

gpg = GPG(gpgbinary="/usr/local/bin/gpg")

gpg.encoding = 'utf-8'
input_data = gpg.gen_key_input(
    name_email='sharatchandrapasham@gmail.com',
    passphrase='test1234',
    key_type='RSA',
    key_length=1024)

key = gpg.gen_key(input_data)
print(key)