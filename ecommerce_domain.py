# ecommerce_domain.py
import re

# ================= E-COMMERCE DATA =================
PRODUCTS = {
    "mobile": {
        "brands": ["Samsung", "Apple", "Infinix", "Xiaomi"],
        "price_range": "PKR 25,000 – 300,000"
    },
    "laptop": {
        "brands": ["HP", "Dell", "Lenovo", "Apple"],
        "price_range": "PKR 80,000 – 400,000"
    },
    "headphones": {
        "brands": ["Audionic", "Sony", "JBL"],
        "price_range": "PKR 3,000 – 40,000"
    },
    "watch": {
        "brands": ["Apple", "Samsung", "Xiaomi"],
        "price_range": "PKR 8,000 – 150,000"
    }
}

SHOPPING_SITES = [
    "Daraz.pk",
    "PriceOye.pk",
    "Telemart.pk",
    "Shophive.com"
]

# ================= ENTITY EXTRACTION =================
def extract_ecommerce_entities(text):
    text = text.lower()

    product = next((p for p in PRODUCTS if p in text), None)
    want_price = bool(re.search(r"price|cost|range", text))
    want_buy = bool(re.search(r"buy|order|purchase", text))

    return {
        "product": product,
        "price": want_price,
        "buy": want_buy
    }

# ================= E-COMMERCE HANDLER =================
def handle_ecommerce(user_input, context):
    text = user_input.lower()
    entities = extract_ecommerce_entities(text)

    # Save product in context
    if entities["product"]:
        context["ecommerce_product"] = entities["product"]
        info = PRODUCTS[entities["product"]]

        return (
            f"Product: {entities['product'].title()}\n"
            f"Popular brands: {', '.join(info['brands'])}\n"
            f"Price range: {info['price_range']}\n\n"
            f"Do you want buying options or price details?",
            "ecommerce"
        )

    # Price inquiry
    if entities["price"] and context.get("ecommerce_product"):
        product = context["ecommerce_product"]
        return (
            f"Price range for {product.title()} is "
            f"{PRODUCTS[product]['price_range']}.",
            "ecommerce"
        )

    # Buy request
    if entities["buy"] and context.get("ecommerce_product"):
        return (
            "You can buy from trusted websites:\n"
            "- Daraz.pk\n"
            "- PriceOye.pk\n"
            "- Telemart.pk\n"
            "- Shophive.com",
            "ecommerce"
        )

    # Fallback
    return (
        "What do you want to shop for?\n"
        "Mobile, Laptop, Headphones or Watch?",
        "ecommerce"
    )
