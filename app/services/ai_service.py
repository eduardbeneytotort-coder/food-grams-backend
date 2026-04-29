from transformers import pipeline

# Carga el modelo (la primera vez tarda)
image_classifier = pipeline(
    "image-classification",
    model="google/vit-base-patch16-224"
)


def detect_food_with_ai(image_path):
    results = image_classifier(image_path)

    if not results:
        return "unknown", 0.0

    best_result = results[0]
    label = best_result["label"].lower()
    score = float(best_result["score"])

    if "apple" in label:
        return "apple", score

    if "banana" in label:
        return "banana", score

    if "rice" in label:
        return "rice", score

    if "tomato" in label:
        return "tomato", score

    if "bread" in label:
        return "bread", score

    if "lettuce" in label or "cabbage" in label:
        return "lettuce", score

    return "unknown", score