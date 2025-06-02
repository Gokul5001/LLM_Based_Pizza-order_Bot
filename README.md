```markdown
# Pizza Order Bot

This project implements a simple “Pizza Order Bot” web application. It consists of:

- **Backend (Flask + OpenAI)**: A Python Flask server (`orderbot.py`) that uses the OpenAI API to handle conversational ordering logic, summarize orders, and reset the conversation.
- **Frontend (Node/Express + HTML/CSS/JavaScript)**: A static HTML/CSS/JavaScript client (`index.html`) served via a lightweight Node/Express server (`server.js`) that provides a chat UI and interacts with the Flask backend.

---

## Table of Contents

1. [Prerequisites](#prerequisites)  
2. [Project Structure](#project-structure)  
3. [Setup & Installation](#setup--installation)  
   - [1. Clone the Repository](#1-clone-the-repository)  
   - [2. Configure the Flask Backend](#2-configure-the-flask-backend)  
   - [3. Configure the Node/Express Server](#3-configure-the-nodeexpress-server)  
4. [Environment Variables](#environment-variables)  
5. [Running the Application](#running-the-application)  
   - [1. Start the Flask Backend](#1-start-the-flask-backend)  
   - [2. Start the Node/Express Frontend Server](#2-start-the-nodeexpress-frontend-server)  
6. [Usage](#usage)  
   - [Chat Interface](#chat-interface)  
   - [Get Order Summary](#get-order-summary)  
   - [Reset Conversation](#reset-conversation)  
7. [API Endpoints](#api-endpoints)  
8. [Folder Structure](#folder-structure)  
9. [Troubleshooting](#troubleshooting)  
10. [License](#license)  

---

## Prerequisites

- **Python 3.7+** installed and added to your `PATH`  
- **Node.js & npm** (Node v14+ recommended)  
- An **OpenAI API key** (exported via environment variable)  
- Basic familiarity with command-line tools  

---

## Project Structure

```

pizza-order-bot/
│
├── backend/
│   ├── orderbot.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── server.js
│   ├── package.json
│   ├── package-lock.json
│   └── index.html
│
└── README.md

````

- `backend/` contains the Flask application (`orderbot.py`) and its dependencies.  
- `frontend/` contains the Node/Express static‐file server (`server.js`), the HTML/CSS/JS client (`index.html`), and its `package.json`.  

---

## Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/pizza-order-bot.git
cd pizza-order-bot
````

---

### 2. Configure the Flask Backend

1. **Navigate to the `backend/` folder**:

   ```bash
   cd backend
   ```

2. **Create a virtual environment (recommended)**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate      # macOS/Linux
   .\venv\Scripts\activate       # Windows
   ```

3. **Install Python dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   * If you don’t have a `requirements.txt` yet, create one with these lines:

     ```
     Flask
     flask-cors
     python-dotenv
     openai
     ```
   * Then run:

     ```bash
     pip install Flask flask-cors python-dotenv openai
     ```

4. **Copy `.env.example` to `.env` and set your OpenAI key**:

   ```bash
   cp .env.example .env
   ```

   * Edit `.env` and add:

     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```

---

### 3. Configure the Node/Express Server

1. **Open a new terminal and navigate to `frontend/`**:

   ```bash
   cd ../frontend
   ```

2. **Install Node dependencies**:

   ```bash
   npm install
   ```

   * If `package.json` already lists `"express"` as a dependency, `npm install` will grab it automatically.
   * Otherwise, run:

     ```bash
     npm init -y
     npm install express
     ```

3. **(Optional) Install CORS middleware for Node**
   If you plan to serve the API calls from the same origin, CORS isn’t strictly necessary in `server.js`. If you want to add it:

   ```bash
   npm install cors
   ```

   and in `server.js` add:

   ```js
   const cors = require('cors');
   app.use(cors());
   ```

---

## Environment Variables

* **`backend/.env`**

  * `OPENAI_API_KEY` — Your secret OpenAI API key.
    Make sure not to commit your real key to version control.

---

## Running the Application

### 1. Start the Flask Backend

From the `backend/` directory:

```bash
# If you haven’t already activated your venv, do so:
# source venv/bin/activate      # macOS/Linux
# .\venv\Scripts\activate       # Windows

python orderbot.py
```

You should see something like:

