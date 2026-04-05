import time
import datetime
import os

print("=== Alert System Started ===")
print("✅ Screen time alert: every 30 minutes")
print("✅ Gym Time alert: 4:00 PM (except Sunday)")
print("Press Ctrl+C to stop.\n")

total_seconds = 0
alerted_today = False
SCREEN_ALERT = 30 * 60

while True:
    now = datetime.datetime.now()
    weekday = now.weekday()
    hour = now.hour
    minute = now.minute

    total_seconds += 1

    hrs = total_seconds // 3600
    mins = (total_seconds % 3600) // 60
    secs = total_seconds % 60

    print(f"\rScreen time: {hrs:02d}:{mins:02d}:{secs:02d} | Clock: {now.strftime('%H:%M:%S')}", end="")

    if total_seconds % SCREEN_ALERT == 0:
        used_hrs = total_seconds // 3600
        used_mins = (total_seconds % 3600) // 60
        print(f"\n\n📱 SCREEN TIME ALERT!")
        print(f"You have been using your phone for {used_hrs}h {used_mins}m!")
        print("Take a break! Rest your eyes. 👀\n")
        os.system("termux-notification --title '📱 Screen Time Alert' --content 'You have been using your phone for 30 minutes! Take a break!'")
        os.system("termux-vibrate -d 500")

    if weekday != 6 and hour == 16 and minute == 0 and not alerted_today:
        alerted_today = True
        print(f"\n\n💪 GYM TIME! Get up and go to the gym!\n")
        os.system("termux-notification --title '💪 Gym Time!' --content 'Time to hit the gym! Lets go!'")
        os.system("termux-vibrate -d 1000")

    if hour == 0 and minute == 0 and total_seconds > 60:
        alerted_today = False

    time.sleep(1)
