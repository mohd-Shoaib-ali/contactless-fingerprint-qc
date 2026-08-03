from quality_assessment import load_image, quality_gate

image = load_image("test_dataset/good/good_01.jpeg")

result = quality_gate(image)

print(result)

