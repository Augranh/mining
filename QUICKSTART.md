# 🚀 QUICK START GUIDE

## For Linux/macOS Servers:

1. **Upload files to server**

   ```bash
   scp -r * user@your-server:/path/to/mining/
   ```

2. **SSH into server**

   ```bash
   ssh user@your-server
   cd /path/to/mining/
   ```

3. **Edit wallet address**

   ```bash
   nano main.py
   # Change line 16: WALLET_ADDRESS = "your_wallet_here"
   ```

4. **Run automated setup**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

## For Windows Servers:

1. **Copy files to server**
2. **Edit wallet address**

   - Open `main.py`
   - Change line 16: `WALLET_ADDRESS = "your_wallet_here"`

3. **Run setup**
   - Double-click `setup.bat`
   - Or run: `python main.py`

## Manual Start (Any System):

```bash
python3 main.py
```

The script will automatically:
✅ Download XMRig if needed
✅ Configure everything
✅ Start mining
✅ Auto-restart on crashes

## Background Execution:

**Linux/macOS:**

```bash
nohup python3 main.py > mining.log 2>&1 &
```

**Windows:**

```cmd
start /min python main.py
```

## Check Mining Status:

View your mining stats at your pool's website using your wallet address.

Default pool: https://moneroocean.stream/

---

**Need help?** See README.md for detailed instructions.
