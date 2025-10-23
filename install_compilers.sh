#!/bin/bash
# Install Kotlin Native compilers for fuzzing
# This script installs two versions: 2.0.0 (baseline) and 2.2.20 (SUT)

set -e

echo "========================================="
echo "Kotlin Native Compiler Installation"
echo "========================================="
echo ""

# Installation directory
INSTALL_DIR="/usr/local"
if [ ! -w "$INSTALL_DIR" ]; then
    echo "Warning: Cannot write to $INSTALL_DIR, using $HOME/.local instead"
    INSTALL_DIR="$HOME/.local"
    mkdir -p "$INSTALL_DIR"
fi

echo "Installing to: $INSTALL_DIR"
echo ""

# Function to install Kotlin Native compiler
install_kotlin_native() {
    local VERSION=$1
    local INSTALL_PATH="$INSTALL_DIR/kotlinc-$VERSION"
    
    if [ -d "$INSTALL_PATH" ]; then
        echo "Kotlin Native $VERSION already installed at $INSTALL_PATH"
        return 0
    fi
    
    echo "Installing Kotlin Native $VERSION..."
    
    # Download URL
    local URL="https://github.com/JetBrains/kotlin/releases/download/v${VERSION}/kotlin-native-prebuilt-linux-x86_64-${VERSION}.tar.gz"
    local TMP_FILE="/tmp/kotlin-native-${VERSION}.tar.gz"
    
    echo "  Downloading from $URL"
    if ! curl -L -o "$TMP_FILE" "$URL"; then
        echo "  Error: Failed to download Kotlin Native $VERSION"
        return 1
    fi
    
    echo "  Extracting..."
    local TMP_DIR="/tmp/kotlin-native-${VERSION}"
    mkdir -p "$TMP_DIR"
    
    if ! tar -xzf "$TMP_FILE" -C "$TMP_DIR"; then
        echo "  Error: Failed to extract Kotlin Native $VERSION"
        rm -f "$TMP_FILE"
        return 1
    fi
    
    # Move to installation directory
    echo "  Installing to $INSTALL_PATH"
    mv "$TMP_DIR/kotlin-native-prebuilt-linux-x86_64-${VERSION}" "$INSTALL_PATH"
    
    # Cleanup
    rm -f "$TMP_FILE"
    rm -rf "$TMP_DIR"
    
    # Verify installation
    if [ -x "$INSTALL_PATH/bin/kotlinc-native" ]; then
        echo "  ✓ Kotlin Native $VERSION installed successfully"
        echo "    Path: $INSTALL_PATH"
        return 0
    else
        echo "  Error: kotlinc-native not found after installation"
        return 1
    fi
}

# Install baseline version (2.0.0)
echo "=== Installing Baseline Compiler ==="
if ! install_kotlin_native "2.0.0"; then
    echo "Failed to install baseline compiler"
    exit 1
fi
echo ""

# Install SUT version (2.2.20)  
echo "=== Installing SUT Compiler ==="
if ! install_kotlin_native "2.2.20"; then
    echo "Failed to install SUT compiler"
    exit 1
fi
echo ""

echo "========================================="
echo "Installation Complete!"
echo "========================================="
echo ""
echo "Installed compilers:"
echo "  Baseline: $INSTALL_DIR/kotlinc-2.0.0"
echo "  SUT: $INSTALL_DIR/kotlinc-2.2.20"
echo ""
echo "You can now run the fuzzer:"
echo "  python3 fuzzer.py -n 100 --baseline $INSTALL_DIR/kotlinc-2.0.0 --sut $INSTALL_DIR/kotlinc-2.2.20"
echo ""
