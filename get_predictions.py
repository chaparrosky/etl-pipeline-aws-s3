"""
Quick script to get predictions for UFC 323 main card fights
"""
import requests
import json

API_BASE = "http://localhost:8000/api/v1"

fights = [
    {"red": "Merab Dvalishvili", "blue": "Petr Yan", "title": "UFC Bantamweight Championship"},
    {"red": "Alexandre Pantoja", "blue": "Joshua Van", "title": "UFC Flyweight Championship"},
    {"red": "Henry Cejudo", "blue": "Payton Talbott", "title": "Bantamweight"},
    {"red": "Brandon Moreno", "blue": "Tatsuro Taira", "title": "Flyweight"},
]

print("=" * 80)
print("UFC 323: DVALISHVILI VS. YAN 2 - DECEMBER 6, 2025")
print("T-Mobile Arena, Las Vegas, Nevada")
print("=" * 80)
print()

for fight in fights:
    print(f"\n{'=' * 80}")
    print(f"{fight['title'].upper()}")
    print(f"{fight['red']} (Red) vs {fight['blue']} (Blue)")
    print(f"{'=' * 80}\n")

    try:
        response = requests.post(
            f"{API_BASE}/predictions/predict",
            json={"red_fighter_name": fight['red'], "blue_fighter_name": fight['blue']},
            timeout=10
        )

        if response.status_code == 200:
            prediction = response.json()

            print(f"PREDICTED WINNER: {prediction['predicted_winner']} Corner")
            winner_name = prediction['red_fighter_name'] if prediction['predicted_winner'] == 'Red' else prediction['blue_fighter_name']
            print(f"                  ({winner_name})")
            print()
            print(f"Win Probability:")
            print(f"  {prediction['red_fighter_name']}: {prediction['red_win_probability'] * 100:.1f}%")
            print(f"  {prediction['blue_fighter_name']}: {prediction['blue_win_probability'] * 100:.1f}%")
            print()
            print(f"Confidence Score: {prediction['confidence_score']:.1f}%")
            print(f"Predicted Method: {prediction['predicted_method']}")
            print()
            print("Key Factors:")
            for factor in prediction['key_factors']:
                print(f"  - {factor}")
            print()
            print(f"Betting Recommendation: {prediction['betting_recommendation']}")

        elif response.status_code == 404:
            print(f"ERROR: One or both fighters not found in database")
            print(f"Details: {response.json()}")
        else:
            print(f"ERROR: Status code {response.status_code}")
            print(f"Response: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"ERROR: Could not connect to API - {e}")
    except Exception as e:
        print(f"ERROR: {e}")

print("\n" + "=" * 80)
print("END OF PREDICTIONS")
print("=" * 80)
