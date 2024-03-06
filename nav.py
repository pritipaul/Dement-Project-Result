import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages


def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]


def make_sidebar():
    with st.sidebar:
        st.title("💎 Details Page")
        st.write("")

        if st.session_state.get("logged_in", False):
            st.page_link("pages/app.py", label="Dementia Prediction Page", icon="🔒")
            st.write("")

        elif get_current_page_name() != "Details":
            st.switch_page("Details.py")
