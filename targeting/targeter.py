from api import Phoenix
from franklinbot import FranklinBot
import sys
import glob

fb = FranklinBot()

ph = Phoenix()

#glub = glob.glob(r'queries/targeting/*.sql')
glub = glob.glob(r'queries/targeting/*.sql')

for sql in glub: 
    print('running surpressed target at...',sql, ' on ', fb.today)
    q = open(sql, 'r+').read()
    df = ph.exe(q)



glib = glob.glob(r'queries/targeting/.unsurpressed/*.sql')

for sql in glib: 
    print('running unsurpressed target at...',sql, ' on ', fb.today)
    q = open(sql, 'r+').read()
    df = ph.exe(q)
