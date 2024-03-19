import requests
import utilities.html_utils as html_utils
from flask import Blueprint, current_app

zastepstwa = Blueprint('zastepstwa', __name__)

@zastepstwa.route('/zastepstwa/')
def zastepstwa_get():
    req = requests.get(current_app.config['zastepstwa_url'])
    req.encoding = 'ISO-8859-2'
    data = req.text.replace('\r', '').replace('\n', '')
    data = html_utils.get_text_between_tags(data, 'BODY')
    data = html_utils.split_tag(data, 'TR')
    for i in range(len(data)):
        data[i] = html_utils.get_text_between_tags_array(data[i], 'TD')
    response = { 'informations': [], 'zastepstwa': {} }
    last_teacher = ''
    for row in data:
        if len(row) == 0:
            continue
        if len(row) == 1:
            if row[0].count('<NOBR>') > 0:
                response['informations'].append((html_utils.get_text_between_tags(row[0], 'NOBR')))
            else:
                last_teacher = row[0]
                response['zastepstwa'][last_teacher] = []
            continue
        if row[0] == 'lekcja' or row[0] == '&nbsp;':
            continue
        sec_val_split = row[1].split(' - ')
        if row[2] == '&nbsp;':
            row[2] = ''
        if row[3] == '&nbsp;':
            row[3] = ''
        response['zastepstwa'][last_teacher].append({'godzina': row[0], 
                                                     'klasa': sec_val_split[0],
                                                     'sala': sec_val_split[1],
                                                     'zastepca': row[2],
                                                     'uwagi': row[3]})
    return response

@zastepstwa.route('/zastepstwa/<klasa>/')
def zastepstwa_get_class(klasa:str):
    klasa = klasa.replace(' ', '')
    req = requests.get(current_app.config['zastepstwa_url'])
    req.encoding = 'ISO-8859-2'
    data = req.text.replace('\r', '').replace('\n', '')
    data = html_utils.get_text_between_tags(data, 'BODY')
    data = html_utils.split_tag(data, 'TR')
    for i in range(len(data)):
        data[i] = html_utils.get_text_between_tags_array(data[i], 'TD')
    response = { klasa: {} }
    last_teacher = ''
    count = 0
    for row in data:
        if len(row) == 0:
            continue
        if len(row) == 1:
            if row[0].count('<NOBR>') == 0:
                last_teacher = row[0]
                response[klasa][last_teacher] = []
            continue
        if row[0] == 'lekcja' or row[0] == '&nbsp;':
            continue
        sec_val_split = row[1].split(' - ')
        if sec_val_split[0].replace(' ', '').count(klasa.upper()) == 0:
            continue
        if row[2] == '&nbsp;':
            row[2] = ''
        if row[3] == '&nbsp;':
            row[3] = ''
        response[klasa][last_teacher].append({'godzina': row[0], 
                                'klasa': sec_val_split[0],
                                'sala': sec_val_split[1],
                                'zastepca': row[2],
                                'uwagi': row[3]})
        count += 1
    response['count'] = count
    response[klasa] = {k: v for k, v in response[klasa].items() if v}
    return response