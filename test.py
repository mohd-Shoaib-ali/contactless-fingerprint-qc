from quality_assessment import (
    load_image,
    check_blur,
    check_brightness,
    check_glare
)

image = load_image("test_dataset/good/good_01.jpeg")

print("\n===== BLUR =====")
print(check_blur(image, threshold=5))

print("\n===== BRIGHTNESS =====")
print(check_brightness(image))

print("\n===== GLARE =====")
print(check_glare(image))

image = load_image("test_dataset/glare/glare_01.jpeg")

print(check_glare(image))