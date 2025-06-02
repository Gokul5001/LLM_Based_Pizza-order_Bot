from openai import OpenAI
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Initialize the context with the system message
context = [{
    'role': 'system',
    'content': """
    You are OrderBot, an automated service to collect orders for a pizza restaurant. 
    You first greet the customer, then collects the order, 
    and then asks if it's a pickup or delivery. 
    You wait to collect the entire order, then summarize it and check for a final 
    time if the customer wants to add anything else. 
    If it's a delivery, you ask for an address. 
    Finally you collect the payment.
    Make sure to clarify all options, extras and sizes to uniquely 
    identify the item from the menu.
    You respond in a short, very conversational friendly style. 
    The menu includes 
    pepperoni pizza  12.95, 10.00, 7.00 
    cheese pizza   10.95, 9.25, 6.50 
    eggplant pizza   11.95, 9.75, 6.75 
    fries 4.50, 3.50 
    greek salad 7.25 
    Toppings: 
    extra cheese 2.00, 
    mushrooms 1.50 
    sausage 3.00 
    canadian bacon 3.50 
    AI sauce 1.50 
    peppers 1.00 
    Drinks: 
    coke 3.00, 2.00, 1.00 
    sprite 3.00, 2.00, 1.00 
    bottled water 5.00 
    """
}]

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content

@app.route('/chat', methods=['POST'])
def chat():
    global context
    data = request.json
    user_message = data.get('message', '')
    
    # Add user message to context
    context.append({'role': 'user', 'content': user_message})
    
    # Get assistant response
    assistant_response = get_completion_from_messages(context, temperature=1)
    
    # Add assistant response to context
    context.append({'role': 'assistant', 'content': assistant_response})
    
    return jsonify({'response': assistant_response})

@app.route('/summary', methods=['GET'])
def get_summary():
    global context
    summary_message = {
        'role': 'system',
        'content': 'create a json summary of the previous food order. Itemize the price for each item. The fields should be 1) pizza, include size 2) list of toppings 3) list of drinks, include size 4) list of sides include size 5)total price'
    }
    
    messages = context.copy()
    messages.append(summary_message)
    
    summary = get_completion_from_messages(messages, temperature=0)
    
    try:
        # Try to parse the JSON response
        summary_json = json.loads(summary)
        return jsonify(summary_json)
    except json.JSONDecodeError:
        # If not valid JSON, return as text
        return jsonify({'summary': summary})

@app.route('/reset', methods=['POST'])
def reset_conversation():
    global context
    # Reset to initial context
    context = [{
        'role': 'system',
        'content': """
        You are OrderBot, an automated service to collect orders for a pizza restaurant. 
        You first greet the customer, then collects the order, 
        and then asks if it's a pickup or delivery. 
        You wait to collect the entire order, then summarize it and check for a final 
        time if the customer wants to add anything else. 
        If it's a delivery, you ask for an address. 
        Finally you collect the payment.
        Make sure to clarify all options, extras and sizes to uniquely 
        identify the item from the menu.
        You respond in a short, very conversational friendly style. 
        The menu includes 
        pepperoni pizza  12.95, 10.00, 7.00 
        cheese pizza   10.95, 9.25, 6.50 
        eggplant pizza   11.95, 9.75, 6.75 
        fries 4.50, 3.50 
        greek salad 7.25 
        Toppings: 
        extra cheese 2.00, 
        mushrooms 1.50 
        sausage 3.00 
        canadian bacon 3.50 
        AI sauce 1.50 
        peppers 1.00 
        Drinks: 
        coke 3.00, 2.00, 1.00 
        sprite 3.00, 2.00, 1.00 
        bottled water 5.00 
        """
    }]
    return jsonify({'status': 'conversation reset'})

if __name__ == '__main__':
    app.run(port=5000)