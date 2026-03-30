#!/bin/bash
# HealthAI — Buildozer setup & build script for Ubuntu/WSL
# Run this after WSL Ubuntu is installed:
#   bash /mnt/d/انتيجرافيتي/m--01/build.sh

set -e
echo ""
echo "======================================"
echo "  HealthAI APK Builder"
echo "======================================"
echo ""

PROJECT_WIN="d:/انتيجرافيتي/m--01"
PROJECT_LINUX="/mnt/d/انتيجرافيتي/m--01"
BUILD_COPY="/home/$USER/healthai_build"

# ─── Step 1: System packages ──────────────────────────────────────────
echo "[1/6] Installing system packages..."
sudo apt-get update -qq
sudo apt-get install -y -qq \
    python3-pip \
    build-essential \
    git \
    zip \
    unzip \
    openjdk-17-jdk \
    autoconf \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    libffi-dev \
    libssl-dev \
    libbz2-dev \
    libsqlite3-dev \
    ccache \
    lld \
    2>/dev/null
echo "   ✅ System packages installed"

# ─── Step 2: Python packages ──────────────────────────────────────────
echo "[2/6] Installing Buildozer & dependencies..."
pip3 install --quiet --upgrade pip
pip3 install --quiet buildozer cython==0.29.33 python-for-android
echo "   ✅ Buildozer $(buildozer --version 2>&1 | head -1) installed"

# ─── Step 3: Copy project to Linux filesystem ─────────────────────────
echo "[3/6] Copying project to Linux filesystem..."
rm -rf "$BUILD_COPY"
mkdir -p "$BUILD_COPY"
cp -r "$PROJECT_LINUX/." "$BUILD_COPY/"
echo "   ✅ Project copied to $BUILD_COPY"

# ─── Step 4: Verify files ─────────────────────────────────────────────
echo "[4/6] Verifying project files..."
REQUIRED=(
    "main.py"
    "buildozer.spec"
    "screens/onboarding.py"
    "screens/home.py"
    "screens/disease_list.py"
    "screens/symptom_form.py"
    "screens/results.py"
    "models/predictor.py"
    "models/diabetes_model.pkl"
    "models/heart_model.pkl"
    "utils/theme.py"
    "data/form_schemas.py"
)

ALL_OK=true
for f in "${REQUIRED[@]}"; do
    if [ -f "$BUILD_COPY/$f" ]; then
        echo "   ✅ $f"
    else
        echo "   ❌ MISSING: $f"
        ALL_OK=false
    fi
done

if [ "$ALL_OK" = false ]; then
    echo ""
    echo "❌ Some files are missing. Please check your project."
    exit 1
fi

# ─── Step 5: Fix buildozer.spec for Linux build ───────────────────────
echo "[5/6] Updating buildozer.spec..."
cd "$BUILD_COPY"
# Remove android.branch = master (can cause issues)
sed -i '/^android\.branch/d' buildozer.spec
echo "   ✅ buildozer.spec ready"

# ─── Step 6: Build ────────────────────────────────────────────────────
echo "[6/6] Building Android APK (this takes 20-35 minutes first time)..."
echo "      Logs: $BUILD_COPY/.buildozer/logs/"
echo ""

buildozer -v android debug 2>&1 | tee build.log

# ─── Result ───────────────────────────────────────────────────────────
echo ""
APK_FILE=$(find "$BUILD_COPY/bin" -name "*.apk" 2>/dev/null | head -1)

if [ -n "$APK_FILE" ]; then
    SIZE=$(du -h "$APK_FILE" | cut -f1)
    APK_NAME=$(basename "$APK_FILE")
    
    echo "======================================"
    echo "  ✅ APK BUILT SUCCESSFULLY!"
    echo "======================================"
    echo "  File: $APK_NAME"
    echo "  Size: $SIZE"
    echo ""
    
    # Copy APK back to Windows
    cp "$APK_FILE" "$PROJECT_LINUX/bin/"
    echo "  📁 APK saved to: d:\\انتيجرافيتي\\m--01\\bin\\$APK_NAME"
    echo ""
    echo "  Install on Android: transfer the APK to your phone and tap to install."
else
    echo "======================================"
    echo "  ❌ BUILD FAILED"
    echo "======================================"
    echo "  Check build.log for details."
    echo "  Last 30 lines:"
    tail -30 build.log
fi
