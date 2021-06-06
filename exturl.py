import requests
import urllib.parse
import socket
import sys
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate


SMTP_SERVER_ADDR = 'HERE IS SMTP SERVER ADDR'
MAIL_ADDRESS = 'HERE IS EMAIL ADDR FOR CONNECT SMTP SERVER'
MAIL_PASSWORD = 'HERE IS PASSWORD ADDR FOR CONNECT SMTP SERVER'
SMTP_SERVER_PORT = 587
WEBSITE_URL = 'HERE IS URL FOR SCRAPING'
USER_AGENT = 'HERE IS USER-AGENT WHEN SEND REQUEST FOR WEB SERVER'
TEXT_DECODE_TYPE = 'HERE IS TEXT DECODE TYPE' # ex.'utf-8'
MY_EMAIL_ADDR = 'HERE IS YOUR EMAIL ADDR FRO SEND E-MAIL'


# Create E-Mail
def create_message(from_addr, to_addr, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Date'] = formatdate()
    return msg


# Send E-Mail
def send_mail(from_addr, to_addr, body_msg):
    smtpobj = smtplib.SMTP(SMTP_SERVER_ADDR, SMTP_SERVER_PORT)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(MAIL_ADDRESS, MAIL_PASSWORD)
    smtpobj.sendmail(from_addr, to_addr, body_msg.as_string())
    smtpobj.close()


# Check target word in one line
def check_words(line, words):
    hit = False
    for i in range(len(words)):
        if len(words[i]) > 0:
            if words[i] in line:
                hit = True
            else:
                hit = False
                break
    return hit 


# Read text file with target word (1 word on 1 line)
print('Loading target word...')
path = 'word.txt'
with open(path) as f:
    search_str = [s.strip() for s in f.readlines()]

if len(search_str) > 0 and search_str[0] != '':
    print('done.')
    print('Send request to get searh result.')

    url = WEBSITE_URL
    dir_path = url[0:url.rfind('/')+1] # for relative URL
    headers = {
        "User-Agent" : USER_AGENT,
    }

    req = urllib.request.Request(url,None,headers)

    response = urllib.request.urlopen(req)
    html = response.read().decode(TEXT_DECODE_TYPE, errors='ignore')
    parsed_html = BeautifulSoup(html, 'html.parser')

    a_list = parsed_html.findAll('a')
    result_list = []
    for a in a_list:
        if 'href' in a.attrs: # Example: extact url from hyperlink
            if check_words(a.text, search_str): # check whether all words are included.
                result_list.append(a.text + ' --> ' + dir_path + a.attrs['href']+'\n')

    if len(result_list) > 0:
        result_str = ''
        for result in result_list:
            result_str += result
        print(result_str)
        print('Send mail')
        msg = create_message(MY_EMAIL_ADDR, MY_EMAIL_ADDR, 'Search Result', result_str)
        send_mail(MY_EMAIL_ADDR, MY_EMAIL_ADDR, msg)
    else:
        print('No Result')

else:
    print('Process aborted because target word was empty.')