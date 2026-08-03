import cv2

image = cv2.imread("test_dataset/good/good_01.jpeg")

blurred = cv2.GaussianBlur(image, (25, 25), 0)

cv2.imwrite("test_dataset/blurry/blur_01.jpeg", blurred)

print("Blurred image saved!")