#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                         CELESTIAL - RED TEAM EDITION                      ║
║                    WhatsApp Intelligence & Reporting Tool                  ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""
import os
import sys
import time
import json
import smtplib
import requests
import random
import re
import shutil
import hashlib
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from itertools import cycle
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

# ===== RED HACKER THEME =====
class Red:
    BLOOD = Fore.RED
    CRIMSON = Fore.LIGHTRED_EX
    DARK_RED = Fore.RED + Style.DIM
    MATRIX_GREEN = Fore.GREEN
    TERMINAL_AMBER = Fore.YELLOW
    CYBER_CYAN = Fore.CYAN
    PURE_WHITE = Fore.WHITE + Style.BRIGHT
    BG_BLACK = Back.BLACK
    BG_RED = Back.RED
    BOLD = Style.BRIGHT
    DIM = Style.DIM
    RESET = Style.RESET_ALL
    RED_ACCENT = Fore.LIGHTRED_EX + Style.BRIGHT
    RED_DIM = Fore.RED + Style.DIM
    RED = Fore.RED

# ===== CELESTIAL BANNER =====
CELESTIAL_BANNER = f"""
{Red.RED_ACCENT}╔═════════════════════════════════════════════════════════════════════╗
{Red.RED_ACCENT}║{Red.CRIMSON}  ██████╗███████╗██╗     ███████╗███████╗████████╗██╗ █████╗ ██╗     {Red.RED_ACCENT}║
{Red.RED_ACCENT}║{Red.CRIMSON} ██╔════╝██╔════╝██║     ██╔════╝██╔════╝╚══██╔══╝██║██╔══██╗██║     {Red.RED_ACCENT}║
{Red.RED_ACCENT}║{Red.CRIMSON} ██║     █████╗  ██║     █████╗  ███████╗   ██║   ██║███████║██║     {Red.RED_ACCENT}║
{Red.RED_ACCENT}║{Red.CRIMSON} ██║     ██╔══╝  ██║     ██╔══╝  ╚════██║   ██║   ██║██╔══██║██║     {Red.RED_ACCENT}║
{Red.RED_ACCENT}║{Red.CRIMSON} ╚██████╗███████╗███████╗███████╗██████╔╝   ██║   ██║██║  ██║███████╗{Red.RED_ACCENT}║
{Red.RED_ACCENT}║{Red.CRIMSON}  ╚═════╝╚══════╝╚══════╝╚══════╝╚═════╝    ╚═╝   ╚═╝╚═╝  ╚═╝╚══════╝{Red.RED_ACCENT}║
{Red.RED_ACCENT}╠═════════════════════════════════════════════════════════════════════╣  
{Red.RED_ACCENT}║{Red.BLOOD}                 WhatsApp Intelligence & Reporting Framework         {Red.RED_ACCENT}║              
{Red.RED_ACCENT}║{Red.DARK_RED}                         Red Team Edition • Version 2.0              {Red.RED_ACCENT}║                  
{Red.RED_ACCENT}║{Red.TERMINAL_AMBER}                         Author: SYMPTOM_BLACK                       {Red.RED_ACCENT}║   
{Red.RED_ACCENT}╚════════════════════════════════════════════════════════════════════{Red.RESET} {Red.RED_ACCENT}║
"""

# ===== YOUR WHATSAPP API CREDENTIALS (MASKED) =====
# These are masked for GitHub. Add your real keys in the Configuration menu.
ACCESS_TOKEN = "EAAJgi17vyDYBPT...[MASKED]...vB4ZCUI8EBNuNZCFZBfG5e11e"
PHONE_NUMBER_ID = "669101...[MASKED]...14"

# ===== SUPPORT TARGETS (LOADED FROM FILE) =====
# Masks used for fallback if file missing
BASE_SUPPORT_EMAILS = [
    "support@support.whatsapp.com",
    "appeals@support.whatsapp.com",
    "abuse@support.whatsapp.com"
]
support_emails = []

def load_support_targets():
    """Load targets from support_targets.txt"""
    global support_emails
    targets_file = "support_targets.txt"
    if os.path.exists(targets_file):
        try:
            with open(targets_file, 'r') as f:
                loaded = [line.strip() for line in f if line.strip()]
                if loaded:
                    support_emails = loaded * 11
                    return
        except:
            pass
    support_emails = BASE_SUPPORT_EMAILS * 11

