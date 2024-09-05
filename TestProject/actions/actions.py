from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionConfirmBooking(Action):

    def name(self) -> Text:
        return "action_confirm_booking"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the slot values
        museum = tracker.get_slot('museum')
        date = tracker.get_slot('date')
        day = tracker.get_slot('day')
        number = tracker.get_slot('number')
        payment_method = tracker.get_slot('payment_method')

        # Confirm the booking
        confirmation_message = f"Your {number} tickets for {museum} on {date} have been booked. You can pay via {payment_method}."
        # elif day:
        #     confirmation_message = f"Your {number} tickets for {museum} on {day} have been booked. You can pay via {payment_method}."
        # else:
        #     confirmation_message = f"Sorry there was some error while booking the tickets. Please try again later."

        dispatcher.utter_message(text=confirmation_message)

        # Optionally, you could set some slots to None or update them
        # return [SlotSet("museum", None), SlotSet("date", None), SlotSet("day", None), SlotSet("number", None), SlotSet("payment_method", None)]

        return []
