#!/usr/bin/env python3
"""
Monero (XMR) Mining Script
This script manages Monero mining using XMRig miner.
"""

import subprocess
import platform
import os
import sys
import json
import time
import urllib.request
import zipfile
import tarfile
import shutil

# ================== CONFIGURATION ==================
# Replace with your Monero wallet address
WALLET_ADDRESS = "8BuBgaci1tR8p3zkbaqb43ZohqWMorNZzGekzpRiKQdy4Ns1nqadLrjSQpA9UQkqVNG5b51navMMvLW2ftyhWR9f5FTTeE1"

# Mining pool configuration (you can change to your preferred pool)
POOL_URL = "gulf.moneroocean.stream:20128"  # Popular pool with SSL
POOL_USER = WALLET_ADDRESS  # Usually the wallet address
POOL_PASS = "x"  # Usually just 'x' or your worker name

# Mining configuration
THREADS = 0  # 0 = auto-detect optimal thread count
MAX_CPU_USAGE = 100  # Maximum CPU usage percentage (0-100)

# XMRig download URLs (update these to latest version if needed)
XMRIG_VERSION = "6.21.0"
XMRIG_URLS = {
    "Windows": f"https://github.com/xmrig/xmrig/releases/download/v{XMRIG_VERSION}/xmrig-{XMRIG_VERSION}-msvc-win64.zip",
    "Linux": f"https://github.com/xmrig/xmrig/releases/download/v{XMRIG_VERSION}/xmrig-{XMRIG_VERSION}-linux-static-x64.tar.gz",
    "Darwin": f"https://github.com/xmrig/xmrig/releases/download/v{XMRIG_VERSION}/xmrig-{XMRIG_VERSION}-macos-x64.tar.gz"
}
# ===================================================


def check_wallet_address():
    """Validate that wallet address has been configured."""
    if WALLET_ADDRESS == "YOUR_MONERO_WALLET_ADDRESS_HERE":
        print("❌ ERROR: Please set your Monero wallet address in the script!")
        print("Edit the WALLET_ADDRESS variable in main.py")
        sys.exit(1)
    
    # Basic validation - Monero addresses are 95 or 106 characters
    if len(WALLET_ADDRESS) not in [95, 106]:
        print("⚠️  WARNING: Wallet address length seems incorrect.")
        print(f"Current length: {len(WALLET_ADDRESS)}")
        print("Monero addresses are typically 95 or 106 characters long.")
        print("Continuing anyway for automated deployment...")
        time.sleep(2)


def get_system_info():
    """Get system information."""
    system = platform.system()
    machine = platform.machine()
    cpu_count = os.cpu_count()
    
    print(f"🖥️  System: {system} ({machine})")
    print(f"🔧 CPU Cores: {cpu_count}")
    return system, machine, cpu_count


def create_xmrig_config():
    """Create XMRig configuration file."""
    config = {
        "autosave": True,
        "cpu": {
            "enabled": True,
            "huge-pages": True,
            "hw-aes": None,
            "priority": None,
            "max-threads-hint": MAX_CPU_USAGE,
            "asm": True,
            "rx": [0, 1],
            "cn": [0, 1]
        },
        "opencl": False,
        "cuda": False,
        "pools": [
            {
                "url": POOL_URL,
                "user": POOL_USER,
                "pass": POOL_PASS,
                "keepalive": True,
                "tls": True,
                "tls-fingerprint": None
            }
        ],
        "log-file": "xmrig.log",
        "print-time": 60,
        "retries": 5,
        "retry-pause": 5
    }
    
    if THREADS > 0:
        config["cpu"]["threads"] = THREADS
    
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
    
    print(f"✅ Configuration file created: {config_path}")
    return config_path


def check_xmrig_installed():
    """Check if XMRig is installed in the current directory."""
    system = platform.system()
    
    if system == "Windows":
        xmrig_path = os.path.join(os.path.dirname(__file__), "xmrig.exe")
    else:
        xmrig_path = os.path.join(os.path.dirname(__file__), "xmrig")
    
    return os.path.exists(xmrig_path), xmrig_path