# ===== YOUR EMERGENCY REPORT TEMPLATE =====
EMERGENCY_REPORT_TEMPLATE = """Dear WhatsApp Support Team,
I am writing in deep distress and fear regarding a user who has repeatedly sent extremely disturbing and illega content to my direct messages.
This individual continues to spam explicit material involving minors and has made horrifying statements about harming children. Beyond that, he has repeatedly threatened me personally, stating that he will hunt me and harm me.
I am genuinely scared for my safety. His messages are violent, disturbing, and show dangerous behavior. The content being sent is illegal and deeply traumatic.
The phone number involved is: {target}
This situation is not just harassment — it involves child exploitation material and direct threats to my life.
I respectfully urge WhatsApp to urgently investigate and permanently disable this account before someone is seriously harmed.
Please treat this as an emergency matter.
Sincerely,
A terrified user"""

# ===== GLOBAL VARIABLES =====
gmail_accounts = []
account_cycle = None
SESSION_ID = hashlib.md5(str(time.time()).encode()).hexdigest()[:6].upper()
OPERATION_COUNT = 0
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".celestial")
LOG_FILE = os.path.join(CONFIG_DIR, "operations.log")
TARGETS_FILE = os.path.join(CONFIG_DIR, "targets.dat")

# Create config directory
os.makedirs(CONFIG_DIR, exist_ok=True)

# ===== UTILITY FUNCTIONS =====
def clear():
    """Clear screen"""
    os.system("clear" if os.name == "posix" else "cls")

def typewriter(text, delay=0.03, color=Red.RED_ACCENT):
    """Typewriter effect"""
    for char in text:
        print(f"{color}{char}{Red.RESET}", end='', flush=True)
        time.sleep(delay)
    print()

def get_terminal_width():
    """Get terminal width"""
    return shutil.get_terminal_size().columns

def print_separator(char="═", color=Red.BLOOD):
    """Print separator line"""
    width = get_terminal_width()
    print(f"{color}{char * width}{Red.RESET}")

def print_header(text, color=Red.RED_ACCENT):
    """Print header with borders"""
    width = get_terminal_width()
    print(f"{Red.BLOOD}╔{'═' * (width-2)}╗")
    print(f"║{color}{text.center(width-2)}{Red.BLOOD}║")
    print(f"╚{'═' * (width-2)}╝{Red.RESET}")

def loading_animation(text, duration=1.0):
    """Loading animation"""
    frames = ["[=====     ]", "[======    ]", "[=======   ]", 
              "[========  ]", "[========= ]", "[==========]"]
    
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        print(f"\r{Red.RED_ACCENT}{frames[i % len(frames)]} {text}{Red.RESET}", end="", flush=True)
        i += 1
        time.sleep(0.1)
    print()

def progress_bar(current, total, bar_length=40):
    """Progress bar"""
    percent = float(current) * 100 / total
    arrow = '█' * int(percent/100 * bar_length)
    spaces = '░' * (bar_length - len(arrow))
    
    print(f"\r{Red.RED_ACCENT}[{arrow}{spaces}] {percent:.1f}% ({current}/{total}){Red.RESET}", end='')

def hacker_input(prompt):
    """Hacker-style input"""
    print(f"{Red.BLOOD}┌──[{Red.RED_ACCENT}celestial{Red.BLOOD}@redteam]-[~]")
    print(f"└─{Red.RED_ACCENT}$ {prompt}{Red.RESET} ", end='')
    return input()

def log_operation(operation, target, status):
    """Log operations to file"""
    global OPERATION_COUNT
    OPERATION_COUNT += 1
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "session": SESSION_ID,
        "operation": operation,
        "target": target,
        "status": status,
        "op_number": OPERATION_COUNT
    }
    
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(json.dumps(log_entry) + "\n")
    except:
        pass

