# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from datetime import datetime
from requests import get
from json import loads
from bs4 import BeautifulSoup
from PyDictionary import PyDictionary

class ActionWeather(Action):
    def name(self) -> Text:
        return "action_weather"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent_name = tracker.latest_message["intent"]["name"]
        print("action_weather processing "+intent_name)
        dispatcher.utter_message(text="Will look up the weather in next version.")
        return []

class ActionJoke(Action):
    def name(self) -> Text:
        return "action_joke"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent_name = tracker.latest_message["intent"]["name"]
        print("action_joke processing "+intent_name)
        try:
            data = get("https://official-joke-api.appspot.com/random_joke")
            a = loads(data.text)
            dispatcher.utter_message(text=a["setup"]+"\n"+a["punchline"])
        except Exception as inst:
            print(inst)
            dispatcher.utter_message(text='Why do chickens cross the road?')
        return []

class ActionInspire(Action):
    def name(self) -> Text:
        return "action_inspire"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent_name = tracker.latest_message["intent"]["name"]
        print("action_inspire processing "+intent_name)
        try:
            response = get('http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en')
            dispatcher.utter_message(text='{quoteText} - {quoteAuthor}'.format(**loads(response.text)))
        except Exception as inst:
            print(inst)
            dispatcher.utter_message(text='Ask me again tomorrow')
        return []

class ActionTime(Action):
    def name(self) -> Text:
        return "action_telltime"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_time = datetime.now().strftime("%I %M %p")
        dispatcher.utter_message(text="It's "+current_time)
        return []


class ActionWiki(Action):
    def name(self) -> Text:
        return "action_wiki"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        subject = tracker.get_slot('subject')
        SlotSet("subject", None)
        if subject is None:
            dispatcher.utter_message(text="Sorry I can't help you with this")
        else:
            try:
                if (len(subject.split()) > 1):
                    ret = self.wiki(subject)
                else:
                    ret = self.lookup(subject)
                    if ret is None:
                        ret = self.wiki(subject)
                dispatcher.utter_message(text=ret)
            except Exception as inst:
                print(inst)
                dispatcher.utter_message(text='Ask me another question.')
        return []
    def lookup(self, subject):
        dictionary=PyDictionary()
        m = dictionary.meaning(subject)
        if m is None:
            return None
        else:
            ret = ""
            for i in m:
                ret += i + ": " + m[i][0] + '\n'
            return ret
    def wiki(self, subject):
        data = get("https://en.wikipedia.org/w/api.php?action=opensearch&search="+subject+"&limit=1&namespace=0&format=json")
        a = loads(data.text)
        data = get("https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro&titles="+a[1][0]+"&format=json")
        p = loads(data.text)["query"]["pages"]
        for i in p:
            txt = BeautifulSoup(p[i]["extract"],features="lxml").getText()
            ## url is a[3][0]
            return txt
"""
import sys
subject = sys.argv[1]
if (len(subject.split()) > 1):
    ret = ActionWiki.wiki(subject)
else:
    ret = ActionWiki.lookup(subject)
    if ret is None:
        ret = ActionWiki.wiki(subject)
print(ret)
from mathparse import mathparse
subject = sys.argv[1]
ret = mathparse.parse(subject)
print(ret)
"""
