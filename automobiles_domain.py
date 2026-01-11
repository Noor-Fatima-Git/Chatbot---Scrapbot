# automobiles_domain.py

CARS = {
    "sedan": {
        "models": ["Toyota Corolla", "Honda Civic", "Hyundai Elantra"],
        "price": "PKR 45 – 80 lacs",
        "fuel": ["petrol", "hybrid"]
    },
    "suv": {
        "models": ["Toyota Fortuner", "KIA Sportage", "Honda BR-V"],
        "price": "PKR 60 – 150 lacs",
        "fuel": ["petrol", "hybrid"]
    },
    "hatchback": {
        "models": ["Suzuki Alto", "Toyota Yaris"],
        "price": "PKR 25 – 45 lacs",
        "fuel": ["petrol"]
    },
    "electric": {
        "models": ["MG ZS EV", "Audi e-tron"],
        "price": "PKR 90 – 250 lacs",
        "fuel": ["electric"]
    }
}

def handle_automobile(user_input, context):
    text = user_input.lower()

    types = ["sedan", "suv", "hatchback", "electric"]
    fuels = ["petrol", "hybrid", "electric"]

    car_type = next((t for t in types if t in text), None)
    fuel = next((f for f in fuels if f in text), None)

    if car_type:
        context["auto_type"] = car_type

    if fuel:
        context["auto_fuel"] = fuel

    if not context.get("auto_type"):
        return (
            "What type of car are you looking for?\n"
            "Sedan, SUV, Hatchback or Electric?",
            "automobile"
        )

    data = CARS[context["auto_type"]]

    reply = (
        f"Car type: {context['auto_type'].title()}\n"
        f"Popular models:\n"
    )

    for m in data["models"]:
        reply += f"- {m}\n"

    reply += f"Price range: {data['price']}\n"
    reply += f"Available fuel types: {', '.join(data['fuel'])}\n"
    reply += "Would you like buying websites or comparison advice?"

    return reply.strip(), "automobile"
