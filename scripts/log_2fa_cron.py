# scripts/log_2fa_cron.py
#!/usr/bin/env python3
# Cron script to log 2FA codes every minute

from app.totp_utils import generate_totp_code
import os
from datetime import datetime, timezone

SEED_PATH = "/data/seed.txt"
LOG_PATH = "/cron/last_code.txt"


def _read_hex_seed():
    if not os.path.exists(SEED_PATH):
        raise FileNotFoundError("Seed not decrypted yet")
    with open(SEED_PATH, "r") as f:
        return f.read().strip()


def main():
    try:
        hex_seed = _read_hex_seed()
        code = generate_totp_code(hex_seed)
        now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        with open(LOG_PATH, "a") as f:
            f.write(f"{now_utc} - 2FA Code: {code}\n")
    except Exception as e:
        print(f"Error in cron job: {e}", flush=True)


if __name__ == "__main__":
    main()
