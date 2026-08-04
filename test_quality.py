import os
import pandas as pd

from quality_assessment import quality_gate

DATASET_FOLDER = "test_dataset"

results = []

categories = [
    "good",
    "blurry",
    "dark",
    "glare"
]

for category in categories:

    folder = os.path.join(DATASET_FOLDER, category)

    if not os.path.exists(folder):
        continue

    for filename in os.listdir(folder):

        if filename.lower().endswith((".jpg", ".jpeg", ".png")):

            image_path = os.path.join(folder, filename)

            result = quality_gate(image_path)

            results.append({

                "Image": filename,

                "Category": category,

                "Composite Score": result["composite_score"],

                "Passed": result["passed"],

                "Guidance": result["guidance"]

            })

df = pd.DataFrame(results)

df.to_csv("test_results.csv", index=False)

print(df)

print("\nResults saved to test_results.csv")