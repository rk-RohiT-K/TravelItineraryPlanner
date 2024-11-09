# OneDay Tour Itinerary Planner
## Overview
The OneDay Tour Itinerary Planner is a travel application designed to plan a comprehensive one-day tour based on user prompts and preferences. The app collects input about places, timings, and budget to create a personalized travel itinerary that adapts to user feedback. Additionally, it provides the current news and weather for the chosen location. The front-end interface is built using Streamlit and involves a user login page and an interactive chat page, while FastAPI powers the back-end services for generating and optimizing itineraries.
## Features
- User Prompt Collection: Accepts input about places, preferred times, and budget for itinerary planning.
- Itinerary Generation: Uses an LLM to generate an itinerary based on user input and preferences.
- Dynamic Adjustments: Modifies the itinerary based on further user suggestions and feedback.
- Weather and News Updates: Displays the latest news and current weather for the selected location.
- User-Friendly Interface: Built with Streamlit for an intuitive user experience, including a login and chat page.
## Requirements
- Python 3.9+
- Streamlit
- FastAPI
- Requests library
- Neo4j (for storing user preferences and visit history)
- Ollama LLM library
## Installation
1. Clone the repository:
~~~sh
git clone https://github.com/yourusername/oneday-tour-planner.git
cd oneday-tour-planner
~~~

2. Install required dependencies:
~~~bash
pip install -r requirements.txt
~~~
3. Ensure your Neo4j database is running and configured properly.
4. Make sure you **AccuWeather** and **NewsApi**, replace them in the ```markdown curr_affairs.py```
## How to Run
### Streamlit Frontend
To start the front-end interface:
~~~sh
streamlit run ./pages/login.py
~~~


### FastAPI Backend
To start the backend service:
~~~sh
uvicorn agents.gen:app --reload
~~~
## Usage
1. Login: Open the Streamlit app and log in through the provided login page.
2. Chat Interaction: Use the chat interface to provide prompts about the places you want to visit, preferred timeframes, and budget.
3. Itinerary Generation: The app processes your input and generates a customized travel itinerary.
4. Modifications: Request changes to the itinerary, and the app will adjust it accordingly.
5. News and Weather Display: View current news articles and weather updates for the destination.
## Tech Stack
- Front-End: Streamlit for building interactive UI components.
- Back-End: FastAPI for API services and handling requests.
- LLM Integration: Ollama for processing and generating itinerary responses.
- Database: Neo4j for storing user preferences and visit history.
- External APIs: News API and AccuWeather API for news and weather updates.
## Future Enhancements
- Integration with real-time mapping services for route visualization.
- Support for multi-day itinerary planning.
- User authentication and profile management for personalized experiences.
## License
This project is licensed under the MIT License.
--- For questions or contributions, please contact [me@tele.com] or create an issue in the GitHub repository.
Enjoy planning your perfect day with the OneDay Tour Itinerary Planner!