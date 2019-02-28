#!/usr/bin/python3
import sys, getopt
import requests
import time
import json

# Más info: https://api.slack.com/custom-integrations/legacy-tokens
# Legacy token
legacy_token = 'xoxp-******'

# Id del canal
channel = 'C9*****'

# Fecha límite para filtrar los datos
# Días * horas * minutos * segundos
deadline = int(time.time()) - 2 * 24 * 60 * 60

# Obtiene los archivos de un canal
# Más info: https://api.slack.com/methods/files.list
def list_files():
    params = { 'token': legacy_token, 'ts_to': deadline, 'count': 1000 }
    uri = 'https://slack.com/api/files.list'
    response = requests.get(uri, params=params)
    return json.loads(response.text)['files']

# Elimina los archivos de un canal por medio de los ids
# Más info: https://api.slack.com/methods/files.delete
def delete_files(file_ids):
    count = 0
    num_files = len(file_ids)
    for file_id in file_ids:
        count = count + 1
        params = {
            'token': legacy_token,
            'file': file_id
        }
        uri = 'https://slack.com/api/files.delete'
        response = requests.get(uri, params=params)
        print(count, "of", num_files, "-", file_id, json.loads(response.text)['ok'])

def list_messages():
    params = { 'token': legacy_token, 'channel': channel, 'latest': deadline, 'count': 1000 }
    uri = 'https://slack.com/api/channels.history'
    response = requests.get(uri, params=params)
    return json.loads(response.text)['messages']

def delete_messages(ts_messages):
    count = 0
    num = len(ts_messages)
    for ts_id in ts_messages:
        count = count + 1
        params = {
            'token': legacy_token,
            'channel': channel,
            'ts': ts_id
        }
        uri = 'https://slack.com/api/chat.delete'
        response = requests.post(uri, params=params)
        print(count, "of", num, "-", ts_id, json.loads(response.text)['ok'])

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "fm", ["files", "messages"])
    except getopt.GetoptError:
        print('Parameter error, example: clean_slack.py -f <files> -m <messages>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-f', '--files'):
            files = list_files()
            file_ids = [f['id'] for f in files]
            # delete_files(file_ids) Descomentar para eliminar
            print(json.dumps(files, indent=2)) # Lista los archivos
            sys.exit()
        elif opt in ('-m', '--messages'):
            messages = list_messages()
            ts_ids = [m['ts'] for m in messages]
            # delete_messages(ts_ids)
            print(json.dumps(messages, indent=2))
            sys.exit()
    print('Empty parameter, example: ./clean_slack.py -f <files> -m <messages>')

main(sys.argv[1:])
