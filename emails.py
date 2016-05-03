from player import RankedPlayer, RankedPlayerList
from streamers import Streamers
import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import fantasy_baseball_settings

def send_email(recipients, subject, html):
  to =  ", ".join(recipients)

  msg = MIMEMultipart('alternative')
  msg['Subject'] = subject
  msg['From'] = fantasy_baseball_settings.email_account
  msg['To'] = to
  
  msg.attach(MIMEText(html, 'html'))
  
  username = fantasy_baseball_settings.email_account
  password = fantasy_baseball_settings.email_pw
  smtp_server = fantasy_baseball_settings.smtp_server
  server = smtplib.SMTP(smtp_server)
  server.starttls()
  server.login(username,password)
  server.sendmail(fantasy_baseball_settings.email_account, recipients, msg.as_string())
  server.quit()

def send_daily_email(team):
    est_time = datetime.now()+timedelta(hours=3)
    overall_rankings_table = build_rankings_table(team.overall_rankings)
    avg_rankings_table = build_rankings_table(team.overall_rankings)

    category_rankings_tables = [build_rankings_table(x) for x in team.category_rankings]

    category_rankings_tables_html = ""
    for x in category_rankings_tables:
        category_rankings_tables_html += x

    streamer_table = build_streamer_table(team.streamers)
    html_message = """
    <html>
      <head>
      Daily Report
      </head>
      <body>
      <div>
        {streamer_table}
      </div>
      <hr>
      <div>
        {overall_rankings_table}
      </div>
      <hr>
      <div>
      <div><h3> CATEGORY RANKINGS </h3></div>
      {category_rankings_tables}
      </div>
      </body>
    </html>""".format(streamer_table = streamer_table, overall_rankings_table = overall_rankings_table, category_rankings_tables = category_rankings_tables_html)
  
    subject = "Fantasy Baseball Help - {0}".format(est_time.strftime("%B %d, %Y"))

    send_email(fantasy_baseball_settings.recipients, subject, html_message)


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
      <h3 style="text-align: center">Today's Possible Streamers</h3>
      <table cellspacing="0" cellpadding="5" border="1" style="border:1px solid #ccc; margin: auto; width: 80%; padding: 10px;">
          <tr>
            <td>GD</td>
            <td>Name</td>
            <td>Opponent</td>
            <td>W-L</td>
            <td>ERA</td>
            <td>WHIP</td>
          </tr>
          <tbody>
            {0}
          </tbody>
      </table>""".format(table_body)
    return table_html

def build_rankings_table(ranked_player_list):
    table_body = ""
    for rp in ranked_player_list.ranked_players:
        table_body += """<tr>
            <td>{rank}</td>
            <td>{name}</td>
            <td>{ranked_value}</td>
          </tr>""".format(rank=rp.rank, name=rp.player.name, ranked_value = rp.ranked_value)
    
    table_html = """
      <h3 style="text-align: center">{rankings_type} Rankings</h3>
      <table cellspacing="0" cellpadding="5" border="1" style="border:1px solid #ccc; margin: auto; width: 80%; padding: 10px;">
          <tr>
            <td>Rank</td>
            <td>Player</td>
            <td>Value</td>
          </tr>
          <tbody>
            {table_body}
          </tbody>
      </table>""".format(rankings_type = ranked_player_list.rank_type, table_body = table_body)
    return table_html
