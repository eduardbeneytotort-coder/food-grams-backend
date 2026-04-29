FOOD_DB = {
    "apple": {"name_es": "Manzana", "grams": 150, "calories": 78},
    "banana": {"name_es": "Plátano", "grams": 120, "calories": 105},
    "orange": {"name_es": "Naranja", "grams": 150, "calories": 70},
    "strawberry": {"name_es": "Fresas", "grams": 150, "calories": 48},
    "grapes": {"name_es": "Uvas", "grams": 150, "calories": 104},

    "rice": {"name_es": "Arroz", "grams": 180, "calories": 240},
    "pasta": {"name_es": "Pasta", "grams": 180, "calories": 280},
    "bread": {"name_es": "Pan", "grams": 80, "calories": 210},
    "potato": {"name_es": "Patata", "grams": 200, "calories": 154},
    "french fries": {"name_es": "Patatas fritas", "grams": 150, "calories": 470},

    "chicken": {"name_es": "Pollo", "grams": 150, "calories": 248},
    "beef": {"name_es": "Ternera", "grams": 150, "calories": 375},
    "pork": {"name_es": "Cerdo", "grams": 150, "calories": 360},
    "fish": {"name_es": "Pescado", "grams": 150, "calories": 180},
    "egg": {"name_es": "Huevo", "grams": 60, "calories": 90},

    "tomato": {"name_es": "Tomate", "grams": 100, "calories": 18},
    "lettuce": {"name_es": "Lechuga", "grams": 50, "calories": 8},
    "carrot": {"name_es": "Zanahoria", "grams": 100, "calories": 41},
    "broccoli": {"name_es": "Brócoli", "grams": 150, "calories": 52},
    "corn": {"name_es": "Maíz", "grams": 150, "calories": 144},

    "pizza": {"name_es": "Pizza", "grams": 180, "calories": 480},
    "hamburger": {"name_es": "Hamburguesa", "grams": 220, "calories": 600},
    "sandwich": {"name_es": "Sándwich", "grams": 180, "calories": 420},
    "salad": {"name_es": "Ensalada", "grams": 250, "calories": 180},
    "soup": {"name_es": "Sopa", "grams": 300, "calories": 150},

    "milk": {"name_es": "Leche", "grams": 250, "calories": 155},
    "yogurt": {"name_es": "Yogur", "grams": 125, "calories": 90},
    "cheese": {"name_es": "Queso", "grams": 40, "calories": 160},

    "cake": {"name_es": "Tarta", "grams": 120, "calories": 420},
    "cookie": {"name_es": "Galleta", "grams": 30, "calories": 150},
    "chocolate": {"name_es": "Chocolate", "grams": 40, "calories": 220},

    "unknown": {"name_es": "Desconocido", "grams": 0, "calories": 0},
}


FOOD_ALIASES = {
    "manzana": "apple",
    "platano": "banana",
    "plátano": "banana",
    "naranja": "orange",
    "fresa": "strawberry",
    "fresas": "strawberry",
    "uvas": "grapes",

    "arroz": "rice",
    "pasta": "pasta",
    "pan": "bread",
    "patata": "potato",
    "patatas": "potato",
    "patatas fritas": "french fries",

    "pollo": "chicken",
    "ternera": "beef",
    "carne": "beef",
    "cerdo": "pork",
    "pescado": "fish",
    "huevo": "egg",

    "tomate": "tomato",
    "lechuga": "lettuce",
    "zanahoria": "carrot",
    "brocoli": "broccoli",
    "brócoli": "broccoli",
    "maiz": "corn",
    "maíz": "corn",

    "pizza": "pizza",
    "hamburguesa": "hamburger",
    "sandwich": "sandwich",
    "sándwich": "sandwich",
    "ensalada": "salad",
    "sopa": "soup",

    "leche": "milk",
    "yogur": "yogurt",
    "yogurt": "yogurt",
    "queso": "cheese",

    "tarta": "cake",
    "pastel": "cake",
    "galleta": "cookie",
    "chocolate": "chocolate",
}


def get_food_info(food_name):
    return FOOD_DB.get(food_name, FOOD_DB["unknown"])


def detect_food(filename):
    filename = filename.lower()

    for alias, food_key in FOOD_ALIASES.items():
        if alias in filename:
            return food_key

    for food_key in FOOD_DB.keys():
        if food_key in filename:
            return food_key

    return "unknown"


def detect_food_by_color(avg_red, avg_green, avg_blue):
    if avg_red > 210 and avg_green > 210 and avg_blue > 210:
        return "rice"

    elif avg_red > 190 and avg_green < 130 and avg_blue < 130:
        return "tomato"

    elif avg_green > 170 and avg_red > 130 and avg_blue < 170:
        return "apple"

    elif avg_red > 160 and avg_green < 170:
        return "apple"

    elif avg_green > avg_red and avg_green > avg_blue and avg_red < 130:
        return "lettuce"

    elif avg_red > 180 and avg_green > 170 and avg_blue < 120:
        return "banana"

    elif avg_red > 140 and avg_green > 100 and avg_blue < 130:
        return "bread"

    else:
        return "unknown"


def detect_food_smart(filename, avg_red, avg_green, avg_blue):
    food_by_name = detect_food(filename)
    food_by_color = detect_food_by_color(avg_red, avg_green, avg_blue)

    if food_by_name != "unknown" and food_by_name == food_by_color:
        return food_by_name, 0.90

    if food_by_name != "unknown":
        return food_by_name, 0.70

    if food_by_color != "unknown":
        return food_by_color, 0.60

    return "unknown", 0.20