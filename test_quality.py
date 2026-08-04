import os
import pandas as pd

from quality_assessment import quality_gate

DATASET_FOLDER = "test_dataset"

CATEGORIES = [
    "good",
    "blurry",
    "dark",
    "glare"
]

results = []

print("=" * 70)
print(" Contactless Fingerprint Quality Assessment - Batch Test")
print("=" * 70)

for category in CATEGORIES:

    folder = os.path.join(DATASET_FOLDER, category)

    if not os.path.exists(folder):
        print(f"Folder not found: {folder}")
        continue

    print(f"\nProcessing {category} images...")

    for file in os.listdir(folder):

        if not file.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        image_path = os.path.join(folder, file)

        try:

            result = quality_gate(image_path)

            results.append({

                "Image": file,
                "Category": category,

                "Blur Score": result["blur"]["blur_score"],

                "Brightness": result["brightness"]["brightness"],

                "Glare Ratio": result["glare"]["glare_ratio"],

                "ROI Ratio": result["roi"]["roi_ratio"],

                "Ridge Score": result["ridge"]["ridge_score"],

                "Composite Score": result["composite_score"],

                "Passed": result["passed"],

                "Guidance": result["guidance"]

            })

            print(f"✓ {file}")

        except Exception as e:

            print(f"✗ {file} -> {e}")

df = pd.DataFrame(results)

df.to_csv("test_results.csv", index=False)

print("\n")
print("=" * 70)
print("Testing Complete")
print("=" * 70)

print(df)

print("\nCSV saved as test_results.csv")

