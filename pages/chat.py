import streamlit as st
import ollama
import requests

BASE_URL = "http://127.0.0.1:8000"


def generate_itinerary(prompt):
    response = requests.get(f"{BASE_URL}/generate_itinerary/?prompt={prompt}")
    if response.status_code == 200:
        return response.json()["itinerary"]
    else:
        return "Failed"
def collect_user_input(prompt):
    response = requests.get(f"{BASE_URL}/collect_user_input/?prompt={prompt}")
    if response.status_code == 200:
        return response.json()
    else:
        return "Failed"
def optimize_travel_plan(itinerary):
    response = requests.get(f"{BASE_URL}/optimize_travel_plan/?itinerary={itinerary}")
    if response.status_code == 200:
        return response.json()
    else:
        return "Failed"
def get_news_n_weather(location):
    response = requests.get(f"{BASE_URL}/get_news_and_weather/?region={location}")
    if response.status_code == 200:
        return response.json()
    else:
        return "Failed"
def get_loc():
    response = requests.get(f"{BASE_URL}/location/")
    if response.status_code == 200:
        return response.json()
    else:
        return "Failed"
def update_info(info):
    response = requests.get(f"{BASE_URL}/update_prompt_hist/?info={info}")
    if response.status_code == 200:
        return response.json()
    else:
        return "Failed"

# if st.button("Reset"):
#     del st.session_state.messages
def main():
    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        st.error("Please login to access the chat.")
    else:
        st.title('Travel@Ease')
        if "messages" not in st.session_state:
            st.session_state.messages = []
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])


        if prompt := st.chat_input("What is up?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            response = collect_user_input(prompt)

            if not '?' in response:
                resp = collect_user_input("Return the name of this city(where trip is planned) in one word only.")
                response += '\n'+'\n**News and Weather**\n' + '\n'+ get_news_n_weather(resp)
                
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()