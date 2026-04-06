import time
import datetime
import os

# ─────────────────────────────────────────────
#  CONFIG — edit these to customize your alerts
# ─────────────────────────────────────────────
SCREEN_ALERT_MINUTES = 30       # How often to remind you (in minutes)
GYM_HOUR             = 16       # 24-hour format (16 = 4:00 PM)
GYM_MINUTE           = 0
GYM_SKIP_DAYS        = {6}      # 6 = Sunday (0=Mon ... 6=Sun)
VIBRATE_SHORT_MS     = 500      # Vibration for screen alert
VIBRATE_LONG_MS      = 1000     # Vibration for gym alert
# ─────────────────────────────────────────────

def notify(title, content):
    os.system(f'termux-notification --title "{title}" --content "{content}"')

def vibrate(duration_ms):
    os.system(f"termux-vibrate -d {duration_ms}")

def send_screen_alert(total_seconds):
    used_hrs  = total_seconds // 3600
    used_mins = (total_seconds % 3600) // 60
    msg = f"You've been on your phone for {used_hrs}h {used_mins}m! Take a break 👀"
    print(f"\n\n📱 SCREEN TIME ALERT! {msg}\n")
    notify("📱 Screen Time Alert", msg)
    vibrate(VIBRATE_SHORT_MS)

def send_gym_alert():
    print("\n\n💪 GYM TIME! Get up and go to the gym!\n")
    notify("💪 Gym Time!", "Time to hit the gym! Let's go!")
    vibrate(VIBRATE_LONG_MS)

def main():
    print("=== Alert System Started ===")
    print(f"✅ Screen time alert : every {SCREEN_ALERT_MINUTES} minutes")
    print(f"✅ Gym Time alert    : {GYM_HOUR:02d}:{GYM_MINUTE:02d} (skips Sunday)")
    print("Press Ctrl+C to stop.\n")

    screen_alert_interval = SCREEN_ALERT_MINUTES * 60

    # Track wall-clock time to avoid drift
    start_time      = time.monotonic()
    last_alert_secs = 0          # last screen alert at this many elapsed seconds
    alerted_today   = False
    last_day        = datetime.date.today()

    try:
        while True:
            now          = datetime.datetime.now()
            today        = now.date()
            elapsed      = int(time.monotonic() - start_time)  # drift-free seconds

            # ── Midnight reset ──────────────────────────────────────────
            if today != last_day:
                alerted_today = False
                last_day      = today

            # ── Display ─────────────────────────────────────────────────
            hrs  = elapsed // 3600
            mins = (elapsed % 3600) // 60
            secs = elapsed % 60
            print(
                f"\rScreen time: {hrs:02d}:{mins:02d}:{secs:02d} | "
                f"Clock: {now.strftime('%H:%M:%S')}",
                end=""
            )

            # ── Screen time alert (wall-clock based, no drift) ──────────
            alerts_due = elapsed // screen_alert_interval
            if alerts_due > last_alert_secs // screen_alert_interval:
                last_alert_secs = elapsed
                send_screen_alert(elapsed)

            # ── Gym alert ───────────────────────────────────────────────
            if (
                now.weekday() not in GYM_SKIP_DAYS
                and now.hour   == GYM_HOUR
                and now.minute == GYM_MINUTE
                and not alerted_today
            ):
                alerted_today = True
                send_gym_alert()

            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\nAlert system stopped. Goodbye! 👋")

if __name__ == "__main__":
    main()
