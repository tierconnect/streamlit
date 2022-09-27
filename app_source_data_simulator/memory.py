import streamlit as st


class Memory:
    def __init__(self):
        self.event_history = []

    def clean_memory(self):
        self.event_history = []

    def add_to_memory(self, element):
        self.event_history.append(element)

    def get_memory(self):
        return self.event_history

    def print_memory(self):
        large_text_memory = ""
        for records in self.event_history:
            line = "{}\n".format(records)
            large_text_memory = large_text_memory + line
        st.text_area('Summary of events', "{}".format(large_text_memory))
