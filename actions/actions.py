# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


from typing import Any, Dict, List, Optional, Text

import dateutil.parser
from rasa_sdk import FormValidationAction, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


class ValidateRestaurantForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_restaurant_form"

    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> Optional[List[Text]]:
        required_slots = ["time", "section", "seats"]
        return required_slots

    async def extract_time(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        datetime = tracker.get_slot("time")
        if datetime is None:
            return {}
        datetime_obj = dateutil.parser.parse(datetime)
        time = datetime_obj.strftime("%H:%M")
        return {"time": time}

    async def validate_time(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        datetime = dateutil.parser.parse(slot_value)
        time = datetime.strftime("%H:%M")
        hours = datetime.strftime("%H")
        # print(time)
        if int(hours) < 19 or int(hours) > 22:
            # print(hours)
            dispatcher.utter_message(text="Please enter a valid time. :(")
            return {"time": None}
        dispatcher.utter_message(text=f"OK! You have chosen: {time}.")
        return {"time": time}

    async def extract_seats(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        seat = tracker.get_slot("seats")
        if seat is None:
            return {"seat": None}
        return {"seats": seat}

    async def validate_seats(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        seat = tracker.get_slot("seats")
        if seat is None:
            return {"seat": None}
        # print(time)
        if type(seat) == int:
            # print(hours)
            dispatcher.utter_message(
                text="Please enter a valid \
                                     number of seats:"
            )
            return {"time": None}
        dispatcher.utter_message(text=f"OK! You have chosen: {seat} seats.")
        return {"time": seat}

    async def extract_section(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        section = tracker.get_slot("section")
        if section not in []:
            return {"seat": None}
        return {"seats": section}

    async def validate_section(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        section = tracker.get_slot("section")
        if section is None:
            dispatcher.utter_message(
                text="Please enter any of the \
                                     listed sections:"
            )
            return {"time": None}
        dispatcher.utter_message(
            text=f"OK! You have chosen: \
                                 {section} section."
        )
        return {"time": section}
