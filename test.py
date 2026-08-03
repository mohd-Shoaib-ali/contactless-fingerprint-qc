from quality_assessment import (
    load_image,
    check_blur,
    check_brightness
)

image = load_image("test_dataset/good/good_01.jpeg")

print("\n===== BLUR =====")
print(check_blur(image, threshold=5))

print("\n===== BRIGHTNESS =====")
print(check_brightness(image))