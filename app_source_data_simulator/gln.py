from model import resource
import streamlit as st


def print_gln():
    organizations = resource.return_organizations()
    col1, col2 = st.columns(2)
    with col1:
        chosen_org = st.selectbox('Select an Organization', organizations)

    # ~ #
    # This part just gets all the sites, and then
    # builds the list of names for the list
    sites = resource.return_sites(chosen_org)
    list_of_sites = []
    for site in sites:
        list_of_sites.append(site['name'])
    # ~ #

    with col2:
        chosen_site = st.selectbox('Select a Site', list_of_sites)

    # ~ #
    # This par of the code will get the GLN of the Chosen Site
    for site in sites:
        if site['name'] == chosen_site:
            gln = site['gln']
    return chosen_site, gln
    # ~ #

    # with col3:
    #     st.write("Selected Values:")
    #     st.markdown('`{}`'.format(chosen_org))
    #     st.markdown('`{}`'.format(chosen_site))
    #     st.markdown('`{}`'.format(gln))
