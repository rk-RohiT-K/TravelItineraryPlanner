import streamlit as st
import json
import chat

def login():
    st.title("Login")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:

            with open("creds.json", "r") as f:
                data = json.load(f)
            for user in data["users"]:
                if user["username"] == username and user["password"] == password:
                    st.success("Login successful!")
                    st.session_state.authenticated = True
                    # Navigate to chat page after successful login
                    # st.experimental_nav(url="chat.py")  # Assuming chat.py is in the same directory
                    return
            st.error("Incorrect username or password")

def main():
    if "authenticated" not in st.session_state:
        login()
    else:
        chat.main()
if __name__ == "__main__":
    main()