# ===== WHATSAPP CHECK FUNCTION =====
def check_whatsapp_number(phone):
    """Check if number is on WhatsApp"""
    print(f"\n{Red.BLOOD}[*] Target:{Red.RED_ACCENT} {phone}")
    print(f"{Red.BLOOD}[*] Session:{Red.RED_ACCENT} {SESSION_ID}")
    print_separator("─")
    
    loading_animation("Bypassing WhatsApp security", 1.5)
    
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/contacts"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "blocking": "wait",
        "contacts": [phone],
        "force_check": True
    }
    try:
        print(f"{Red.RED_DIM}[>] Sending exploit payload...")
        response = requests.post(url, headers=headers, json=payload, timeout=15)
    except Exception as e:
        print(f"{Red.RED}[⚠️] Request failed: {e}\n")
        log_operation("SCAN", phone, f"FAILED-ERROR")
        return
    if response.status_code == 200:
        data = response.json()
        contacts = data.get("contacts", [])
        
        if contacts:
            for contact in contacts:
                status = contact.get("status", "unknown")
                wa_id = contact.get("wa_id", "N/A")
                
                print_separator("═")
                print(f"{Red.RED_ACCENT}  ███████╗ █████╗  ██████╗████████╗██╗██╗   ██╗███████╗")
                print(f"  ██╔════╝██╔══██╗██╔════╝╚══██╔══╝██║██║   ██║██╔════╝")
                print(f"  █████╗  ███████║██║        ██║   ██║██║   ██║█████╗  ")
                print(f"  ██╔══╝  ██╔══██║██║        ██║   ██║╚██╗ ██╔╝██╔══╝  ")
                print(f"  ██║     ██║  ██║╚██████╗   ██║   ██║ ╚████╔╝ ███████╗")
                print(f"  ╚═╝     ╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝  ╚═══╝  ╚══════╝{Red.RESET}")
                print_separator("═")
                print(f"{Red.BLOOD}    Target:     {Red.RED_ACCENT}{phone}")
                print(f"{Red.BLOOD}    WhatsApp ID:{Red.RED_ACCENT} {wa_id}")
                print(f"{Red.BLOOD}    Status:     {Red.RED_ACCENT}{status.upper()}")
                print(f"{Red.BLOOD}    Threat Level:{Red.RED_ACCENT} CRITICAL")
                print_separator("═")
                
                log_operation("SCAN", phone, "ACTIVE")
                with open(TARGETS_FILE, 'a') as f:
                    f.write(f"{datetime.now().isoformat()}|{phone}|{wa_id}|ACTIVE\n")
        else:
            print_separator("═")
            print(f"{Red.BLOOD}  ☠️  TARGET NOT FOUND  ☠️")
            print_separator("═")
            print(f"{Red.BLOOD}    Target:     {Red.RED_ACCENT}{phone}")
            print(f"{Red.BLOOD}    Status:     {Red.RED_ACCENT}INACTIVE")
            print_separator("═")
            log_operation("SCAN", phone, "INACTIVE")
    else:
        print(f"{Red.RED}[⚠️] Failed to check number. Status: {response.status_code}\n")
        log_operation("SCAN", phone, f"FAILED-{response.status_code}")

# ===== EMAIL SENDING FUNCTION =====
def send_email(subject, body, max_emails=None):
    """Send emails with optional limit"""
    success = 0
    fail = 0
    if not account_cycle:
        print(f"{Red.RED}[❌] No email accounts configured!")
        return (0, len(support_emails) if max_emails is None else max_emails)
    
    total = len(support_emails) if max_emails is None else min(max_emails, len(support_emails))
    print(f"{Red.RED_ACCENT}[>] Launching {total} warheads... (Rotation Active)\n")
    
    for i, email in enumerate(support_emails[:total], 1):
        # Rotate account for each email
        try:
            account = next(account_cycle)
            current_email = account["email"]
            current_password = account["password"]
            
            # Connect per email (stealth mode)
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(current_email, current_password)
            
            msg = MIMEMultipart()
            msg['From'] = current_email
            msg['To'] = email
            msg['Subject'] = f"[{SESSION_ID}] {subject}"
            msg.attach(MIMEText(body, 'plain'))
            
            server.send_message(msg)
            server.quit()
            
            success += 1
            print(f"\r{Red.RED_ACCENT}[{i}/{total}] {Red.MATRIX_GREEN}Sent from {current_email} -> {email}{Red.RESET}", end='')
            time.sleep(1.0) # Increased delay for safety
            
        except Exception as e:
            fail += 1
            print(f"\n{Red.RED}[❌] Failed to send from {current_email} to {email}: {e}")
            time.sleep(0.5)
            
    print("\n")
    return (success, fail)

# ===== VALIDATION FUNCTION =====
def validate_phone(phone):
    """Validate phone number format"""
    cleaned = re.sub(r'\D', '', phone)
    if 10 <= len(cleaned) <= 15:
        return cleaned
    return None

