# entities.py
import re

FOODS = ["biryani", "burger", "pizza", "ice cream", "shake", "sundae", "dessert"]
FOOD_CITIES = ["islamabad", "rawalpindi"]

TRIP_PLACES = [
    "hunza", "swat", "murree",
    "nathia gali", "shogran", "abbottabad"
]

def extract_food_entities(text):
    text = text.lower()
    return {
        "food": next((f for f in FOODS if f in text), None),
        "city": next((c for c in FOOD_CITIES if c in text), None)
    }

def extract_trip_entities(text):
    text = text.lower()
    return {
        "place": next((p for p in TRIP_PLACES if p in text), None),
        "hotel": bool(re.search(r"hotel|stay|room|booking", text)),
        "time": bool(re.search(r"best time|season|when", text))
    }
