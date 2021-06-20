from os.path import basename 
import sys 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders

import smtplib as sm

from franklinbot import FranklinBot 
from api import Phoenix, Postgres
from composer import Composer 

#simple instantiation with HD
#composer still activating the benchmarker class in full 
#c = Composer('050')

fbot = FranklinBot()

parameters = {
    'g_user' : 'frank@pahdcc.com',
    'g_password':'ksnveuadipbkbymo'
        }

hds = ['003','018', '026', '029', '030', '041', '044', '053','087', '097', '105', '106', '120', '131', '144', '151', '152', '158', '160', '168', '171', '176', '178', '155', '165'] 

for i, hd in enumerate(hds): 
    print(f'instantiating benchmarker for {hd} on {fbot.today}')
    co = Composer(hd) 
    co.write_daily()
    msg = MIMEMultipart()

    recip = co.emails_all
    #recip = ['frank@pahdcc.com', 'fburdelliv@gmail.com']
    
    subj = f'HD{hd} Target Checks'
    body = 'Evaluating the last seven days of work done in district by both the coordinated and state house campaigns...\n###'
    
    attach = [co.attach_file, co.attach_readme] 
    #appending attachments to msg
    for fi in attach: 
        with open(fi, 'rb') as f: 
            part = MIMEApplication(
                    f.read(), 
                    Name=basename(fi))
        part['Content-Disposition'] = f'attachment; filename={basename(fi)}'

        msg.attach(part)

    #appending body to msg
    msg.attach(MIMEText(body))

    #setting subj of msg 
    msg['Subject'] = rf"[FRANKLINBOT] {fbot.today} " + subj

    server = sm.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()

    server.login(parameters['g_user'], parameters['g_password'])

    server.sendmail(parameters['g_user'], recip, msg.as_string())
    server.close()
