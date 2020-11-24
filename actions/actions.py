lookup = {
    'a': 1,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'zero': 0,
    'eleven': 11,
    'twelve': 12,
    'fifteen': 15,
    'twenty': 20,
    'twenty five': 25,
    'thirty': 30,
    'fourty': 40,
    'forty': 40,
    'fifty': 50,
    'sixty': 60,
    'one and a half': 1.5,
    'a couple of': 2,
    'couple of': 2,
    'couple': 2,
    'half an': 0.5
}
# Numbers beyond twelve are unlikely
# Numbers beyond 60 will have no value for time

from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from rasa_sdk import Action
from rasa_sdk.forms import FormAction

from datetime import datetime, timedelta

class BookRoomForm(FormAction):
    def name(self):
        return 'book_room_form'
    def required_slots(self,tracker) -> List[Text]:
        return ['number_of_rooms', 'number_of_visitor', 'room_type']
    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        num_rooms = self.from_entity('number_of_rooms')
        return {
                "number_of_rooms": [
                    1 if num_rooms == 'a' else lookup[num_rooms],
                ],
                "number_of_visitor": [
                    lookup[self.from_entity('number_of_visitor')],
                ],
                "room_type": [
                    self.from_entity('room_type'),
                ]
            }
    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> List[Dict]:
        # dispatcher.utter_template('utter_book_room', tracker)
        return []

class CleaningTimeForm(FormAction):
    def name(self):
        return 'cleaning_time_form'
    def required_slots(self,tracker) -> List[Text]:
        return ['cleaning_time']
    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
                "cleaning_time": [
                    self.from_entity('cleaning_time'),
                ]
            }
    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> List[Dict]:
        # cleaning_time = ' '.join(tracker.get_slot('cleaning_time')).lower()
        # now = datetime.now()
        # if cleaning_time.endswith('now') and not 'after' in cleaning_time.split(' '):
            # dispatcher.utter_message(template='utter_clean_room', cleaning_time=cleaning_time)
        # else:
        #     time_unit = cleaning_time.split(' ')[-1]
        #     measure = cleaning_time.replace('after','').replace(time_unit, '').strip(' ')
        #     if 'to' in measure.split(' '):
        #         measure = measure.split(' ')[-1]
        #     try:
        #         int_measure = lookup[measure]
        #     except KeyError as k:
        #         print("Key error occured : {}".format(e))
        #         dispatcher.utter_message(template='utter_clean_room', cleaning_time=cleaning_time)
        #         return []
        #     if time_unit.startswith('hour'):
        #         sched_time = now + timedelta(hour=measure)
        #         dispatcher.utter_message(template='utter_clean_room_detailed', cleaning_time=str(sched_time.hour))
        #     elif time_unit.startswith('min'):
        #         sched_time = now + timedelta(minutes=measure)
        #         sched_time = str(sched_time.hour) + ' hours ' + sched_time.minute + ' minutes'
        #         dispatcher.utter_message(template='utter_clean_room_detailed', cleaning_time=sched_time)
        #     else:
        #         print("The else section was called")
        #         dispatcher.utter_message(template='utter_clean_room', cleaning_time=cleaning_time)

        return []

class ActionSetBookRoom(Action):
    def name(self):
        return 'action_set_book_room'

    def run(self, dispatcher, tracker, domain):
        number_of_rooms = lookup[tracker.get_slot('number_of_rooms')]
        number_of_visitor = lookup[tracker.get_slot('number_of_visitor')]
        dispatcher.utter_template('utter_book_room', tracker)
        return [
            SlotSet('number_of_rooms', str(number_of_rooms)),
            SlotSet('number_of_visitor', str(number_of_visitor))
        ]


class ActionSetCleaningTime(Action):
    def name(self):
        return 'action_set_cleaning_time'

    def run(self, dispatcher, tracker, domain):
        cleaning_time = tracker.get_slot('cleaning_time')
        now = datetime.now()
        if cleaning_time.endswith('now') and not 'after' in cleaning_time.split(' '):
            # dispatcher.utter_message(template='utter_clean_room', cleaning_time=cleaning_time)
            sched_time = str(now.hour) + ' hours ' + str(now.minute) + ' minutes'
            return [SlotSet('cleaning_time', sched_time)]
        else:
            time_unit = cleaning_time.split(' ')[-1]
            measure = cleaning_time.replace('after','').replace(time_unit, '').strip(' ')
            if 'to' in measure.split(' '):
                measure = measure.split(' ')[-1]
            try:
                int_measure = lookup[measure]
            except KeyError as k:
                print("Key error occured : {}".format(k))
                dispatcher.utter_message(template='utter_clean_room', cleaning_time=cleaning_time)
                return [SlotSet('cleaning_time', cleaning_time)]
            if time_unit.startswith('hour'):
                sched_time = now + timedelta(hours=int_measure)
                sched_time = str(sched_time.hour) + ' hours ' + str(sched_time.minute) + ' minutes'
                # dispatcher.utter_message(template='utter_clean_room_detailed', cleaning_time=sched_time)
            elif time_unit.startswith('min'):
                sched_time = now + timedelta(minutes=int_measure)
                sched_time = str(sched_time.hour) + ' hours ' + str(sched_time.minute) + ' minutes'
                # dispatcher.utter_message(template='utter_clean_room_detailed', cleaning_time=sched_time)
            else:
                sched_time = cleaning_time
                # dispatcher.utter_message(template='utter_clean_room', cleaning_time=cleaning_time)
        return [SlotSet('cleaning_time', sched_time)]