# ===== REPORTING FUNCTIONS =====
def single_number_check():
    """Check a single phone number"""
    clear()
    print_header(" SINGLE TARGET SCAN ")
    
    phone = hacker_input("Enter phone number (with country code)")
    validated = validate_phone(phone)
    
    if validated:
        check_whatsapp_number(validated)
    else:
        print(f"{Red.RED}[❌] Invalid phone number format!")
    
    hacker_input("\nPress Enter to continue")

def standard_report():
    """Standard fraud report"""
    clear()
    print_header(" STANDARD FRAUD REPORT ")
    
    target = hacker_input("Enter fraud/scam number (with country code)")
    confirm = input(f"{Red.RED_ACCENT}⚠️ Report {Red.BLOOD}{target}{Red.RED_ACCENT}? (y/n): {Red.RESET}").lower()
    
    if confirm == "y":
        print(f"{Red.TERMINAL_AMBER}🚨 Sending report...")
        
        subject = f"Report Fraud Number {target}"
        body = f"""Dear WhatsApp Support,
I want to report this number: {target}.
This number is involved in scam/fraudulent activities.
Please investigate and take action.
Regards,
WhatsApp User"""
        
        success, fail = send_email(subject, body)
        
        print_separator("═")
        if success > 0:
            print(f"{Red.RED_ACCENT}[✓] Report sent successfully for target: {target}")
            print(f"{Red.TERMINAL_AMBER}[!] Check after 2-3 minutes.")
        else:
            print(f"{Red.RED}[✗] Failed to send report.")
        print_separator("═")
        
        log_operation("STANDARD_REPORT", target, f"SUCCESS:{success}" if success > 0 else "FAILED")
    
    hacker_input("\nPress Enter to continue")

def hard_report():
    """HARD REPORT - Original hard report"""
    clear()
    print_header(" 🔴 HARD REPORT - EMERGENCY MODE 🔴 ")
    
    target = hacker_input("Enter fraud/scam number (with country code)")
    
    print(f"\n{Red.RED_ACCENT}╔══════════════════════════════════════════════════════════════╗")
    print(f"║{Red.CRIMSON}                   ⚠️  WARNING  ⚠️                              {Red.RED_ACCENT}║")
    print(f"║{Red.BLOOD}     This will send an EMERGENCY FRAUD REPORT                  {Red.RED_ACCENT}║")
    print(f"╚══════════════════════════════════════════════════════════════╝{Red.RESET}")
    
    confirm = input(f"{Red.RED_ACCENT}⚠️ Confirm HARD REPORT on {Red.BLOOD}{target}{Red.RED_ACCENT}? (y/n): {Red.RESET}").lower()
    
    if confirm == "y":
        print(f"{Red.RED}💀 Sending strong fraud report...")
        
        subject = f"URGENT: Strong Fraud Report {target}"
        body = f"""Dear WhatsApp Support Team,
This number {target} is being used for **serious abuse, fraud, impersonation, and criminal scam operations**.
This account is extremely dangerous and poses a **major threat to user safety and security**.
It is **repeatedly violating your Terms of Service and community standards**.
This is a **critical abuse report**. The account linked to {target} is involved in **extreme misconduct, harassment, impersonation, and fraud**.
The user is **deceiving people by falsely claiming to be the son of Mark Zuckerberg** in order to scam victims.
I **demand immediate and permanent suspension** of this account.
Sincerely,
A concerned user"""
        
        success, fail = send_email(subject, body)
        
        print_separator("═")
        if success > 0:
            print(f"{Red.RED_ACCENT}[✓] HARD REPORT sent successfully for target: {target}")
        else:
            print(f"{Red.RED}[✗] Failed to send HARD REPORT.")
        print_separator("═")
        
        log_operation("HARD_REPORT", target, f"SUCCESS:{success}" if success > 0 else "FAILED")
    
    hacker_input("\nPress Enter to continue")

