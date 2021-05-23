from datetime import datetime, timezone, timedelta
import os
import pickle
from googleapiclient.discovery import build
import logging as log

class Calender:
    def __init__(self):
        #config the log leves
        log.basicConfig(filename='CalEvents.log',level=log.DEBUG, 
                        format='%(asctime)s:%(message)s')

        #creating 24hrs
        self.LocalTime = datetime.now(timezone.utc).astimezone()
        self.LocalTimeNextDay = datetime.now(timezone.utc).astimezone()+timedelta(days=1)

        #time in RFC 3339 format
        log.debug(timeMax := self.LocalTimeNextDay.isoformat())
        log.debug(timeMin := self.LocalTime.isoformat())

        #accessing pickel file
        if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    creds = pickle.load(token)
        self.service = build('calendar', 'v3', credentials=creds)

        self.events = self.service.events().list(calendarId='primary',
                                                timeMax=timeMax,timeMin=timeMin).execute()
    
    def GetNameDict(self):
        self.NameDict = {}
        for event in self.events['items']:
            CalEvent = event['summary'].split(' ')

            #for birthday
            if any(item in CalEvent for item in ['birthday','Birthday']):
                log.debug(SendTo := Calender.GetName(CalEvent))
                
                if len(SendTo) == 2:
                    log.debug(Message := 'Many more happy returns of the day {}...'.format(SendTo[1]))
                    self.NameDict[SendTo[0]] = Message
                else:
                    log.debug(Message := 'Many more happy returns of the day...')
                    self.NameDict[SendTo] = Message

            #for marriage aniversaries
            if any(item in CalEvent for item in ['Marriage','marriage']):
                log.debug(SendTo := Calender.GetName(CalEvent))
                log.debug(Message := 'Happy Marriage Anniversary')
                self.NameDict[SendTo] = Message

        # print(auto.position())
        log.debug('End of Main Function')
    
    @staticmethod
    def GetName(text):
        #to get names for birthdays
        if any(item in text for item in ['birthday','Birthday']):
            text = text[:len(text)-1]
            if any(item in text for item in ['son','daughter','sister','brother']):
                return ' '.join(text[:len(text)-2]),text[-1]
            if 'mummy' in text:
                return ' '.join(text[:len(text)-1]),'aunty'
            if 'daddy' in text:
                return ' '.join(text[:len(text)-1]),'uncle'
            return (' '.join(text),)

        #to get names for marriage anniversaries
        if any(item in text for item in ['Marriage','marriage']):
            text = text[:len(text)-2]
            index = text.index('&')
            return ' '.join(text[:index]),' '.join(text[index+1:])