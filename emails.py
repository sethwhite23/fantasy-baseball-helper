import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import fantasy_baseball_settings

def send_email(to_addr, subject, html):
  msg = MIMEMultipart('alternative')
  msg['Subject'] = subject
  msg['From'] = fantasy_baseball_settings.email_account
  msg['To'] = to_addr
  
  msg.attach(MIMEText(html, 'html'))
  
  username = fantasy_baseball_settings.email_account
  password = fantasy_baseball_settings.email_pw
  smtp_server = fantasy_baseball_settings.smtp_server
  server = smtplib.SMTP(smtp_server)
  server.starttls()
  server.login(username,password)
  server.sendmail(fantasy_baseball_settings.email_account, to_addr, msg.as_string())
  server.quit()

def send_daily_email(streamers):
    est_time = datetime.now()+timedelta(hours=3)
    streamer_table = build_streamer_table(streamers)
    html_message = """
    <html>
      <head>
        <h3 style="text-align: center">Today's Possible Streamers</h3>
      </head>
      <body>
      {0}
      </body>
    </html>""".format(streamer_table)
  
    subject = "Fantasy Baseball Help - {0}".format(est_time.strftime("%B %d, %Y"))

    send_email(fantasy_baseball_settings.to_email_address, subject, html_message)


def build_streamer_table(streamers):
    table_body = ""
    for p in streamers:
        table_body += """<tr bgcolor="#{rank_color}" style="background:#{rank_color}">
            <td>{gd}</td>
            <td>{name}</td>
            <td>{opponent}</td>
            <td>{wl}</td>
            <td>{era}</td>
            <td>{whip}</td>
          </tr>""".format(rank_color = p['rank'].value, gd=p['GD'], name=p['Name'], opponent=p['Opponent'], wl=p['W-L'], era=p['ERA'], whip=p['WHIP'])

    table_html = """
      <table cellspacing="0" cellpadding="5" border="1" style="border:1px solid #ccc; margin: auto; width: 80%; padding: 10px;">
          <tr>
            <td>GD</td>
            <td>Name</td>
            <td>Opponent</td>
            <td>W-L</td>
            <td>ERA</td>
            <td>WHIP</td>
            {0}
          </tr>
          <tbody>
          </tbody>
      </table>""".format(table_body)
    return table_html