def emergency_report():
    """YOUR EMERGENCY REPORT - Child exploitation & death threats"""
    clear()
    print_header(" 🔴🚨 EXTREME EMERGENCY REPORT 🚨🔴 ")
    
    target = hacker_input("Enter the predator's number (with country code)")
    
    print(f"\n{Red.RED_ACCENT}╔══════════════════════════════════════════════════════════════╗")
    print(f"║{Red.CRIMSON}              ⚠️  EXTREME CAUTION  ⚠️                          {Red.RED_ACCENT}║")
    print(f"║{Red.BLOOD}  This reports:                                                   {Red.RED_ACCENT}║")
    print(f"║{Red.BLOOD}  • Child exploitation material                                   {Red.RED_ACCENT}║")
    print(f"║{Red.BLOOD}  • Death threats against you                                     {Red.RED_ACCENT}║")
    print(f"║{Red.BLOOD}  • Direct threats to harm children                               {Red.RED_ACCENT}║")
    print(f"║{Red.BLOOD}  • User claims they will hunt you                                {Red.RED_ACCENT}║")
    print(f"╚══════════════════════════════════════════════════════════════╝{Red.RESET}")
    
    confirm = input(f"{Red.RED_ACCENT}⚠️ Confirm EXTREME EMERGENCY REPORT on {Red.BLOOD}{target}{Red.RED_ACCENT}? (y/n): {Red.RESET}").lower()
    
    if confirm == "y":
        print(f"{Red.RED}💀 Sending EXTREME EMERGENCY report...")
        
        subject = f"🚨 URGENT LIFE THREAT & CHILD EXPLOITATION: {target} 🚨"
        body = EMERGENCY_REPORT_TEMPLATE.format(target=target)
        
        success, fail = send_email(subject, body)
        
        print_separator("═")
        if success > 0:
            print(f"{Red.RED_ACCENT}[✓] EXTREME EMERGENCY REPORT sent for: {target}")
            print(f"{Red.TERMINAL_AMBER}[!] This is a LIFE THREATENING situation.")
            print(f"{Red.TERMINAL_AMBER}[!] If in immediate danger, contact local authorities.")
        else:
            print(f"{Red.RED}[✗] Failed to send emergency report. Try again or contact authorities directly.")
        print_separator("═")
        
        log_operation("EXTREME_EMERGENCY", target, f"SUCCESS:{success}" if success > 0 else "FAILED")
    
    hacker_input("\nPress Enter to continue")

def bulk_report():
    """Bulk report multiple numbers"""
    target = input("Enter your Subject: ")
    clear()
    print_header(" BULK REPORT - MULTIPLE NUMBERS ")
    
    filename = hacker_input("Enter filename with numbers (one per line)")
    try:
        with open(filename, 'r') as f:
            numbers = [line.strip() for line in f if line.strip()]
        
        print(f"{Red.BLOOD}[*] Loaded {len(numbers)} targets")
        print_separator("─")
        
        # Report type selection
        print(f"{Red.RED_ACCENT}Report Types:")
        print(f"  {Red.RED_ACCENT}[1] {Red.BLOOD}Standard Report")
        print(f"  {Red.RED_ACCENT}[2] {Red.CRIMSON}HARD Report")
        print(f"  {Red.RED_ACCENT}[3] {Red.RED}EXTREME EMERGENCY Report")
        
        report_type = input(f"{Red.RED_ACCENT}Select type [1-3]: {Red.RESET}").strip()
        
        confirm = input(f"{Red.RED_ACCENT}⚠️ Confirm bulk report on {len(numbers)} numbers? (y/n): {Red.RESET}").lower()
        
        if confirm == "y":
            success_count = 0
            fail_count = 0
            
            for i, target in enumerate(numbers, 1):
                print(f"\n{Red.RED_DIM}[{i}/{len(numbers)}] Reporting: {target}")
                
                if report_type == "3":
                    subject = f"🚨 URGENT LIFE THREAT & CHILD EXPLOITATION: {target} 🚨"
                    body = EMERGENCY_REPORT_TEMPLATE.format(target=target)
                elif report_type == "2":
                    subject = f"URGENT: Strong Fraud Report {target}"
                    body = f"""Dear WhatsApp Support Team,
This number {target} is being used for **serious abuse, fraud, impersonation, and criminal scam operations**.
This account is extremely dangerous and poses a **major threat to user safety and security**.
I **demand immediate and permanent suspension** of this account."""
                else:
                    subject = f"Report Fraud Number {target}"
                    body = f"""Dear WhatsApp Support,I want to report this number: {target}.This number is involved in scam/fraudulent activities.Please investigate and take action.
                    """   
                success, fail = send_email(subject, body, max_emails=1)
                
                if success > 0:
                    success_count += 1
                    print(f"{Red.RED_ACCENT}  ✓ Reported")
                else:
                    fail_count += 1
                    print(f"{Red.RED}  ✗ Failed")
                
                time.sleep(0.5)
            
            print_separator("═")
            print(f"{Red.RED_ACCENT}[✓] BULK REPORT COMPLETE")
            print(f"    Successful: {success_count}")
            print(f"    Failed: {fail_count}")
            print_separator("═")
            
            log_operation("BULK_REPORT", f"{len(numbers)} numbers", f"SUCCESS:{success_count}")
    
    except FileNotFoundError:
        print(f"{Red.RED}[✗] File '{filename}' not found!")
    except Exception as e:
        print(f"{Red.RED}[✗] Error: {e}")
    
    hacker_input("\nPress Enter to continue")

