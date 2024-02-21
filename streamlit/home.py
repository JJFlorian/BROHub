

import streamlit as st
import authentication as auth


def main():
    
    if auth.authenticate():
        st.text("logged in")
    

if __name__ == "__main__":
    main()


