import os

import requests
import streamlit as st
from django.contrib.auth import authenticate
from django.core.wsgi import get_wsgi_application

TITLE = "Random Cats 😼"

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StreamlitDjango.settings')
application = get_wsgi_application()


def reload():
    """Reload the page"""
    try:
        st.experimental_rerun()
    except Exception as e:
        print("Experimental rerun error:", e)


def run_authentication(username, password):
    user = authenticate(
        username = username, password = password
    )
    if user is not None: # user exists
        st.session_state['user_authenticated'] = True
        # make sure not to store passwords
        del username
        del password
    else:
        st.session_state['user_authenticated'] = False
    reload()


def render_auth_form():
    st.markdown(f"<h1 style='text-align: center;'>Top Secret🤫</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>Log in to proceed.</h1>", unsafe_allow_html=True)
    with st.form('AuthForm'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button(label="Login")
    if login_button:
        run_authentication(username, password)
        # make sure not to store passwords
        del username
        del password


def render_main_app():
    st.markdown(f"<h1 style='text-align: center;'>{TITLE}</h1>", unsafe_allow_html=True)
    left_col, center_col,right_col = st.columns([1,2,1])
    with center_col:
        with st.spinner("Loading..."):
            image = requests.get("https://cataas.com/cat/gif").content # Avoid streamlit caching
            st.image(
                image, 
                use_column_width=True,
                caption="source: http://cataas.com")
        clicked = st.button("Another one!", key="catbutton", use_container_width=True)
        if clicked:
            reload()

if "user_authenticated" in st.session_state: # Prior authentication attempt has been made
    
    if st.session_state["user_authenticated"]: # Authentication successful
        render_main_app()

    else: # Authentication failed
        render_auth_form()
        st.error("Incorrect authentication details")

else: # Prior authentication has not been attempted
    render_auth_form()