def download_xmrig():
    """Automatically download and set up XMRig."""
    import urllib.request
    import zipfile
    import tarfile
    import shutil
    
    system = platform.system()
    script_dir = os.path.dirname(os.path.abspath(__file__)) or os.getcwd()
    
    print("\n" + "="*60)
    print("⚠️  XMRig not found - Starting automatic download...")
    print("="*60)
    
    url = XMRIG_URLS.get(system)
    if not url:
        print(f"❌ No download URL available for {system}")
        return False
    
    try:
        # Download XMRig
        print(f"📥 Downloading XMRig {XMRIG_VERSION} from GitHub...")
        print(f"   URL: {url}")
        filename = os.path.join(script_dir, url.split('/')[-1])
        
        # Show download progress
        def reporthook(blocknum, blocksize, totalsize):
            readsofar = blocknum * blocksize
            if totalsize > 0:
                percent = readsofar * 100 / totalsize
                s = f"\r   Progress: {percent:5.1f}% ({readsofar}/{totalsize} bytes)"
                sys.stderr.write(s)
                if readsofar >= totalsize:
                    sys.stderr.write("\n")
            else:
                sys.stderr.write(f"\r   Downloaded: {readsofar} bytes")
        
        urllib.request.urlretrieve(url, filename, reporthook)
        print("✅ Download complete!")
        
        # Extract archive
        print("📦 Extracting archive...")
        extract_dir = os.path.join(script_dir, "xmrig_temp")
        
        if filename.endswith('.zip'):
            with zipfile.ZipFile(filename, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
        elif filename.endswith('.tar.gz'):
            with tarfile.open(filename, 'r:gz') as tar_ref:
                tar_ref.extractall(extract_dir)
        else:
            print(f"❌ Unknown archive format: {filename}")
            return False
        
        print("✅ Extraction complete!")
        
        # Find and move xmrig executable
        print("🔍 Locating XMRig executable...")
        xmrig_exe = "xmrig.exe" if system == "Windows" else "xmrig"
        xmrig_found = False
        
        for root, dirs, files in os.walk(extract_dir):
            if xmrig_exe in files:
                source = os.path.join(root, xmrig_exe)
                destination = os.path.join(script_dir, xmrig_exe)
                
                print(f"📋 Moving {xmrig_exe} to script directory...")
                shutil.move(source, destination)
                
                # Make executable on Unix systems
                if system != "Windows":
                    os.chmod(destination, 0o755)
                    print("✅ Made executable")
                
                xmrig_found = True
                break
        
        # Clean up
        print("🧹 Cleaning up temporary files...")
        if os.path.exists(filename):
            os.remove(filename)
        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)
        
        if xmrig_found:
            print("✅ XMRig setup complete!")
            print(f"   Location: {os.path.join(script_dir, xmrig_exe)}")
            return True
        else:
            print(f"❌ Could not find {xmrig_exe} in extracted files")
            return False
            
    except Exception as e:
        print(f"❌ Error during download/setup: {e}")
        import traceback
        traceback.print_exc()
        return False


def start_mining(xmrig_path, config_path):
    """Start the mining process."""
    print("\n" + "="*60)
    print("⛏️  Starting Monero Mining...")
    print("="*60)
    print(f"Wallet: {WALLET_ADDRESS[:10]}...{WALLET_ADDRESS[-10:]}")
    print(f"Pool: {POOL_URL}")
    print(f"Config: {config_path}")
    print("="*60)
    print("\n🚀 Mining started! Press Ctrl+C to stop.\n")
    
    try:
        # Start XMRig with config file
        cmd = [xmrig_path, "--config", config_path]
        
        # Run the miner
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Display output in real-time
        for line in process.stdout:
            print(line, end='')
        
        process.wait()
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopping mining...")
        process.terminate()
        process.wait()
        print("✅ Mining stopped.")
    except Exception as e:
        print(f"\n❌ Error during mining: {e}")


def main():
    """Main function."""
    print("="*60)
    print("    🔷 Monero (XMR) Mining Script 🔷")
    print("="*60)
    
    # Check wallet address is configured
    check_wallet_address()
    
    # Get system info
    get_system_info()
    
    # Check if XMRig is installed
    xmrig_installed, xmrig_path = check_xmrig_installed()
    
    if not xmrig_installed:
        print("\n🔄 XMRig not found - initiating automatic setup...")
        success = download_xmrig()
        
        if success:
            xmrig_installed, xmrig_path = check_xmrig_installed()
        
        if not xmrig_installed:
            print("\n❌ XMRig setup failed!")
            print("Please check your internet connection and try again.")
            print("Or download XMRig manually from: https://github.com/xmrig/xmrig/releases")
            sys.exit(1)
    
    print(f"\n✅ XMRig found: {xmrig_path}")
    
    # Make executable on Unix systems
    if platform.system() != "Windows":
        try:
            os.chmod(xmrig_path, 0o755)
        except Exception as e:
            print(f"⚠️  Warning: Could not set executable permissions: {e}")
    
    # Create configuration file
    config_path = create_xmrig_config()
    
    # Start mining with auto-restart
    retry_count = 0
    max_retries = 999  # Essentially infinite for server deployment
    
    while retry_count < max_retries:
        try:
            if retry_count > 0:
                print(f"\n🔄 Restarting miner (attempt {retry_count + 1})...")
                time.sleep(5)  # Wait 5 seconds before restart
            
            start_mining(xmrig_path, config_path)
            
            # If we get here, mining ended normally (Ctrl+C)
            break
            
        except KeyboardInterrupt:
            print("\n\n⏹️  Stopping mining...")
            print("✅ Mining stopped by user.")
            break
            
        except Exception as e:
            print(f"\n❌ Mining error: {e}")
            retry_count += 1
            
            if retry_count < max_retries:
                print(f"⏳ Waiting 10 seconds before retry...")
                time.sleep(10)
            else:
                print("❌ Max retries reached. Exiting.")
                sys.exit(1)


if __name__ == "__main__":
    main()
