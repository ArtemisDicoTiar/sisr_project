from PIL import Image
import pytesseract


d_image = Image.open('../../../test_images/downSampled.jpg')
d_text = pytesseract.image_to_string(d_image, lang='eng')

print(d_text)

image = Image.open('../../../test_images/Interpolations/lanczos.jpg')
text = pytesseract.image_to_string(image, lang='eng')

print(text)
