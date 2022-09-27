from model import resource, util_class
import streamlit as st
import random
import string


def generate_lot(chars: int) -> str:
    N = chars
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))


def print_gtin(keyword):
    gtin_list = util_class.get_gtins()
    return st.selectbox('Select a GTIN', gtin_list, key=keyword)


def print_lot_single():
    if st.button("Autogenerate a Lot "):
        st.session_state.lot_placeholder = generate_lot(10)

    lot_number = st.text_input(label='Lot Number',
                               value=st.session_state.lot_placeholder,
                               placeholder=st.session_state.lot_placeholder,
                               disabled=st.session_state.disabled,
                               label_visibility=st.session_state.visibility,
                               key='lot_number_key')
    single_keyword = 'object_gtin'
    single_gtin = print_gtin(single_keyword)
    return {
        'gtin': single_gtin,
        'lot': lot_number
    }


def print_lot_tf():
    col1, col2 = st.columns(2)
    with col1:
        st.info("Input")
        ingredients = st.slider('How many input sources you have?', min_value=1, max_value=3)
        input_contents_array = []
        for inputs in range(0, ingredients):
            # ~ #
            # TLDR; There are 2 things here. There is a variable for memory and there is a unique key for elements.
            # This part is very interesting. So happens that every widget needs to be unique.
            # That is one fact. The other fact is that the memory element is a dictionary and to store
            # a placeholder value different for every iteration we need to create a variable key.
            # The same logic applies for keys in the widgets. I'm basically creating an element unique for every
            # iteration. So every value is different.
            # This code will initialize the session_state keys to save the placeholders, that then will be
            # replaced if someone actually presses the button to generate a value.
            variable_name = "lot_placeholder_in_{}".format(inputs)
            if variable_name not in st.session_state:
                st.session_state[variable_name] = "Pick or generate a Lot"
            # Once the variable in the session_state is created, we create the variable
            # this means, if there are 4 ingredients, these variables will be in memory:
            # st.session_state.lot_placeholder_in_0 = "Pick or generate a Lot"
            # st.session_state.lot_placeholder_in_1 = "Pick or generate a Lot"
            # st.session_state.lot_placeholder_in_2 ... etc.

            # This is the button. It's unique because it creates these keys
            # key=button_in_0
            # key=button_in_1
            # key=button_in_2
            # If someone presses the button, the placeholder is replaced with a value:
            # st.session_state.lot_placeholder_in_0 = "CAJ21KDA132F"
            # st.session_state.lot_placeholder_in_1 = "ABJ249DA1321"
            if st.button("Autogenerate a Lot ", key="button_in_{}".format(inputs)):
                st.session_state[variable_name] = generate_lot(10)

            # If no one pressed the button, it will show the value "Pick or generate lot"
            # but if you pressed it will show the current value of whatever is there in state.
            # I will stop calling it memory now, because I do have a class for Memory
            # and that one is really for the event history and this one is for the streamlit state.
            lot_number = st.text_input(label='Lot Number',
                                       # Example values during execution:
                                       # value=st.session_state.lot_placeholder_in_0
                                       # placeholder=st.session_state.lot_placeholder_in_0
                                       value=st.session_state[variable_name],
                                       placeholder=st.session_state[variable_name],
                                       disabled=st.session_state.disabled,
                                       label_visibility=st.session_state.visibility,
                                       key="text_in_{}".format(inputs))

            # Now, the final usage is that it will create a keyword for the GTIN box which was only one
            # but for this case we will require multiple GTIN fields and sending the keyword will allow for
            # the GTIN picker to be unique too. The keys will look like:
            # key=gtin_in_0
            # key=gtin_in_1
            # key=gtin_in_2
            keyword = "gtin_in_{}".format(inputs)
            gtin = print_gtin(keyword)
            input_contents_array.append({'gtin': gtin, 'lot': lot_number})

    with col2:
        st.info("Output")
        results = st.slider('How many outputs you will have?', min_value=1, max_value=3)
        output_contents_array = []
        for outputs in range(0, results):
            variable_name = "lot_placeholder_out_{}".format(outputs)
            if variable_name not in st.session_state:
                st.session_state[variable_name] = "Pick or generate a Lot"

            if st.button("Autogenerate a Lot ", key="button_out_{}".format(outputs)):
                st.session_state[variable_name] = generate_lot(10)
            lot_number = st.text_input(label='Lot Number',
                                       value=st.session_state[variable_name],
                                       placeholder=st.session_state[variable_name],
                                       disabled=st.session_state.disabled,
                                       label_visibility=st.session_state.visibility,
                                       key="text_out_{}".format(outputs))
            keyword = "gtin_out_{}".format(outputs)
            gtin = print_gtin(keyword)
            output_contents_array.append({'gtin': gtin, 'lot': lot_number})
    return input_contents_array, output_contents_array


def print_event():
    # Get the possible values from environment variables
    event_types = [i for i in util_class.getenv('EVENT_TYPES').replace(" ", "")
        .split(",")]
    bizsteps = [i for i in util_class.getenv('BIZSTEPS').replace(" ", "")
        .split(",")]
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False
        st.session_state.lot_placeholder = 'XFRD520HC2123'

    gtin_lot = {}
    gtin_lot_input = []
    gtin_lot_output = []

    col1, col2 = st.columns(2)

    with col1:
        chosen_event_type = st.selectbox('Select an Event Type', event_types)

    with col2:
        possible_bizsteps = bizsteps
        if chosen_event_type == 'TransformationEvent':
            possible_bizsteps = ['commissioning']

        chosen_bizstep = st.selectbox('Select a BizStep', possible_bizsteps)
        if chosen_event_type == 'ObjectEvent':
            gtin_lot = print_lot_single()

    # Then the TransformationEvent is selected, it will spread out to all the page
    # instead of putting everything in the same column when it's an object event
    if chosen_event_type == 'TransformationEvent':
        gtin_lot_input, gtin_lot_output = print_lot_tf()

    merged_transformation = {
        "input": gtin_lot_input,
        "output": gtin_lot_output
    }

    if len(merged_transformation['input']) == 0:
        returnable_gtin_lot = gtin_lot
    else:
        returnable_gtin_lot = merged_transformation

    # Well here, because the module needs to return only one type of result to the caller,
    # it will basically merge the results into a single results that will be parsed and interpreted after.
    return chosen_event_type, chosen_bizstep, returnable_gtin_lot
    # ~ #
