def flight_bot(user_input):
    user_input = user_input.lower().strip()

    # city mapping for abbreviations
    city_map = {
        "pta": "peshawar",
        "isb": "islamabad",
        "khi": "karachi",
        "lhr": "lahore",
        "multa": "multan"  # just in case typo
    }

    # replace abbreviation with full city name
    for abbr, full in city_map.items():
        if abbr in user_input:
            user_input = user_input.replace(abbr, full)

    # ===== FLIGHT START =====
    if any(x in user_input for x in ["flight", "flights", "air ticket", "book flight", "travel"]):
        return "Sure, are you traveling domestic or international?"

    # ===== FLIGHT TYPE =====
    elif "domestic" in user_input:
        return "Great, from which city are you flying? (Karachi / Islamabad / Lahore / Multan / Peshawar)"

    elif "international" in user_input:
        return "International flights coming soon. Currently I can help with domestic flights."

    # ===== SOURCE / DESTINATION CITY =====
    elif user_input in ["karachi", "islamabad", "lahore", "multan", "peshawar"]:
        return "Nice, where do you want to go?"

    elif any(city in user_input for city in ["karachi", "islamabad", "lahore", "multan", "peshawar"]):
        return "When do you want to travel? (Today / Tomorrow / Choose date)"

    # ===== DATE =====
    elif any(x in user_input for x in ["today", "tomorrow"]):
        return "Which class do you prefer? (Economy / Business)"

    # ===== CLASS =====
    elif "economy" in user_input:
        return (
            "Economy class \n"
            "Available airlines:\n"
            "- PIA\n"
            "- Airblue\n"
            "- Serene Air\n"
            "- Fly Jinnah\n"
            "Would you like the cheapest option?"
        )

    elif "business" in user_input:
        return (
            "Business class \n"
            "Available airlines:\n"
            "- PIA\n"
            "- Airblue\n"
            "Would you like the best timing option?"
        )

    # ===== CHEAP / BEST OPTION =====
    elif any(x in user_input for x in ["cheap", "cheapest", "budget"]):
        return (
            "Cheapest flights suggestion:\n"
            "- Fly Jinnah\n"
            "- Airblue\n"
            "Prices usually start from PKR 15,000 – 42,000 depending on route & date."
        )

    elif any(x in user_input for x in ["best", "timing", "comfortable"]):
        return (
            "Best experience airlines:\n"
            "- PIA\n"
            "- Serene Air\n"
            "These offer better timings & comfort."
        )

    # ===== BOOKING =====
    elif any(x in user_input for x in ["book", "booking", "reserve"]):
        return (
            "Sure, please book from the airline’s official website.\n"
            "If not available, check:\n"
            "- Google Flights\n"
            "- Sastaticket\n"
            "- Bookme.pk"
        )

    # ===== THANKS =====
    elif any(x in user_input for x in ["thanks", "thank you", "thanks bud"]):
        return "No worries,I’m here to help. Safe travels!"

    # ===== FALLBACK =====
    else:
        return None  # important to allow food domain fallback
