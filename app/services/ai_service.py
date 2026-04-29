import torch
from torchvision import models
from PIL import Image

weights = models.MobileNet_V2_Weights.DEFAULT
model = models.mobilenet_v2(weights=weights)
model.eval()

categories = weights.meta["categories"]
transform = weights.transforms()


FOOD_LABELS = {
    # frutas
    "apple": "apple",
    "granny smith": "apple",
    "banana": "banana",
    "orange": "orange",
    "lemon": "orange",
    "strawberry": "strawberry",
    "pineapple": "pineapple",
    "pomegranate": "pomegranate",
    "fig": "fig",

    # verduras
    "broccoli": "broccoli",
    "cauliflower": "broccoli",
    "cucumber": "cucumber",
    "zucchini": "zucchini",
    "bell pepper": "pepper",
    "mushroom": "mushroom",
    "artichoke": "artichoke",

    # comida preparada
    "pizza": "pizza",
    "cheeseburger": "hamburger",
    "hamburger": "hamburger",
    "hotdog": "sandwich",
    "burrito": "burrito",
    "guacamole": "guacamole",

    # pan / bollería / dulces
    "bagel": "bread",
    "pretzel": "bread",
    "French loaf": "bread",
    "bakery": "bread",
    "ice cream": "ice_cream",
    "chocolate sauce": "chocolate",
    "espresso": "coffee",

    # proteínas / otros
    "meat loaf": "beef",
    "mashed potato": "potato",
    "carbonara": "pasta",
    "plate": "unknown",
}


def detect_food_with_ai(image_path):
    image = Image.open(image_path).convert("RGB")
    image_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)

    top_prob, top_index = torch.max(probabilities, dim=0)

    label = categories[top_index.item()].lower()
    score = float(top_prob.item())

    for keyword, food_key in FOOD_LABELS.items():
        if keyword.lower() in label:
            return food_key, score

    return "unknown", score