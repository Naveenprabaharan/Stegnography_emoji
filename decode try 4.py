from PIL import Image
import string

def extract_text_from_image_ilsb(image_path):
    image = Image.open(image_path)
    width, height = image.size
    binary_text = ''

    pixels = image.load()
    binary_index = 0

    for row in range(height):
        for col in range(width):
            pixel = pixels[col, row]
            for channel_value in pixel[:3]:  # Iterate over RGB channels
                binary_text += str(channel_value & 1)
                binary_index += 1

                if binary_index >= 8 and binary_text[-8:] == '00000000':
                    return binary_text_to_text(binary_text[:-8])

    return binary_text_to_text(binary_text)

def binary_text_to_text(binary_text):
    print('binary_text : ',len(binary_text))

    # binary_text = binary_text.ljust(8 * ((len(binary_text) + 7) // 8), '0')  # Pad binary text with zeros
    print('after ',len(binary_text))
    text = ''
    for i in range(0, len(binary_text), 8):
        byte = binary_text[i:i+8]
        text += chr(int(byte, 2))
    return text

# Test the code
hidden_message = extract_text_from_image_ilsb(r"hidden_image2.png")
print(hidden_message)
