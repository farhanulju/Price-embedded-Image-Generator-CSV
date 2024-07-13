import csv
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import requests
import textwrap

def generate_image(name, price, image_url):
    # Set the dimensions of the product card
    card_width = 1000
    card_height = 1200

    # Create a new image with a white background
    card = Image.new("RGB", (card_width, card_height), color="white")
    draw = ImageDraw.Draw(card)

    # Download and resize the product image
    response = requests.get(image_url)
    product_image = Image.open(BytesIO(response.content))
    product_image.thumbnail((800, 800))

    # Calculate the position to center the product image
    image_x = (card_width - product_image.width) // 2
    image_y = 50

    # Paste the product image onto the card
    card.paste(product_image, (image_x, image_y))

    # Set the font and size for the text
    font_name = "D:\CN\Downloads\Montserrat-Bold.ttf"
    title_font_size = 32
    price_font_size = 40
    title_font = ImageFont.truetype(font_name, title_font_size)
    price_font = ImageFont.truetype(font_name, price_font_size)

    # Set the text color
    text_color = (0, 0, 0)  # Black

    # Add the product name (wrapped)
    name_text = name
    name_lines = textwrap.wrap(name_text, width=40)
    name_y = image_y + product_image.height + 50
    for line in name_lines:
        line_bbox = title_font.getbbox(line)
        line_width = line_bbox[2] - line_bbox[0]
        line_height = line_bbox[3] - line_bbox[1]
        line_x = (card_width - line_width) // 2
        draw.text((line_x, name_y), line, font=title_font, fill=text_color)
        name_y += line_height + 10

    # Add the price
    price_text = f"BDT {price}"
    price_bbox = price_font.getbbox(price_text)
    price_width = price_bbox[2] - price_bbox[0]
    price_x = (card_width - price_width) // 2
    price_y = name_y + 50
    draw.text((price_x, price_y), price_text, font=price_font, fill=text_color)

    # Save the modified image
    card.save(f"D:/CN/Downloads/socialproduct/{name}.jpg")

# Read the CSV file
with open("D:\CN\Downloads\imagedata.csv", "r") as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        name = row["Name"]
        price = row["Price"]
        image_url = row["Image"]

        generate_image(name, price, image_url)