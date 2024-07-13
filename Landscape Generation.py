import csv
from io import BytesIO, StringIO
from PIL import Image, ImageDraw, ImageFont
import requests
import textwrap
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def generate_image(name, price, image_url, total_sales_count, discount, avg_rating, description):
    # Set the dimensions of the product card
    card_width = 1000
    card_height = 700
    margin = int(card_width * 0.05)  # Calculate 5% margin

    # Create a new image with a white background
    card = Image.new("RGB", (card_width, card_height), color="white")
    draw = ImageDraw.Draw(card)

    # Download and resize the product image
    response = requests.get(image_url)
    product_image = Image.open(BytesIO(response.content))
    product_image.thumbnail((400, 400))

    # Calculate the position to place the product image
    image_x = 50
    image_y = 100

    # Paste the product image onto the card
    card.paste(product_image, (image_x, image_y))

    # Set the font and size for the text
    font_name = "D:\CN\Downloads\Montserrat-Bold.ttf"
    title_font_size = 32
    sub_font_size = 20
    price_font_size = 24
    description_font_size = 16
    title_font = ImageFont.truetype(font_name, title_font_size)
    sub_font = ImageFont.truetype(font_name, sub_font_size)
    price_font = ImageFont.truetype(font_name, price_font_size)
    description_font = ImageFont.truetype(font_name, description_font_size)

    # Set the text color
    text_color = (0, 0, 0)  # Black

    # Add the product name (wrapped)
    name_text = name
    name_lines = textwrap.wrap(name_text, width=28)
    name_x = image_x + 400 + 40
    name_y = image_y
    for line in name_lines:
        draw.text((name_x, name_y), line, font=title_font, fill=text_color)
        name_y += title_font_size + 10

    # Add the "Office Chair" subtitle
    sub_text = "Office Chair"
    sub_x = name_x
    sub_y = name_y
    

    # Add the price
    price_text = f"BDT {price}"
    price_x = name_x
    price_y = sub_y + sub_font_size + 10
    draw.text((price_x, price_y), price_text, font=price_font,fill=text_color)

    # Add the description (wrapped and truncated)
    if description:
        description_text = strip_tags(description)
        description_words = description_text.split()
        truncated_description = ' '.join(description_words[:50])
        description_lines = textwrap.wrap(truncated_description, width=50)
        description_y = price_y + price_font_size + 20
        for line in description_lines:
            draw.text((name_x, description_y), line, font=description_font, fill=text_color)
            description_y += description_font_size + 5

    # Add the stock status
    stock_text = "In stock (Delivery in 1-3 days)"
    stock_x = name_x
    stock_y = description_y + 20
    draw.text((stock_x, stock_y), stock_text, font=description_font, fill="#177300")

    # Add the star ratings
    if avg_rating:
        star_size = 16
        star_spacing = 4
        star_y = stock_y + description_font_size + 10
        
    # Add the number of sales
    if total_sales_count:
        reviews_text = f"({total_sales_count}pcs Sold)"
        reviews_x = name_x
        reviews_y = star_y
        draw.text((reviews_x, reviews_y), reviews_text, font=description_font, fill=text_color)

    # Add the recommended by section
    recommend_text = "Brought to you by"
    recommend_x = 50
    recommend_y = card_height - 150
    draw.text((recommend_x, recommend_y), recommend_text, font=description_font, fill=text_color)

    recommender_text = "CubeNation Bangladesh"
    recommender_x = recommend_x
    recommender_y = recommend_y + description_font_size + 5
    draw.text((recommender_x, recommender_y), recommender_text, font=sub_font, fill="#8a0000")

    # Add the order button
    button_text = "Order Today"
    button_width = 150
    button_height = 40
    button_x = card_width - button_width - margin
    button_y = card_height - 150
    button_rect = [(button_x, button_y), (button_x + button_width, button_y + button_height)]
    draw.rectangle(button_rect, fill="#8a0000")
    button_font = ImageFont.truetype(font_name, 16)
    button_bbox = button_font.getbbox(button_text)
    button_text_width = button_bbox[2] - button_bbox[0]
    button_text_height = button_bbox[3] - button_bbox[1]
    button_text_x = button_x + (button_width - button_text_width) // 2
    button_text_y = button_y + (button_height - button_text_height) // 2
    draw.text((button_text_x, button_text_y), button_text, font=button_font, fill="white")

    # Save the modified image
    card.save(f"D:/CN/Downloads/socialproduct/{name}.jpg")

# Read the CSV file
with open("D:\CN\Downloads\imagedata1.csv", "r") as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        name = row["title"]
        price = row["originalPrice"]
        image_url = row["image"]
        total_sales_count = row["totalSalesCount"]
        discount = row["discount"]
        avg_rating = row["avgRating"]
        description = row["description"]

        generate_image(name, price, image_url, total_sales_count, discount, avg_rating, description)