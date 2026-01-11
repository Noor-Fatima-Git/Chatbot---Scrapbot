import pickle

from rag.rag_engine import rag_answer

from flight_domain import flight_bot
from trips_domain import handle_trips
from ecommerce_domain import handle_ecommerce
from automobiles_domain import handle_automobile
from jobs_domain import handle_jobs

def normalize_domain(domain):
    return domain.lower() if domain else "food"

# ================= LOAD ML MODELS =================
with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("intent_model.pkl", "rb") as f:
    intent_model = pickle.load(f)

# ================= FOOD DATA =================
FOOD_PLACES = {
    "biryani": {
        "islamabad": ["Student Biryani – Rs 350", "Cheezious – Rs 420"],
        "rawalpindi": ["Tandoori Hut – Rs 300"]
    },
    "burger": {
        "islamabad": ["Howdy – Rs 550", "Burger Lab – Rs 600"],
        "rawalpindi": ["Daily Deli – Rs 520"]
    },
    "pizza": {
        "islamabad": ["14th Street – Rs 1800", "Broadway – Rs 1600"],
        "rawalpindi": ["Pizza Hut – Rs 1500"]
    },
    "sundae": {
        "islamabad": ["Layers – Rs 550", "F-10 Ice Cream – Rs 500"],
        "rawalpindi": ["Hico – Rs 300"]
    },
    "ice cream": {
        "islamabad": ["Cold Stone – Rs 600", "Baskin Robbins – Rs 650"],
        "rawalpindi": ["Hico – Rs 300"]
    },
    "shake": {
        "islamabad": ["Juice Land – Rs 350", "Gloria Jeans – Rs 500"],
        "rawalpindi": ["Juice Corner – Rs 250"]
    }
}

# ================= CONTEXT =================
context = {
    "domain": None,
    "food_item": None,
    "food_city": None,
    "food_mode": None,
    "trip_place": None,
    "ecommerce_product": None,
    "auto_type": None,
    "auto_action": None,
    "job_title": None
}

# ================= HELPERS =================
def reset_context():
    for k in context:
        context[k] = None

def extract_food(text):
    foods = ["biryani", "burger", "pizza", "sundae", "ice cream", "shake"]
    cities = ["islamabad", "rawalpindi"]
    food = next((f for f in foods if f in text), None)
    city = next((c for c in cities if c in text), None)
    return food, city

def is_knowledge_question(text):
    return any(k in text for k in [
        "what is", "define", "explain", "tell me about",
        "information", "details"
    ])

def is_action_query(text):
    return any(k in text for k in [
        "buy", "order", "job", "vacancy", "flight",
        "travel", "trip", "car", "restaurant", "price"
    ])

# ================= CHATBOT =================
def chatbot_response(user_input):
    text = user_input.lower().strip()

    # 🤖 Self‑identity responses
    if any(q in text for q in [
        "who are you",
        "what is your name",
        "your name",
        "who built you",
        "who created you"
    ]):
        return (
            "🤖 I am ScrapBot, an intelligent chatbot.\n"
            "I was built by Noor Fatima, Hoorain Fatima, and Abdul Sammad.\n"
            "Instructor: Mam Mamoona.\n"
            "I help with food, trips, flights, jobs, shopping,\n"
            "and knowledge‑based questions using AI‑powered retrieval (RAG).\n"
            "I understand questions, fetch knowledge, and respond intelligently."
        )

    # ⬇️ rest of your existing chatbot logic continues below


    # -------- EXIT --------
    
    if text in ["exit", "bye", "quit"]:
        return "Allah Hafiz"

    # -------- THANKS --------
    if text in ["thanks", "nice", "thank you"]:
        reset_context()
        return "You're welcome 😊"

    # ================= ML INTENT =================
    X = vectorizer.transform([text])
    probs = intent_model.predict_proba(X)[0]
    intent = intent_model.classes_[probs.argmax()]

    # ================= GREETING =================
    if intent == "greeting":
        return "Hello! How can I help you?"

    # ================= JOBS =================
    if any(k in text for k in ["job", "vacancy", "hiring", "career"]) or context["domain"] == "jobs":
        context["domain"] = "jobs"
        reply, d = handle_jobs(user_input, context)
        context["domain"] = d
        if d is None:
            reset_context()
        return reply

    # ================= AUTOMOBILE =================
    if any(k in text for k in ["car", "vehicle", "suv", "sedan"]) or context["domain"] == "automobile":
        context["domain"] = "automobile"
        reply, d = handle_automobile(user_input, context)
        context["domain"] = d
        if d is None:
            reset_context()
        return reply

    # ================= FLIGHTS =================
    if any(w in text for w in ["fly", "flight", "air ticket"]):
        reset_context()
        context["domain"] = "Flights"
        return flight_bot(user_input)

    if context["domain"] == "Flights":
        return flight_bot(user_input)

    # ================= TRIPS =================
    if any(k in text for k in ["trip", "travel", "hunza", "swat"]) or context["domain"] == "Trips":
        context["domain"] = "Trips"
        reply, d = handle_trips(user_input, context)
        context["domain"] = d
        if d is None:
            reset_context()
        return reply

    # ================= ECOMMERCE =================
    if any(k in text for k in ["buy", "shop", "mobile", "laptop"]) or context["domain"] == "Ecommerce":
        context["domain"] = "Ecommerce"
        reply, d = handle_ecommerce(user_input, context)
        context["domain"] = d
        if d is None:
            reset_context()
        return reply

    # ================= FOOD =================
    
    # ================= RAG (ONLY IF LOGIC FAILS) =================
    if is_knowledge_question(text) and not is_action_query(text):
        answer = rag_answer(text)
        if answer:
            return f"Here’s what I found 👇\n\n{answer}"

    food, city = extract_food(text)

    if intent == "food" or food or context["domain"] == "food":
        context["domain"] = "food"

        if food:
            context["food_item"] = food
        if city:
            context["food_city"] = city

        if "dine" in text:
            context["food_mode"] = "dine in"
        elif "order" in text or "delivery" in text:
            context["food_mode"] = "order"

        if not context["food_item"]:
            return "What would you like to eat?"

        if not context["food_mode"]:
            return "Do you want to dine in or order at home?"

        if not context["food_city"]:
            return "Which city are you in? Islamabad or Rawalpindi?"

        places = FOOD_PLACES.get(context["food_item"], {}).get(context["food_city"], [])

        if not places:
            reset_context()
            return "Sorry, no options found."

        reply = "Available options:\n" + "\n".join(f"- {p}" for p in places)
        reset_context()
        return reply

    
    # ================= FALLBACK =================
    return "I can help with food, shopping, trips, flights, automobiles, or jobs."