# ===== EMAIL ATTACK MENU =====
def email_attack_menu():
    """Email bombing menu"""
    clear()
    print_header(" EMAIL BOMBING SEQUENCE ")
    
    print(f"\n{Red.BLOOD}[*] Launch platforms: {Red.RED_ACCENT}{len(gmail_accounts)}")
    print(f"{Red.BLOOD}[*] Target emails: {Red.RED_ACCENT}{len(support_emails)}")
    print_separator("─")
    
    if not gmail_accounts:
        print(f"{Red.RED}[❌] No email platforms configured!")
        hacker_input("Press Enter to continue")
        return
    
    subject = hacker_input("Subject")
    if not subject:
        subject = "Message"
    
    print(f"{Red.BLOOD}[*] Enter message body (type 'END' on new line):")
    body_lines = []
    while True:
        line = input()
        if line.strip() == 'END':
            break
        body_lines.append(line)
    
    body = '\n'.join(body_lines) if body_lines else "Test message"
    
    max_input = hacker_input(f"Max emails (default: {len(support_emails)})")
    try:
        max_emails = int(max_input) if max_input else len(support_emails)
    except:
        max_emails = len(support_emails)
    
    success, fail = send_email(subject, body, max_emails)
    
    print_separator("═")
    print(f"{Red.BLOOD}[*] Attack Summary:")
    print(f"    Successful: {success}")
    print(f"    Failed: {fail}")
    print_separator("═")
    
    hacker_input("Press Enter to continue")

# ===== BULK SCAN FUNCTION =====
def scan_single_bulk(phone):
    """Single scan for bulk operation"""
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/contacts"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "blocking": "wait",
        "contacts": [phone],
        "force_check": True
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return bool(data.get("contacts", []))
        return None
    except:
        return None

def bulk_scan():
    """Scan multiple numbers from file"""
    clear()
    print_header(" BULK TARGET SCAN ")
    
    filename = hacker_input("Target file path")
    
    try:
        with open(filename, 'r') as f:
            numbers = [line.strip() for line in f if line.strip()]
        
        print(f"{Red.BLOOD}[*] Loaded {len(numbers)} targets")
        
        valid = []
        invalid = []
        for num in numbers:
            validated = validate_phone(num)
            if validated:
                valid.append(validated)
            else:
                invalid.append(num)
        
        if invalid:
            print(f"{Red.RED_DIM}[!] Skipped {len(invalid)} invalid targets")
        
        if not valid:
            print(f"{Red.RED}[❌] No valid targets")
            hacker_input("Press Enter to continue")
            return
        
        confirm = hacker_input(f"Scan {len(valid)} targets? (y/n)")
        
        if confirm.lower() in ['y', 'yes']:
            results = {'active': [], 'inactive': [], 'failed': []}
            
            for i, number in enumerate(valid, 1):
                print(f"\n{Red.BLOOD}[{i}/{len(valid)}] Scanning: {number}")
                result = scan_single_bulk(number)
                
                if result == True:
                    results['active'].append(number)
                    print(f"{Red.RED_ACCENT}  [✓] ACTIVE")
                elif result == False:
                    results['inactive'].append(number)
                    print(f"{Red.RED_DIM}  [-] INACTIVE")
                else:
                    results['failed'].append(number)
                    print(f"{Red.RED}  [✗] FAILED")
                
                time.sleep(0.5)
            
            print_separator("═")
            print(f"{Red.RED_ACCENT}[*] BULK SCAN COMPLETE")
            print_separator("─")
            print(f"  Active:   {len(results['active'])}")
            print(f"  Inactive: {len(results['inactive'])}")
            print(f"  Failed:   {len(results['failed'])}")
            print_separator("═")
            
            log_operation("BULK_SCAN", f"{len(valid)} targets", f"A:{len(results['active'])}")
    
    except FileNotFoundError:
        print(f"{Red.RED}[✗] File not found")
    except Exception as e:
        print(f"{Red.RED}[✗] Error: {e}")
    
    hacker_input("Press Enter to continue")