```
 * Serving Flask app "orderbot"
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

> **Note:** By default, Flask runs on port 5000.
> The Flask app exposes three routes:
>
> * `POST /chat` — Accepts `{ "message": "..." }` JSON and returns the bot’s response.
> * `GET  /summary` — Returns a JSON summary of the current order.
> * `POST /reset` — Resets the conversation context.

---

### 2. Start the Node/Express Frontend Server

Open a new terminal, navigate to `frontend/`, and run:

```bash
node server.js
```

You should see:

```
Server running at http://localhost:3000
Make sure the Python Flask server is also running at http://localhost:5000
```

This serves `index.html` (and any static assets) at `http://localhost:3000/`.

---

## Usage

1. **Open your browser** and go to:

   ```
   http://localhost:3000
   ```

2. You’ll see the PizzaBot chat UI. The bot greets you immediately:

   > “Hello! Welcome to our pizza restaurant. What would you like to order today?”

3. **Type a message** in the input box (e.g., “I’d like a large pepperoni pizza with extra cheese and a coke.”) and click **Send** (or press **Enter**).

4. The frontend will `POST` your message to `http://localhost:5000/chat`, receive the AI‐generated reply, and display it in the chat window.

5. Once you’ve built an order, click **Get Order Summary**. This button invokes `GET http://localhost:5000/summary` and shows you a JSON‐formatted summary (pizza, toppings, sides, drinks, total price).

6. To clear all conversation history and start fresh, click **Reset Conversation**, which sends `POST http://localhost:5000/reset`. The chat window will reset to the initial greeting.

---

## API Endpoints

### 1. `POST /chat`

* **URL**: `http://localhost:5000/chat`
* **Headers**: `Content-Type: application/json`
* **Body**:

  ```json
  {
    "message": "Your user message here"
  }
  ```
* **Response**:

  ```json
  {
    "response": "The bot’s reply text"
  }
  ```
* **Behavior**: The server appends the user message to the conversation context, calls OpenAI’s Chat Completion endpoint, appends the AI’s reply to context, and returns the reply as JSON.

---

### 2. `GET /summary`

* **URL**: `http://localhost:5000/summary`
* **Response** (success, JSON):

  ```json
  {
    "pizza": {
      "item": "pepperoni",
      "size": "large",
      "price": 12.95
    },
    "toppings": [
      { "name": "extra cheese", "price": 2.00 },
      { "name": "mushrooms", "price": 1.50 }
    ],
    "drinks": [
      { "item": "coke", "size": "medium", "price": 2.00 }
    ],
    "sides": [
      { "item": "fries", "size": "small", "price": 3.50 }
    ],
    "total_price": 21.95
  }
  ```

  * If the AI response is not valid JSON, the server returns:

    ```json
    {
      "summary": "Raw text response from AI"
    }
    ```

---

### 3. `POST /reset`

* **URL**: `http://localhost:5000/reset`
* **Headers**: `Content-Type: application/json` (empty body is fine)
* **Response**:

  ```json
  {
    "status": "conversation reset"
  }
  ```
* **Behavior**: Clears the in‐memory conversation context and reinstates the original system prompt. Subsequent `/chat` calls start fresh.

---

## Folder Structure

```
pizza-order-bot/
│
├── backend/
│   ├── .env.example             # Sample environment file
│   ├── orderbot.py              # Flask + OpenAI server
│   └── requirements.txt         # Python dependencies
│
├── frontend/
│   ├── index.html               # Main chat UI
│   ├── package.json             # Node.js dependencies
│   ├── server.js                # Express static‐file server
│   └── package-lock.json        # Lockfile (auto-generated)
│
└── README.md                    # Project documentation
```

---

## Troubleshooting

* **“Cannot connect to server” in UI**

  * Verify the Flask backend is running on `http://localhost:5000`.
  * Check console logs in both the browser DevTools and terminal windows for errors.

* **OpenAI API key invalid or missing**

  * Ensure `.env` has a valid `OPENAI_API_KEY` and that you restarted Flask after editing `.env`.
  * Your Python code uses `python-dotenv` so it picks up `OPENAI_API_KEY` from `.env`.

* **CORS issues**

  * By default, `orderbot.py` calls `CORS(app)`, allowing requests from `localhost:3000`.
  * If you host frontend elsewhere, adjust your CORS settings in `orderbot.py`:

    ```python
    CORS(app, origins=["http://your-frontend-domain.com"])
    ```

* **Port conflicts**

  * If port 5000 is in use, modify `orderbot.py`:

    ```python
    if __name__ == "__main__":
        app.run(port=YOUR_DESIRED_PORT)
    ```
  * Likewise, change `const port = 3000;` in `frontend/server.js` if port 3000 is occupied.

---

## License

This project is released under the [MIT License](LICENSE). Feel free to use, modify, and distribute as needed.

---

```
```
