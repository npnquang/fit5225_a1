import base64

# Path to your image
image_path = 'images/image1.jpeg'
# Path where you want to save the Base64 encoded content
output_txt_path = 'encoded_image.txt'

# Open the image in binary mode and encode to base64
with open(image_path, 'rb') as image_file:
    # Read the image as binary and encode it to base64
    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

# Write the Base64 encoded string to a text file
with open(output_txt_path, 'w') as output_file:
    output_file.write(encoded_image)

print(f"Base64 encoded image has been written to {output_txt_path}")