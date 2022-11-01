import yaml
import base64
import argparse
import os
from gnupg import GPG
import sys


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', type=str, required=True, help="Enter Key name")
    parser.add_argument('--value', type=str, required=True, help="Enter Value name")
    parser.add_argument('--service', type=str, required=True, help="Enter Service name")
    parser.add_argument('--existing', type=str, required=True, help="Enter existing value 'true' or 'false'")
    return parser.parse_args()


def decrypt_file(secrets_file):
    if os.path.exists(secrets_file):
        output_fname = os.path.splitext(secrets_file)[0]
        gpg = GPG(gpgbinary="/usr/local/bin/gpg")
        passwd = os.getenv("GPG_PASSPHRASE")
        with open(secrets_file, 'rb') as f:
            status = gpg.decrypt_file(f, passphrase=passwd, output=output_fname)
            if status.status == "decryption ok":
                print(f"Decrypted file is {output_fname}")
            else:
                print("File was not decrypted")
                sys.exit(1)
    else:
        print(f"{secrets_file} file does not exist")
        sys.exit(1)



def update_secret(key, value, secrets_file, existing):
    with open(secrets_file) as f:
        yml_to_dict = yaml.load(f, Loader=yaml.FullLoader)  # Convert Yaml to dict
        dct = {}
        msg_bytes = value.encode('ascii')    # Converting input string to bytes-like object
        base64_value = base64.b64encode(msg_bytes).decode('ascii')  #Convert base64_bytes to ASCII
        dct[key] = base64_value
        if existing == "true" and key in yml_to_dict:
            print(f"Updating value for existing key : {key}")
            yml_to_dict['data'][key] = base64_value
            value = 'true'
        elif existing == "false" and key not in yml_to_dict:
            print(f"Create new Key/Value entry : {key} : {base64_value}")
            yml_to_dict['data'].update(dct)
            value = 'true'
        else:
            print(f"Seems key - {key} does not exist in yaml file. Please verify the arguments passed to script")
            value = 'false'
        return value


def encrypt_file(secrets_file):
    gpg_file = secrets_file + '.gpg'
    gpg = GPG(gpgbinary="/usr/local/bin/gpg")
    passwd = os.getenv("GPG_PASSPHRASE")
    with open(secrets_file, 'rb') as f:
        status = gpg.encrypt_file(f, passphrase=passwd, recipients=['sharatchandrapasham@gmail.com'], output=gpg_file)
        if status.status == "encryption ok":
            print(f"Encrypted file is {gpg_file}")
        else:
            print("File was not encrypted")
            sys.exit(1)


if __name__ == '__main__':
    args = get_args()
    secret_file_path = 'helm/app/templates/'
    file_name = secret_file_path + args.service + "-secrets.yml"
    decrypt_file(file_name + '.gpg')
    updated = update_secret(args.key, args.value, file_name, args.existing)
    if updated:
        encrypt_file(file_name)









