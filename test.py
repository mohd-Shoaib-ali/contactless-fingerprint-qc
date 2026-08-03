from quality_assessment import load_image, check_blur

image = load_image("test_dataset/good/good_01.jpeg")

result = check_blur(image, threshold=5)

print("\n===== BLUR TEST =====")
print(f"Blur Score : {result['blur_score']}")
print(f"Is Blurry  : {result['is_blurry']}")