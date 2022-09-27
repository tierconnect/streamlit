import streamlit as st
import json
import datetime
import uuid

def payload(gln: str, event_type: str, bizstep: str, lot_gtin: dict) -> dict:

    event_time = datetime.datetime.now().isoformat()
    event_id = str(uuid.uuid1())
    if event_type == 'TransformationEvent':
        payload = {
            'eventTime': event_time,
            'eventId': event_id,
            'bizLocation': gln,
            'bizStep': bizstep,
            'eventType': 'Transformation',
            'inputQuantityList': lot_gtin['input'],
            'outputQuantityList': lot_gtin['output']
        }
        return payload
    elif event_type == 'ObjectEvent':
        payload = {
            'eventTime': event_time,
            'eventId': event_id,
            'bizLocation': gln,
            'bizStep': bizstep,
            'eventType': 'Object',
            'gtin': lot_gtin['gtin'],
            'lot': lot_gtin['lot'],
            'section': ''
        }
        return payload