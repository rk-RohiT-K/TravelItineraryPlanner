from fastapi import FastAPI
from pydantic import BaseModel
import ollama


app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello World"}
prompt_history = []
pre_defined_rules = """
In our whole conversation you will follow these rules. 
1) Use plain text only, bullet points only when necessary. 
2) You are given a task of planning an itinerary for one-day tour today(don't mention it) of whose prompts I will give you.
3) Itinenary should be in tabular format, use bullet points if necesary.
4) You have to get info about place and timings and budget. No other questions apart from regarding these.
5) Ask for a starting point if not known. No other questions apart from regarding these.
6) Generate an itinerary based on this info.
7) Just for once for suggestions after generating itinerary. No other questions.
8) When the user confirms, generate final itinerary with first a list of stops. Then a sequence of stops and travel suggestions. No further questions.
9) Don't ask for questions inquiring about places or perferences just generate an itinerary based on popular places starting from starting point.
"""
prompt_history.append({'role':'user','content':pre_defined_rules})
prompt_history.append({'role':'model','content':'okay'})

# LLM User Interaction Agent
def generate(history):
    try:
        response = ollama.chat(
            model = "llama3.2",
            messages=history,
        )
    except ollama.ResponseError as e:
        print('Error:', e.error)
    # print(response['message']['content'])
    return response['message']['content']

@app.get("/collect_user_input/")
async def collect_user_input(prompt: str):
    prompt_history.append({'role':'user','content':prompt})
    response = generate(prompt_history)
    prompt_history.append({'role':'model','content':response})
    return response

# LLM Itinerary Generation Agent
def generate_itinerary(final_response):
    predefined_rules = """
    Generate Itinerary for the prompt using these rules
    1.) Clear and Concise
    2.) List places, means of travel to the place and cost in tabular markdown format
    3.) Don't raise any further questions, response ends at the last place.
    4.) No other additional text, just the itinerary.
    """
    response = ollama.chat(
        model = "llama3.2",
        messages=[{'role':'user','content':predefined_rules}] + final_response
    )
    return response

@app.get("/generate_itinerary/")
async def generate_itinerary_endpoint():
    itinerary = generate_itinerary(prompt_history[2:])
    return {"itinerary": itinerary}

# LLM Optimization Agent
def optimize_travel_plan(itinerary):
    rules = """
    Follow these rules for the prompt.
    1.) Optimize the following itinerary making it time efficient and budget friendly.
    2.) If possible also adjust means of travel
    3.) Result should be optimal
    4.) Response should be only the list of places, means of transport, cost incurred.
    5.) No other text rather than the list
    """
    response = ollama.chat(
        model = "llama3.2",
        messages=[{'role':'user','content':rules},{'role':'user','content':itinerary}]
    )
    return response['message']['content']

@app.get("/optimize_travel_plan/")
async def optimize_travel_plan_endpoint(itinerary):
    optimized_plan = optimize_travel_plan(itinerary)
    return optimized_plan