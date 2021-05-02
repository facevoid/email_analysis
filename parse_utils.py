import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re



def parse_raw_message(raw_message):
    
    lines = raw_message.split('\n')
    email = {}
    message = ''
    keys_to_extract = ['from', 'to', 'subject', 'date', 'x-from', 'x-to']
    subject_found = False
    for line in lines:
        
        if ':' not in line:
            if not subject_found:
                continue
            forward_index = raw_message.rfind('- Forwarded by')
            if forward_index != -1:
                continue
            message += line.strip() + ' '
            email['body'] = message
        else:
            pairs = line.split(':')
            key = pairs[0].lower()
            val = pairs[1].strip()
            if key in keys_to_extract:
                email[key] = val
            if key in ['subject', 'to', 'cc']:
                subject_found = True
    if 'body' in email.keys():
        email['body'] = re.sub(r'([,?!])', r' \1 ', email['body'])  #Use regex for more punctuation to do at once
        email['body'] = re.sub(' +', ' ', email['body'])
        email['body'] = email['body'].strip()
    return email
def parse_into_emails(messages):
    emails = [parse_raw_message(message) for message in messages]
        
    bodies = []
    tos = []
    froms = []
    subjects = []
    dates = []
    xfroms = []
    xtos = []
    for email in emails:
        froms.append(email['from'])
        tos.append(email.get('to', None))
        bodies.append(email.get('body', None))
        subjects.append(email.get('subject', None))
        dates.append(email.get('date', None))
        xfroms.append(email.get('x-from', None))
        xtos.append(email.get('x-to', None))
    return {
        'body': bodies, 
        'to': tos, 
        'from_': froms,
        'subject': subjects,
        'date': dates,
        'xfroms': xfroms,
        'xtos': xtos
    }