import streamlit as st
import pandas as pd
import requests
import json
import time
from gln import print_gln
from event import print_event
from memory import Memory
from builder import payload
from model import resource

st.set_page_config(
    page_title="Source Data Simulator", page_icon="🌱", initial_sidebar_state="expanded"
)

mem = Memory()

st.write(
    """
# Source Data Generator
Generate your events for a use case!
"""
)


def save_memory(gln, site, event_type, bizstep, lot_gtin):
    st.session_state.memory.add_to_memory('{} / {} / {} / {} / {}'.format(
        str(lot_gtin), event_type, bizstep, gln, site))


def request(event_input: dict):
    array_of_events = [event_input]
    url = 'https://traceability-n4j-data-model-g6cwscijuq-uc.a.run.app/source/api/graphdb/events'
    headers = {
        'Content-type': 'application/json'
    }
    try:
        r = requests.post(url, headers=headers, data=json.dumps(array_of_events))
        if r.status_code == 200:
            st.write("Yey!")
        else:
            st.write("oops")
            st.write(r.status_code)
            st.write(r.content)
    except Exception as error:
        print(error)


# Store the initial value of widgets in session state
# Ok this part creates a memory object class
# and what I understand is that this st.session_state is like a dictionary
# which hast its keys as memory fields, and the values are what you are
# storing in memory.
mem = Memory()
if "memory" not in st.session_state:
    st.session_state.memory = mem

# Launch loading application

# Front End
site, gln = print_gln()
event_type, bizstep, lot_gtin = print_event()

# Builder
event = payload(gln, event_type, bizstep, lot_gtin)
st.success('Event Ready')
st.write(event)

st.warning("Ready to send Event to Graph Database")
if st.button('Send Event'):
    save_memory(gln, site, event_type, bizstep, lot_gtin)
    request(event)

st.error("Danger Zone")
if st.button('Clean Use Case'):
    st.session_state.memory.clean_memory()

st.session_state.memory.print_memory()
