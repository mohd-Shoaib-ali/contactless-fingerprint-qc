from quality_assessment import load_image, check_blur

image = load_image("test_dataset/blurry/blur_01.jpeg")

print(check_blur(image))