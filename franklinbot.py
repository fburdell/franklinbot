import datetime

class FranklinBot():

    def __init__(self): 
        self.today = datetime.date.today()
        self.general_election = datetime.date(2020,11,4) 


        self.week_prior = self.today - datetime.timedelta(days=7)
        self.week_future = self.today + datetime.timedelta(days=7)
        self.month_prior = self.today - datetime.timedelta(days=30)

        self.persuasion_start = datetime.date(2020,6,3)  #datetime
        self.persuasion_end = datetime.date(2020,9,15) #datetime
        self.turnout_start = datetime.date(2020,6,3) #datetime
        self.turnout_end = datetime.date(2020,11,27) #datetime
        self.capture_start = datetime.date(2020,10,15) #datetime
        self.capture_end = datetime.date(2020,11,3) #datetime


        self.persuasion_remaining = (self.persuasion_end - self.today).days #count in days
        self.turnout_remaining = (self.turnout_end - self.today).days #count in days
        self.capture_remaining = (self.capture_end - self.today).days #count in days

f = FranklinBot()

