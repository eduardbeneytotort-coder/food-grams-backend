import asyncio

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from app.services.image_service import save_uploaded_file, process_image, get_average_color
from app.services.food_service import detect_food_smart, get_food_info
from app.services.ai_service import detect_food_with_ai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://127.0.0.1",
    ],
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1):\d+$",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


PORTION_MULTIPLIERS = {
    "small": 0.7,
    "medium": 1.0,
    "large": 1.4,
}


@app.get("/")
def home():
    return {"message": "API funcionando correctamente"}


@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    portion_size: str = Form("medium")
):
    file_content = await file.read()

    file_path = save_uploaded_file(file, file_content)
    process_image(file_path, file.filename)

    color_data = get_average_color(file_path)

    try:
        ai_food, ai_confidence = await asyncio.wait_for(
            asyncio.to_thread(detect_food_with_ai, file_path),
            timeout=8
        )
    except Exception:
        ai_food = "unknown"
        ai_confidence = 0.0

    if ai_food != "unknown" and ai_confidence > 0.5:
        food_name = ai_food
        confidence = ai_confidence
    else:
        food_name, confidence = detect_food_smart(
            file.filename,
            color_data["avg_red"],
            color_data["avg_green"],
            color_data["avg_blue"]
        )

    food_info = get_food_info(food_name)

    multiplier = PORTION_MULTIPLIERS.get(portion_size, 1.0)

    estimated_grams = round(food_info["grams"] * multiplier)
    estimated_calories = round(food_info["calories"] * multiplier)

    return {
        "food": food_name,
        "name_es": food_info["name_es"],
        "portion_size": portion_size,
        "estimated_grams": estimated_grams,
        "calories": estimated_calories,
        "confidence": confidence
    }