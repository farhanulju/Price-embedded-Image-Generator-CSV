# Product Card Generator

This Python script generates product cards by combining product information from a CSV file with corresponding product images. The generated product cards are saved as individual image files.

## Prerequisites

- Python 3.x
- PIL (Python Imaging Library)
- requests

## Installation

1. Clone the repository or download the script file.

2. Install the required dependencies by running the following command:
   ```
   pip install pillow requests
   ```

## Usage

1. Prepare a CSV file named `imagedata.csv` with the following columns:
   - Name: The name of the product.
   - Price: The price of the product.
   - Image: The URL of the product image.

   Example CSV file:
   ```
   Name,Price,Image
   Product 1,100,https://example.com/product1.jpg
   Product 2,200,https://example.com/product2.jpg
   ```

2. Update the following variables in the script:
   - `font_name`: The path to the font file (e.g., "D:\CN\Downloads\Montserrat-Bold.ttf").
   - Output directory: Modify the path in the `card.save()` function to specify the desired output directory for the generated product card images.

3. Run the script:
   ```
   python product_card_generator.py
   ```

   The script will read the product information from the CSV file, download the corresponding product images, and generate individual product card images. The generated images will be saved in the specified output directory.

## Customization

You can customize the appearance of the product cards by modifying the following variables in the script:

- `card_width` and `card_height`: The dimensions of the product card image.
- `title_font_size` and `price_font_size`: The font sizes for the product name and price.
- `text_color`: The color of the text on the product card.

Feel free to adjust these variables to suit your desired design.

## License

This script is released under the [MIT License](LICENSE).