# ===== CONFIGURATION FUNCTIONS =====
def load_accounts():
    """Load saved Gmail accounts"""
    global gmail_accounts, account_cycle
    
    accounts_file = os.path.join(CONFIG_DIR, "accounts.json")
    if os.path.exists(accounts_file):
        try:
            with open(accounts_file, 'r') as f:
                config = json.load(f)
                gmail_accounts = config.get("gmail_accounts", [])
        except:
            pass
            
   #Gmails
    if not gmail_accounts:
        gmail_accounts = [
            {"email": "ken...[MASKED]@gmail.com", "password": "****************"},
            {"email": "coi...[MASKED]@gmail.com", "password": "****************"},
            {"email": "mer...[MASKED]@gmail.com", "password": "****************"},
            {"email": "sop...[MASKED]@gmail.com", "password": "****************"}
        ]
    
    account_cycle = cycle(gmail_accounts)

def update_source_masks():
    """Automatically update the source code fallback list with masked versions"""
    global gmail_accounts
    try:
        script_path = __file__
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create the new masked list string
        masked_list = "        gmail_accounts = [\n"
        for i, acc in enumerate(gmail_accounts):
            email = acc['email']
            # Masking logic
            if "@" in email:
                prefix, domain = email.split("@")
                masked_email = f"{prefix[:3]}...[MASKED]...@{domain}"
            else:
                masked_email = f"{email[:3]}...[MASKED]..."
                
            comma = "," if i < len(gmail_accounts) - 1 else ""
            masked_list += f'            {{"email": "{masked_email}", "password": "****************"}}{comma}\n'
        masked_list += "        ]"
        
        # Regex to find and replace the fallback list
        pattern = r"    if not gmail_accounts:\s+gmail_accounts = \[\s+.*?        \]"
        new_content = re.sub(pattern, f"    if not gmail_accounts:\n{masked_list}", content, flags=re.DOTALL)
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    except:
        pass

def save_accounts():
    """Save Gmail accounts"""
    accounts_file = os.path.join(CONFIG_DIR, "accounts.json")
    config = {"gmail_accounts": gmail_accounts}
    with open(accounts_file, 'w') as f:
        json.dump(config, f)
    # Automatically update the source code with masked versions for the "public" aesthetic
    update_source_masks()

def add_email_account():
    """Add Gmail account"""
    clear()
    print_header(" ADD EMAIL PLATFORM ")
    
    print(f"{Red.RED_DIM}[!] Use App Password (https://myaccount.google.com/apppasswords)")
    print_separator("─")
    
    email = hacker_input("Gmail address")
    password = hacker_input("App password")
    
    if email and password:
        gmail_accounts.append({"email": email, "password": password})
        global account_cycle
        account_cycle = cycle(gmail_accounts)
        save_accounts()
        print(f"{Red.RED_ACCENT}[✓] Platform added")
    else:
        print(f"{Red.RED}[❌] Both fields required")
    
    time.sleep(1)

def remove_email_account():
    """Remove Gmail account"""
    global gmail_accounts, account_cycle
    
    clear()
    print_header(" REMOVE EMAIL PLATFORM ")
    
    if not gmail_accounts:
        print(f"{Red.RED_DIM}[!] No platforms configured")
        time.sleep(1)
        return
    
    for i, acc in enumerate(gmail_accounts, 1):
        print(f"{Red.RED_ACCENT}[{i}] {acc['email']}")
    
    try:
        choice = int(hacker_input("Select platform to remove"))
        if 1 <= choice <= len(gmail_accounts):
            removed = gmail_accounts.pop(choice-1)
            if gmail_accounts:
                account_cycle = cycle(gmail_accounts)
            else:
                account_cycle = None
            save_accounts()
            print(f"{Red.RED_ACCENT}[✓] Removed {removed['email']}")
        else:
            print(f"{Red.RED}[❌] Invalid selection")
    except ValueError:
        print(f"{Red.RED}[❌] Invalid input")
    
    time.sleep(1)

def list_email_accounts():
    """List all email accounts"""
    clear()
    print_header(" EMAIL PLATFORMS ")
    
    if not gmail_accounts:
        print(f"{Red.RED_DIM}[!] No platforms configured")
    else:
        for i, acc in enumerate(gmail_accounts, 1):
            print(f"{Red.RED_ACCENT}[{i}] {acc['email']}")

    hacker_input("\nPress Enter to continue")

