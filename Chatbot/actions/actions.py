import os
import uuid
import qrcode
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

        # Ensure all necessary slots are filled
        if not museum or not number or not payment_method:
            dispatcher.utter_message(
                text="It seems like some information is missing for the booking. Please provide the museum name, number of tickets, and payment method."
            )
            return []

        # Generate a unique ID for the booking
        unique_id = str(uuid.uuid4())

        # Generate a QR code for the unique ID
        qr_code_img = qrcode.make(unique_id)

        # Ensure the qr_codes directory exists
        qr_code_dir = "./qr_codes"
        if not os.path.exists(qr_code_dir):
            os.makedirs(qr_code_dir)

        # Save the QR code image
        qr_code_path = os.path.join(qr_code_dir, f"qr_code_{unique_id}.png")
        qr_code_img.save(qr_code_path)

        # Confirm the booking based on available information
        if date:
            confirmation_message = f"Your {number} tickets for {museum} on {date} have been booked. You can pay via {payment_method}. Your unique ID is {unique_id}."
        elif day:
            confirmation_message = f"Your {number} tickets for {museum} on {day} have been booked. You can pay via {payment_method}. Your unique ID is {unique_id}."
        else:
            confirmation_message = f"Your payment for {number} tickets for {museum} could not be completed due to technical issues. Please try again later."

        dispatcher.utter_message(text=confirmation_message)

        # Optionally send the QR code image path to the user (adjust this based on your front-end)
        dispatcher.utter_message(text=f"Path of QR code: {qr_code_path}")

        # Reset the slots after booking confirmation and store the unique ID
        return [SlotSet("museum", None), SlotSet("date", None), SlotSet("day", None), SlotSet("number", None),
                SlotSet("payment_method", None), SlotSet("unique_id", unique_id)]
