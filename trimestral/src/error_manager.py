from .instances import config

import smtplib


def send_email(exception: Exception):
  if config['profile'] == 'local':
    return None
    
  # Source: https://stackoverflow.com/a/4308203
  body = f'Project execution failed due to exception: {repr(exception)}'

  text = f"Subject: {config['email']['subject']}\n\n{body}"

  server = smtplib.SMTP("smtp.gmail.com", 587)
  server.starttls()

  server.login(config['email']['sender'], config['email']['app_password'])
  server.sendmail(
    config['email']['sender'], 
    config['email']['receiver'], 
    text.encode('utf8')
  )


if __name__ == '__main__':
  print(config)