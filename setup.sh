#!/bin/bash
# Monero Mining - Quick Setup Script for Linux Servers

echo "=============================================="
echo "  Monero Mining - Quick Server Setup"
echo "=============================================="
echo ""

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Installing..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip
fi

echo "✅ Python3 is installed"
python3 --version

# Check if script directory exists
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "📂 Script directory: $SCRIPT_DIR"

# Check if wallet address is configured
WALLET_CHECK=$(grep "YOUR_MONERO_WALLET_ADDRESS_HERE" main.py)
if [ -n "$WALLET_CHECK" ]; then
    echo ""
    echo "⚠️  WARNING: Wallet address not configured!"
    echo "Please edit main.py and set your Monero wallet address"
    echo ""
    read -p "Enter your Monero wallet address (or press Enter to skip): " WALLET_ADDR
    
    if [ -n "$WALLET_ADDR" ]; then
        sed -i "s/YOUR_MONERO_WALLET_ADDRESS_HERE/$WALLET_ADDR/" main.py
        echo "✅ Wallet address configured"
    fi
fi

echo ""
echo "=============================================="
echo "  Setup Options"
echo "=============================================="
echo "1. Run now (foreground)"
echo "2. Run in background (nohup)"
echo "3. Install as systemd service"
echo "4. Exit"
echo ""
read -p "Choose option [1-4]: " OPTION

case $OPTION in
    1)
        echo ""
        echo "Starting miner in foreground..."
        echo "Press Ctrl+C to stop"
        echo ""
        python3 main.py
        ;;
    2)
        echo ""
        echo "Starting miner in background..."
        nohup python3 main.py > mining.log 2>&1 &
        PID=$!
        echo "✅ Miner started with PID: $PID"
        echo "📊 View logs: tail -f mining.log"
        echo "🛑 Stop miner: kill $PID"
        ;;
    3)
        echo ""
        echo "Installing systemd service..."
        
        # Update service file with correct paths
        CURRENT_USER=$(whoami)
        SERVICE_FILE="monero-miner.service"
        
        sed "s|YOUR_USERNAME|$CURRENT_USER|g" "$SERVICE_FILE" > /tmp/monero-miner.service
        sed -i "s|/path/to/mining/folder|$SCRIPT_DIR|g" /tmp/monero-miner.service
        
        sudo cp /tmp/monero-miner.service /etc/systemd/system/
        sudo systemctl daemon-reload
        sudo systemctl enable monero-miner
        sudo systemctl start monero-miner
        
        echo "✅ Service installed and started"
        echo ""
        echo "Useful commands:"
        echo "  Status:  sudo systemctl status monero-miner"
        echo "  Stop:    sudo systemctl stop monero-miner"
        echo "  Start:   sudo systemctl start monero-miner"
        echo "  Logs:    sudo journalctl -u monero-miner -f"
        ;;
    4)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid option"
        exit 1
        ;;
esac

echo ""
echo "=============================================="
echo "  Setup Complete!"
echo "=============================================="
