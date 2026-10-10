
import requests
import pandas as pd
import matplotlib.pyplot as plt

API_URL = "https://dummyjson.com/c/a817-36dc-4f5a-a1c8"


def fetch_scores():
    response = requests.get(API_URL, timeout=15)
    response.raise_for_status()
    data = response.json()

    if not isinstance(data, list):
        raise ValueError("Expected a JSON array of student scores.")

    records = []
    for item in data:
        if not isinstance(item, dict):
            continue

        name = item.get("student")
        score = item.get("score")

        if name is None or score is None:
            continue

        try:
            score = float(score)
        except (ValueError, TypeError):
            continue

        if not 0 <= score <= 100:
            continue

        records.append({
            "Student": str(name),
            "Score": score
        })

    if not records:
        raise ValueError("The API returned no valid student scores.")

    return pd.DataFrame(records)


def main():
    try:
        df = fetch_scores()
        average_score = df["Score"].mean()

        print("Student scores:")
        print(df.to_string(index=False))
        print(f"\nAverage score: {average_score:.2f}")

        plt.figure(figsize=(9, 5))
        plt.bar(df["Student"], df["Score"])
        plt.axhline(
            average_score,
            linestyle="--",
            label=f"Average: {average_score:.2f}"
        )
        plt.xlabel("Students")
        plt.ylabel("Test score")
        plt.title("Student Test Scores")
        plt.ylim(0, 100)
        plt.legend()
        plt.tight_layout()
        plt.savefig("student_scores.png", dpi=150)
        plt.show()

        print("Chart saved as student_scores.png")

    except requests.RequestException as error:
        print(f"API request failed: {error}")
    except (ValueError, KeyError) as error:
        print(f"Data processing failed: {error}")


if __name__ == "__main__":
    main()