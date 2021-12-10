# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from datetime import date
import requests

Last_Field = None
class ActionShowNews(Action):
    def name(self) -> Text:
        return "action_show_news"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        field = next(tracker.get_latest_entity_values("news_field"),None) 
        if not field:
            field = "random"
        url = ('https://newsapi.org/v2/everything?'
        'q=' + field + '&'
       'from=' + date.today().strftime("%Y-%m-%d") + '&'
       'sortBy=popularity&'
       'apiKey=a4798906e1614010b7d0ef0b2694bbd4')
        indent = "   "
        response = requests.get(url).json()['articles']
        Articles = response
        message = field + " news" + "\n"
        Last_Field = field;
        i = 1
        for n in response:
            message += indent + str(i) + "-  " + n['title'] + "\n"
            i+=1
        
        dispatcher.utter_message(text=message)

        return []

class ShowArticle(Action):
    def name(self) -> Text:
        return "action_show_article"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        article = next(tracker.get_latest_entity_values("number_art"),None) 

        if not article:
            article = 0
        else :
            article = int(article)
        
        field = next(tracker.get_latest_entity_values("news_field"),None) 
        if not field:
            field = "random"
        url = ('https://newsapi.org/v2/everything?'
            'q=' + field + '&'
            'from=' + date.today().strftime("%Y-%m-%d") + '&'
            'sortBy=popularity&'
            'apiKey=a4798906e1614010b7d0ef0b2694bbd4')
        indent = "   "
        response = requests.get(url).json()['articles']
        Articles = response
        if article > len(Articles):
            article = len(Articles)
        message = "News: " + field + "\n"
        message += str(article) + "- "+ Articles[article-1]['title'] + "\n"
        message += "*- Description: " + Articles[article-1]['description'] + "\n"

        dispatcher.utter_message(text=message)
        return []



class GetJokes(Action):
    def name(self) -> Text:
        return "action_get_joke"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        message =  requests.get('http://api.icndb.com/jokes/random/1')
        message = message.json()["value"][0]['joke']
        dispatcher.utter_message(text="  " + message)
        return []