# Pizza Order Bot

A conversational pizza ordering system powered by a large language model (LLM). This repository contains a Flask-based backend (`orderbot.py`) that interacts with OpenAI’s API to manage conversations, and a simple Node.js server (`server.js`) to serve the front-end (`index.html`). The bot greets users, collects their pizza orders, asks for pickup or delivery details, summarizes the order, and processes payment information.

---

## Table of Contents

* [Features](#features)
* [Prerequisites](#prerequisites)
* [Project Structure](#project-structure)
* [Installation](#installation)

  * [1. Clone the Repository](#1-clone-the-repository)
  * [2. Backend Setup (Flask)](#2-backend-setup-flask)
  * [3. Frontend Setup (Node.js)](#3-frontend-setup-nodejs)
* [Configuration](#configuration)
* [Usage](#usage)

  * [Starting the Flask Server](#starting-the-flask-server)
  * [Starting the Node Server](#starting-the-node-server)
  * [Interacting with the Bot](#interacting-with-the-bot)
  * [Endpoints](#endpoints)
* [Environment Variables](#environment-variables)
* [Customization](#customization)
* [Troubleshooting](#troubleshooting)
* [Contributing](#contributing)
* [License](#license)

---

## Features

* **Natural Language Ordering**
  The bot uses OpenAI’s Chat API (e.g., `gpt-3.5-turbo`) to understand and respond in a conversational style.
* **Menu Clarification**
  Automatically asks for size, toppings, and extras to uniquely identify each pizza or side.
* **Pickup vs. Delivery**
  Prompts the user to specify pickup or delivery. If delivery is chosen, collects the address.
* **Order Summary**
  Provides a JSON-formatted summary that itemizes pizzas (with sizes), toppings, drinks (with sizes), sides (with sizes), and total price.
* **Reset Conversation**
  Allows resetting the entire context so a new customer can start fresh.

---

## Prerequisites

* **Python 3.7+** (with `pip`)
* **Node.js 14+** and **npm**
* An **OpenAI API Key**
* Basic familiarity with Flask, Express, and environment variables

---

## Project Structure

```
.
├── orderbot.py       # Flask app that handles chat, summary, and reset endpoints
├── server.js         # Express server to serve the front-end files
├── index.html        # Front-end UI for interacting with the pizza bot
├── .env              # Environment variables (not committed)
├── package.json      # Node.js dependencies for server.js
├── requirements.txt  # Python dependencies for orderbot.py
└── README.md         # This file
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/pizza-order-bot.git
cd pizza-order-bot
```

### 2. Backend Setup (Flask)

1. Create and activate a virtual environment (recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your OpenAI API key:

   ```dotenv
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   Make sure to replace `your_openai_api_key_here` with your actual key.

### 3. Frontend Setup (Node.js)

1. Install Node.js dependencies:

   ```bash
   npm install
   ```

   *(This installs Express listed in `package.json`.)*

2. (Optional) If you don’t have a `package.json`, run:

   ```bash
   npm init -y
   npm install express
   ```

---

## Configuration

* **Flask App (`orderbot.py`)**

  * Listens on port **5000** by default.
  * Uses `python-dotenv` to load `OPENAI_API_KEY` from `.env`.
  * Endpoints:

    * `POST /chat` – sends user messages to OpenAI and returns Bot responses.
    * `GET /summary` – returns a JSON summary of the collected order.
    * `POST /reset` – resets the conversation context to its initial system message.

* **Express Server (`server.js`)**

  * Serves static files (including `index.html`, CSS, JS) on port **3000**.
  * No additional configuration is needed beyond having `index.html` in the same directory.

---

## Usage

### Starting the Flask Server

1. Activate your virtual environment (if not already active):

   ```bash
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

2. Run the Flask app:

   ```bash
   python orderbot.py
   ```

   You should see:

   ```
   * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
   ```

### Starting the Node Server

In a separate terminal (no need for the Python virtual environment):

```bash
node server.js
```

You should see:

```
Server running at http://localhost:3000
Make sure the Python Flask server is also running at http://localhost:5000
```

### Interacting with the Bot

1. Open your browser and navigate to:

   ```
   http://localhost:3000/
   ```

2. You’ll see the PizzaBot Assistant UI.

   * The bot greets you automatically.
   * Type your messages in the input field and click “Send” (or press Enter).
   * The bot will collect your order item by item.

3. **Get Order Summary**

   * Click the “Get Order Summary” button.
   * A pane will appear showing a JSON object with:

     1. **pizza** (with size)
     2. **toppings**
     3. **drinks** (with size)
     4. **sides** (with size)
     5. **total price**

4. **Reset Conversation**

   * Click “Reset Conversation” to clear the chat window and start over.
   * The context is reset to the initial system prompt.

### Endpoints

* **`POST http://localhost:5000/chat`**

  * **Request JSON**: `{ "message": "<user message>" }`
  * **Response JSON**: `{ "response": "<bot reply>" }`

* **`GET http://localhost:5000/summary`**

  * **Response**: JSON summary of the complete order. If the LLM fails to produce valid JSON, returns `{ "summary": "<raw text>" }`.

* **`POST http://localhost:5000/reset`**

  * **Response**: `{ "status": "conversation reset" }`

---

## Environment Variables

Ensure you have a `.env` file in the project root containing:

```dotenv
OPENAI_API_KEY=your_openai_api_key_here
```

* **`OPENAI_API_KEY`**
  Required to authenticate with OpenAI’s API for chat completions.

---

## Customization

1. **Menu and Pricing**

   * Modify the `context` variable in `orderbot.py` (the system prompt) to update menu items, prices, or add/remove toppings and sides.
   * Example snippet from `orderbot.py`:

     ```python
     context = [{
         'role': 'system',
         'content': """
         You are OrderBot, an automated service to collect orders for a pizza restaurant. 
         … (existing instructions) …
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
     ```

2. **Model Selection & Temperature**

   * By default, the bot uses `gpt-3.5-turbo` with temperature `1` for creative responses.
   * To switch to `gpt-4` (if enabled for your API key) or adjust temperature, update the `get_completion_from_messages` call:

     ```python
     def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=1):
         response = client.chat.completions.create(
             model=model,
             messages=messages,
             temperature=temperature,
         )
         return response.choices[0].message.content
     ```

3. **Frontend Styling**

   * `index.html` uses [Tailwind CSS](https://tailwindcss.com/) for styling and Font Awesome for icons.
   * Adjust classes or add your own CSS rules under `<style>` or link another stylesheet.

---

## Troubleshooting

* **CORS Errors**

  * Ensure the Flask server is running on `http://localhost:5000` and includes `CORS(app)`.
  * Check that you’re calling `fetch('http://localhost:5000/chat', …)` exactly as shown.

* **Environment Variable Not Found**

  * Confirm that `.env` is in the same directory as `orderbot.py`.
  * Run `echo $OPENAI_API_KEY` (or `printenv OPENAI_API_KEY` on Linux/macOS) to check if it’s set.
  * If missing, reinstall `python-dotenv`:

    ```bash
    pip install python-dotenv
    ```

* **Port Conflicts**

  * If port **5000** or **3000** is already in use, either stop the conflicting service or modify `orderbot.py`/`server.js` to listen on different ports.

* **Invalid JSON Summary**

  * Occasionally the LLM may produce non-JSON output. In that case, you’ll see a raw `{"summary": "…"}` response.
  * Double-check that the system prompt for summary (in `get_summary`) is correct:

    ```python
    summary_message = {
        'role': 'system',
        'content': 'create a json summary of the previous food order. Itemize the price for each item. The fields should be 1) pizza, include size 2) list of toppings 3) list of drinks, include size 4) list of sides include size 5)total price'
    }
    ```

---

## Contributing

1. Fork this repository.
2. Create a new branch for your feature or bug fix:

   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes and ensure the project still runs without errors.
4. Commit your work:

   ```bash
   git commit -m "Add feature: describe what you added"
   ```
5. Push to your fork:

   ```bash
   git push origin feature/your-feature-name
   ```
6. Open a Pull Request with a clear description of your changes.

---

## License

This project is released under the [MIT License](LICENSE). Feel free to use, modify, and distribute.

---

> **Enjoy building and customizing your own LLM-based pizza ordering bot! 🍕🤖**
