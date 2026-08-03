from quality_assessment import load_image

image = load_image("test_dataset/good/good_01.jpeg")

print(type(image))
print(image.shape)