def load_wa_config():
    """Load WhatsApp API credentials"""
    global ACCESS_TOKEN, PHONE_NUMBER_ID
    config_file = os.path.join(CONFIG_DIR, "wa_config.json")
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                token = config.get("access_token")
                pid = config.get("phone_id")
                if token and "[MASKED]" not in token:
                    ACCESS_TOKEN = token
                if pid and "[MASKED]" not in pid:
                    PHONE_NUMBER_ID = pid
        except:
            pass

def save_wa_config():
    """Save WhatsApp API credentials"""
    config_file = os.path.join(CONFIG_DIR, "wa_config.json")
    config = {
        "access_token": ACCESS_TOKEN,
        "phone_id": PHONE_NUMBER_ID
    }
    with open(config_file, 'w') as f:
        json.dump(config, f)

def edit_wa_credentials():
    """UI for editing WhatsApp credentials"""
    global ACCESS_TOKEN, PHONE_NUMBER_ID
    clear()
    print_header(" WHATSAPP API CONFIG ")
    
    def mask(s): return f"{s[:10]}...[REDACTED]...{s[-10:]}" if len(s) > 20 else s
    
    print(f"{Red.BLOOD}[*] Current Token: {Red.RED_ACCENT}{mask(ACCESS_TOKEN)}")
    print(f"{Red.BLOOD}[*] Current Phone ID: {Red.RED_ACCENT}{PHONE_NUMBER_ID}")
    print_separator("─")
    
    new_token = hacker_input("Enter New Access Token (Enter to skip)")
    new_id = hacker_input("Enter New Phone Number ID (Enter to skip)")
    
    if new_token: ACCESS_TOKEN = new_token
    if new_id: PHONE_NUMBER_ID = new_id
    
    if new_token or new_id:
        save_wa_config()
        print(f"{Red.RED_ACCENT}[✓] Credentials updated and saved locally")
    
    time.sleep(1.5)

def config_menu():
    """Configuration menu"""
    while True:
        clear()
        print_header(" CONFIGURATION ")
        print(f"{Red.RED_ACCENT} [1] {Red.BLOOD}Add Email Platform (Sender)")
        print(f"{Red.RED_ACCENT} [2] {Red.BLOOD}Remove Email Platform")
        print(f"{Red.RED_ACCENT} [3] {Red.BLOOD}List Email Platforms")
        print(f"{Red.RED_ACCENT} [4] {Red.CRIMSON}Edit WhatsApp API Credentials")
        print(f"{Red.RED_ACCENT} [5] {Red.BLOOD}Back")
        
        choice = hacker_input("Select option")
        
        if choice == '1': add_email_account()
        elif choice == '2': remove_email_account()
        elif choice == '3': list_email_accounts()
        elif choice == '4': edit_wa_credentials()
        elif choice == '5': break

def main_menu():
    """Main application menu"""
    while True:
        clear()
        print(CELESTIAL_BANNER)
        print(f"{Red.RED_ACCENT} [1] {Red.BLOOD}Single Target Scan")
        print(f"{Red.RED_ACCENT} [2] {Red.BLOOD}Bulk Target Scan")
        print(f"{Red.RED_ACCENT} [3] {Red.BLOOD}Standard Fraud Report")
        print(f"{Red.RED_ACCENT} [4] {Red.CRIMSON}Hard Report (Emergency)")
        print(f"{Red.RED_ACCENT} [5] {Red.RED}Extreme Emergency Report")
        print(f"{Red.RED_ACCENT} [6] {Red.BLOOD}Bulk Report")
        print(f"{Red.RED_ACCENT} [7] {Red.BLOOD}Email Attack System")
        print(f"{Red.RED_ACCENT} [8] {Red.BLOOD}Configuration")
        print(f"{Red.RED_ACCENT} [9] {Red.BLOOD}Exit")
        
        choice = hacker_input("Select option")
        
        if choice == '1': single_number_check()
        elif choice == '2': bulk_scan()
        elif choice == '3': standard_report()
        elif choice == '4': hard_report()
        elif choice == '5': emergency_report()
        elif choice == '6': bulk_report()
        elif choice == '7': email_attack_menu()
        elif choice == '8': config_menu()
        elif choice == '9': sys.exit()

if __name__ == "__main__":
    try:
        load_support_targets()
        load_wa_config()
        load_accounts()
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{Red.RED}Exiting...{Red.RESET}")
