#!/bin/bash
# Setup script for Kotlin code generator

set -e

echo "========================================="
echo "Kotlin Code Generator Setup"
echo "========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create grammars directory if it doesn't exist
mkdir -p grammars

# Download Kotlin grammar if not exists
if [ ! -d "grammars/kotlin-spec-release" ]; then
    echo ""
    echo "Downloading Kotlin grammar specification..."
    cd grammars
    if ! curl -L -o kotlin-spec.tar.gz https://github.com/Kotlin/kotlin-spec/archive/refs/heads/release.tar.gz; then
        echo "Failed to download Kotlin grammar"
        exit 1
    fi
    
    if ! tar -xzf kotlin-spec.tar.gz; then
        echo "Failed to extract Kotlin grammar"
        exit 1
    fi
    cd ..
fi

# Verify grammar files exist
if [ ! -d "grammars/kotlin-spec-release/grammar/src/main/antlr" ]; then
    echo "Error: Grammar files not found in expected location"
    exit 1
fi

# Copy grammar files
echo ""
echo "Copying grammar files..."
if ! cp grammars/kotlin-spec-release/grammar/src/main/antlr/*.g4 grammars/; then
    echo "Error: Failed to copy grammar files"
    exit 1
fi

# Clean RCURL action from lexer
echo ""
echo "Cleaning Java actions from grammar..."
if ! grep -q "RCURL:" grammars/KotlinLexer.g4; then
    echo "Warning: RCURL rule not found in KotlinLexer.g4, skipping cleanup"
else
    sed 's/RCURL: .*/RCURL: "}";/' grammars/KotlinLexer.g4 > grammars/KotlinLexer_clean.g4
fi

# Process grammar with Grammarinator
if [ ! -f "grammars/KotlinGenerator.py" ]; then
    echo ""
    echo "Processing grammar with Grammarinator..."
    grammarinator-process grammars/KotlinLexer_clean.g4 grammars/KotlinParser.g4 -o grammars/
fi

# Check if Kotlin is installed
echo ""
echo "Checking Kotlin installation..."
if command -v kotlinc &> /dev/null; then
    kotlinc -version
else
    echo "Kotlin compiler not found!"
    echo ""
    echo "WARNING: About to install SDKMan and Kotlin 2.2.20"
    echo "This involves downloading and executing scripts from the internet."
    echo "Press Ctrl+C to cancel or Enter to continue..."
    read -r
    
    # Install SDKMan if not installed
    if [ ! -d "$HOME/.sdkman" ]; then
        echo "Downloading and installing SDKMan..."
        if ! curl -s "https://get.sdkman.io" -o /tmp/sdkman-installer.sh; then
            echo "Failed to download SDKMan installer"
            exit 1
        fi
        bash /tmp/sdkman-installer.sh
        rm /tmp/sdkman-installer.sh
        source "$HOME/.sdkman/bin/sdkman-init.sh"
    fi
    
    # Install Kotlin
    source "$HOME/.sdkman/bin/sdkman-init.sh"
    sdk install kotlin 2.2.20
fi

# Create output directory
mkdir -p generated_code

echo ""
echo "========================================="
echo "Setup complete!"
echo "========================================="
echo ""
echo "Try generating a complex valid program (recommended):"
echo "  python3 generate_complex.py -o generated_code/example.kt --run"
echo ""
echo "Or use grammar-based generation for fuzzing:"
echo "  python3 generate_kotlin.py -o generated_code/example.kt"
echo ""
echo "Run batch tests:"
echo "  python3 batch_test.py -n 10"
