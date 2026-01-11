# trips_domain.py
import re

# ================= TRIPS KNOWLEDGE =================
TRIPS_PLACES = {
    "hunza": {
        "about": "Hunza is famous for mountains, lakes and peaceful views.",
        "best_time": "April to October"
    },
    "swat": {
        "about": "Swat is known as the Switzerland of Pakistan.",
        "best_time": "May to September"
    },
    "murree": {
        "about": "Murree is popular for family trips and snowfall.",
        "best_time": "December to February"
    },
    "nathia gali": {
        "about": "Nathia Gali is known for hiking trails and cool weather.",
        "best_time": "June to August"
    },
    "shogran": {
        "about": "Shogran is famous for Siri Paye meadows.",
        "best_time": "May to September"
    },
    "abbottabad": {
        "about": "Abbottabad has pleasant weather and greenery.",
        "best_time": "March to October"
    }
}

BOOKING_SITES = [
    "Airbnb",
    "Booking.com",
    "Agoda"
]

# ================= ENTITY EXTRACTION =================
def extract_trips_entities(text):
    text = text.lower()

    place = next((p for p in TRIPS_PLACES if p in text), None)

    want_hotel = bool(re.search(r"hotel|stay|room|booking|book", text))
    want_time = bool(re.search(r"best time|when|season", text))

    return {
        "place": place,
        "hotel": want_hotel,
        "time": want_time
    }

# ================= TRIPS HANDLER =================
def handle_trips(user_input, context):
    text = user_input.lower()
    entities = extract_trips_entities(text)

    # save place in context
    if entities["place"]:
        context["trip_place"] = entities["place"]

        info = TRIPS_PLACES[entities["place"]]
        return (
            f" {entities['place'].title()} Trip\n"
            f"{info['about']}\n"
            f"Best time to visit: {info['best_time']}\n\n"
            f"Would you like stay details or travel season info?",
            "trips"
        )

    # hotel / stay request
    if entities["hotel"]:
        return (
            " You can book stays from:\n"
            "- Airbnb\n"
            "- Booking.com\n"
            "- Agoda\n\n"
            "These websites offer hotels & guest houses.",
            "trips"
        )

    # best time request
    if entities["time"] and context.get("trip_place"):
        place = context["trip_place"]
        return (
            f"📅 Best time to visit {place.title()} is "
            f"{TRIPS_PLACES[place]['best_time']}.",
            "trips"
        )

    # fallback inside trips
    return (
        "Which northern area are you planning to visit?\n"
        "Hunza, Swat, Murree, Nathia Gali, Shogran or Abbottabad?",
        "trips"
    )
