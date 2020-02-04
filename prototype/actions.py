from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet

class ActionStatus(Action):
    def name(self):
        return 'action_status_claim'
    
    def run(self, dispatcher, tracker, domain):
        #prod = tracker.get_slot('product')
        claim_number = tracker.get_slot('claim_number')
        confirmationNumber = 123456 #later generate through some process
        response = """Your product {} is ordered for you. It will be shipped to your address. Your confirmation number is {}""".format(
                claim_number,confirmationNumber)
        dispatcher.utter_message(response)
        return [SlotSet('claim_number',claim_number)]

class ActionDefaultFallback(Action):
    def name(self):
        return 'action_default_fallback'

    def run(self,dispatcher,tracker,domain):
        response = """Sorry, I did not understand that, Please contact admin"""
        dispatcher.utter_message(response)
        return 


