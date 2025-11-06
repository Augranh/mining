# Monero Mining Script - Automated Setup

Fully automated Monero (XMR) mining script with auto-download and auto-restart capabilities for server deployment.

## 🚀 Quick Start

1. **Edit wallet address in `main.py`** (line 16):

   ```python
   WALLET_ADDRESS = "YOUR_MONERO_WALLET_ADDRESS_HERE"
   ```

2. **Run the script**:
   ```bash
   python3 main.py
   ```

That's it! The script will automatically:

- Download XMRig miner if not present
- Extract and configure it
- Start mining
- Auto-restart on crashes

## 📋 Features

✅ **Fully Automated Setup**

- Auto-downloads XMRig from official GitHub releases
- Extracts and configures automatically
- No manual intervention needed

✅ **Server-Ready**

- Auto-restart on crashes
- Runs without user prompts
- Continuous mining operation

✅ **Cross-Platform**

- Windows (auto-detects)
- Linux (auto-detects)
- macOS (auto-detects)

✅ **Configurable**

- CPU usage control
- Thread count adjustment
- Custom mining pool support

## ⚙️ Configuration Options

Edit these variables in `main.py`:

```python
# Your Monero wallet address (REQUIRED)
WALLET_ADDRESS = "your_wallet_address_here"

# Mining pool (optional - default: gulf.moneroocean.stream)
POOL_URL = "pool.example.com:port"

# CPU usage (0-100, default: 100)
MAX_CPU_USAGE = 100

# Thread count (0 = auto, default: 0)
THREADS = 0
```

## 🖥️ Server Deployment

### Option 1: Run in Background (Linux/macOS)

```bash
nohup python3 main.py > mining.log 2>&1 &
```

### Option 2: Using Screen

```bash
screen -S mining
python3 main.py
# Press Ctrl+A then D to detach
# Reattach: screen -r mining
```

### Option 3: Using tmux

```bash
tmux new -s mining
python3 main.py
# Press Ctrl+B then D to detach
# Reattach: tmux attach -t mining
```

### Option 4: Systemd Service (Linux)

Create `/etc/systemd/system/monero-miner.service`:

```ini
[Unit]
Description=Monero Mining Service
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/mining/folder
ExecStart=/usr/bin/python3 /path/to/mining/folder/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then enable and start:

```bash
sudo systemctl enable monero-miner
sudo systemctl start monero-miner
sudo systemctl status monero-miner
```

## 📊 Monitoring

### Check Mining Status

```bash
# View real-time logs (if using nohup)
tail -f mining.log

# View XMRig logs
tail -f xmrig.log
```

### Check Hashrate

Mining stats are displayed in the console output. You can also check your pool's dashboard using your wallet address.

## 🛠️ Troubleshooting

### Script doesn't start mining

- Check internet connection (needed to download XMRig)
- Verify wallet address is correct
- Check if port 443 or 20128 is not blocked

### Low hashrate

- Increase `MAX_CPU_USAGE` to 100
- Set `THREADS` to match your CPU core count
- Ensure no other intensive processes are running

### Mining stops unexpectedly

The script has auto-restart enabled. Check logs for errors:

```bash
cat xmrig.log
```

## 📁 Generated Files

- `xmrig.exe` or `xmrig` - The mining executable (auto-downloaded)
- `config.json` - XMRig configuration (auto-generated)
- `xmrig.log` - Mining logs
- `mining.log` - Script output (if using nohup)

## 🔒 Security Notes

- Never share your wallet address private keys
- This script only needs your public wallet address
- Run on trusted servers only
- Monitor resource usage

## 📈 Popular Mining Pools

The script uses `gulf.moneroocean.stream:20128` by default. Other options:

- MoneroOcean: `gulf.moneroocean.stream:20128`
- SupportXMR: `pool.supportxmr.com:443`
- HashVault: `pool.hashvault.pro:443`
- MineXMR: `pool.minexmr.com:443`

## 💡 Tips for Maximum Performance

1. **Use dedicated CPU**: Mining works best on servers with good CPU
2. **Keep system cool**: Monitor temperature
3. **Stable internet**: Ensure reliable connection
4. **Update regularly**: Check for XMRig updates periodically
5. **Monitor pool**: Choose pool with low latency to your server

## 🆘 Support

For XMRig issues: https://github.com/xmrig/xmrig/issues
For Monero questions: https://www.reddit.com/r/Monero/

## ⚖️ Legal Notice

Cryptocurrency mining may be subject to regulations in your jurisdiction. Ensure you have permission to run mining software on your server. Check your hosting provider's terms of service.

## 📝 Version Info

- XMRig Version: 6.21.0
- Script Version: 2.0 (Auto-setup enabled)
- Last Updated: November 2025
