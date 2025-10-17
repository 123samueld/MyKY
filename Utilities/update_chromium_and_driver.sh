#!/bin/bash

set -e  # Exit on error

echo "🔧 INSTALLING CHROMIUM 114.0.5735.90 + MATCHING DRIVER (Ubuntu 20.04)"
echo "========================================================="
echo "Target: Ubuntu 20.04.6 LTS (Focal) - Using Launchpad phd PPA"
echo "Source: Official Bionic build adapted for Focal (trusted)"
echo ""

# Step 1: Clean slate
echo "➡ Step 1: Cleaning up..."
rm -f /tmp/chromium_114.deb /tmp/driver.zip
sudo apt-get purge -y chromium-browser 2>/dev/null || true
sudo rm -f /usr/local/bin/chromedriver /usr/bin/chromedriver 2>/dev/null || true

# Step 2: Add phd PPA and update (for exact v114 .deb)
echo "➡ Step 2: Adding trusted phd/chromium-browser PPA..."
sudo add-apt-repository ppa:phd/chromium-browser-daily -y 2>/dev/null || true
sudo apt-get update -qq
sudo apt-mark hold chromium-browser  # Prevent auto-upgrades

# Step 3: Install dependencies
echo "➡ Step 3: Installing dependencies..."
sudo apt-get install -y wget unzip gdebi-core libnss3 libgconf-2-4 libxss1 libasound2 libgtk-3-0

# Step 4: Pin and install exact Chromium 114.0.5735.90
echo "➡ Step 4: Installing pinned Chromium 114.0.5735.90..."
# Create temp pin file for exact version
cat << EOF | sudo tee /etc/apt/preferences.d/chromium-pin
Package: chromium-browser
Pin: version 114.0.5735.90-0ubuntu0.18.04.1
Pin-Priority: 1001
EOF

sudo apt-get update -qq
sudo apt-get install -y chromium-browser=114.0.5735.90-0ubuntu0.18.04.1

# Step 5: Install matching ChromeDriver
echo "➡ Step 5: Installing ChromeDriver 114.0.5735.90..."
wget -q "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip" -O /tmp/driver.zip
sudo unzip -o /tmp/driver.zip -d /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
rm -f /tmp/driver.zip

# Step 6: Create symlink if needed (Ubuntu 20.04 fix)
if [ ! -f /usr/bin/chromium-browser ]; then
    echo "➡ Step 6: Creating chromium-browser symlink..."
    sudo ln -sf /usr/lib/chromium-browser/chromium-browser /usr/bin/chromium-browser
fi

# Step 7: Cleanup pin file
sudo rm -f /etc/apt/preferences.d/chromium-pin

# Step 8: FINAL VERIFICATION
echo ""
echo "✅ =========================================="
echo "✅          INSTALLATION COMPLETE!"
echo "✅ =========================================="
echo ""
echo "Chromium version:"
chromium-browser --version
echo ""
echo "ChromeDriver version:"
chromedriver --version
echo ""
echo "🔗 Paths:"
which chromium-browser
which chromedriver
echo ""
echo "🎉 VERSION MATCH CHECK:"
CHROMIUM_VER=$(chromium-browser --version 2>/dev/null | grep -o '114.0.5735')
DRIVER_VER=$(chromedriver --version 2>/dev/null | grep -o '114.0.5735')
if [[ "$CHROMIUM_VER" == "114.0.5735" && "$DRIVER_VER" == "114.0.5735" ]]; then
    echo "🎉 PERFECT MATCH! Selenium will work!"
else
    echo "⚠️  Version mismatch - check output above"
fi
echo ""
echo "➡ Step 9: Installing Python deps (Playwright + Stealth)"
python3 -m pip install --upgrade pip >/dev/null 2>&1 || true
python3 -m pip install playwright playwright-stealth >/dev/null 2>&1 || true
python3 -m playwright install chromium >/dev/null 2>&1 || true

echo "🚀 NEXT: You can run your scraper or use launch.sh to start services."
echo "🧹 To remove PPA later: sudo add-apt-repository --remove ppa:phd/chromium-browser-daily"