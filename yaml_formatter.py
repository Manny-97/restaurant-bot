import sys

import yaml

input = """
version: "3.1"


# session_config:
#   session_expiration_time: 60
#   carry_over_slots_to_new_session: true

forms:
  restaurant_form:
    required_slots:
    # ignored_intents:
    # - greet
    # - goodbye
    - type: from_entity
      entity: seats
      not_intent: time
      section:
        - type: from_entity
          entity: section

actions:
  - validate_restaurant_form
  - utter_greeting
  - utter_goodbye
  - utter_booking_confirmation
  - utter_unclear
  - utter_ask_time
  - utter_ask_section
  - utter_ask_seats

entities:
  - time
  - section
  - seats

# intents:
#   - greet:
#       use_entities: []
#   - time:
#       use_entities:
#         - time
#   - book:
#       use_entities:
#         - time
#         - section
#         - seats
#   - section:
#       use_entities:
#         - section
#   - seats:
#       use_entities:
#         - seats
#   - goodbye:
#       use_entities: []
#   - faq
#   - nlu_fallback

slots:
  time:
  mappings:
    type: unfeaturized
    influence_conversation: False
  section:
    type: categorical
    values:
      - AC
      - Non-AC
    influence_conversation: False
  seats:
    type: float
    influence_conversation: False

responses:
  utter_greeting:
    - text: "Hello! Welcome to Atreya's Multi-cuisine \
      restaurant. How can I help you?"
  utter_goodbye:
    - text: "Thank you for using our services. See you again!"
  utter_ask_time:
    - text: "At what time would you like to book a reservation?"
  utter_unclear:
    - text: "Sorry, I could not understand. Could you \
      please frame your query in a different way?"
  utter_ask_seats:
    - text: "How many seats would you like to reserve?"
  utter_ask_section:
    - text: "Which section would you like to book?"
      buttons:
        - title: "AC"
          payload: '/section{{"section":"AC"}}'
        - title: "Non-AC"
          payload: '/section{{"section":"Non-AC"}}'
  utter_booking_confirmation:
    - text: "You have reserved {seats} seat(s) in our \
      {section} section for {time}. Thanks!"
  utter_faq/timings:
    - text: "The restaurant opens at 7pm and closes at 10pm."
  utter_faq/days:
    - text: "The restaurant is open each and every day."
  utter_faq/cancel:
    - text: "To cancel a reservation, simply call us at \
      +91-1234567890 and cancel your reservation."
  utter_faq/specials:
    - text: "Our chef is a master of the Italian cuisine. \
      Our core speciality is our pasta, which is renowned throughout the city."

session_config:
  session_expiration_time: 60
  carry_over_slots_to_new_session: true

"""

events = []
level = 0
seen = set()
is_key = False
skip = False

for event in yaml.parse(input):
    if level == 1:
        is_key = not is_key
    if isinstance(event, yaml.CollectionStartEvent):
        level += 1
    elif isinstance(event, yaml.CollectionEndEvent):
        level -= 1
        if level == 1 and skip:
            skip = False
            continue
    elif isinstance(event, yaml.ScalarEvent):
        if level == 1:
            if is_key:
                if event.value in seen:
                    print("skipping duplicate key: " + event.value)
                    skip = True
                else:
                    seen.add(event.value)
            else:
                if skip:
                    skip = False
                    continue
    if not skip:
        events.append(event)

print("Result:\n---")
yaml.emit(events, sys.stdout)
