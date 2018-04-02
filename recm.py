# See: https://stackoverflow.com/questions/4908472/how-to-receive-mail-using-python

import poplib
from email import parser
import html2text
import time
import subprocess
import sys


URL = 'kvm.201a.win'
USER = 'fmaster'
PASS = raw_input('Enter the password: ')


def fetch_new_emails(start=1, url=URL, username=USER, password=PASS):
  connector = poplib.POP3(url)
  connector.user(username)
  connector.pass_(password)

  # get messages from server
  messages = [connector.retr(i) for i in range(start, len(connector.list()[1]) + 1)]
  connector.quit()

  # concatenate message pieces
  messages = ["\n".join(msg[1]) for msg in messages]

  # parse messages into email object
  messages = [parser.Parser().parsestr(msg) for msg in messages]

  return messages


def refresh(process):
  start = 1
  try:
    with open('config', 'r') as f:
      start = int(f.read())
  except:
    pass
  messages = fetch_new_emails(start=start)
  # show results
  for message in messages:
    subject = message['subject']
    body = ''
    for part in message.walk():
      if part.get_content_type():
        body = part.get_payload(decode=True)
    body = html2text.html2text(body)
    process(subject, body)

  start += len(messages)
  with open('config', 'w') as f:
    f.write(str(start))


def execute(title, content):
  try:
    if title.startswith('[Run]'):
      subprocess.Popen(content, shell=True)
    else:
      pass
  except Exception as e:
    sys.stderr.write(e + '\n')


def main():
  while True:
    time.sleep(5)
    refresh(execute)


if __name__ == '__main__':
  main()

