from PIL import Image
import os

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"

def save_uploaded_file(file, file_content):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(file_content)

    return file_path

def process_image(file_path, original_filename):
    image = Image.open(file_path)
    original_width, original_height = image.size
    image_format = image.format

    resized_image = image.resize((300, 300))

    processed_filename = f"processed_{original_filename}"
    processed_path = os.path.join(PROCESSED_FOLDER, processed_filename)
    resized_image.save(processed_path)

    return {
        "original_width": original_width,
        "original_height": original_height,
        "format": image_format,
        "processed_filename": processed_filename,
        "new_width": 300,
        "new_height": 300
    }

def get_average_color(file_path):
    image = Image.open(file_path)
    image = image.resize((50, 50))

    pixels = list(image.getdata())

    r_total = 0
    g_total = 0
    b_total = 0

    for pixel in pixels:
        r, g, b = pixel[:3]
        r_total += r
        g_total += g
        b_total += b

    total_pixels = len(pixels)

    avg_r = int(r_total / total_pixels)
    avg_g = int(g_total / total_pixels)
    avg_b = int(b_total / total_pixels)

    return {
        "avg_red": avg_r,
        "avg_green": avg_g,
        "avg_blue": avg_b
    }