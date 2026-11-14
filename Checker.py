import os
import requests

API_URL = os.environ.get("GYMFINITY_API_URL")
NTFY_TOPIC = os.environ.get("NTFY_TOPIC")


def check_classes():
  if not API_URL:
    print("Error: GYMFINITY_API_URL secret is missing.")
    return

  try:
    response = requests.get(
        API_URL,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
        },
        timeout=15,
    )
    response.raise_for_status()
    data = response.json()

    spot_found = False
    alert_message = ""

    # Adjust keys based on the exact JSON structure from your Chrome DevTools inspection
    for session in data:
      day = session.get("dayOfWeek", "")
      time = session.get("startTime", "")
      spaces = session.get("availableSpaces", 0)

      # Customize your target day and time filter here
      if day == "Saturday" and "10:00" in time and spaces > 0:
        spot_found = True
        alert_message = (
            f"🚨 Spot Open! {session.get('name')} on {day} at {time} ({spaces}"
            " spaces left)"
        )
        break

    if spot_found and NTFY_TOPIC:
      requests.post(
          f"https://ntfy.sh/{NTFY_TOPIC}",
          data=alert_message.encode("utf-8"),
          headers={"Title": "Gymfinity Cambridge Alert"},
      )
      print("Alert sent via ntfy!")
    else:
      print("Checked: No matching spots open right now.")

  except Exception as e:
    print(f"Error checking API: {e}")


if __name__ == "__main__":
  check_classes()
