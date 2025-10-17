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

# Download Kotlin grammar if not exists
if [ ! -d "grammars/kotlin-spec-release" ]; then
    echo ""
    echo "Downloading Kotlin grammar specification..."
    cd grammars
    curl -L -o kotlin-spec.tar.gz https://github.com/Kotlin/kotlin-spec/archive/refs/heads/release.tar.gz
    tar -xzf kotlin-spec.tar.gz
    cd ..
fi

# Copy grammar files
echo ""
echo "Copying grammar files..."
cp grammars/kotlin-spec-release/grammar/src/main/antlr/*.g4 grammars/

# Clean RCURL action from lexer
echo ""
echo "Cleaning Java actions from grammar..."
sed 's/RCURL: .*/RCURL: "}";/' grammars/KotlinLexer.g4 > grammars/KotlinLexer_clean.g4

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
    echo "Installing Kotlin 2.2.20 via SDKMan..."
    
    # Install SDKMan if not installed
    if [ ! -d "$HOME/.sdkman" ]; then
        curl -s "https://get.sdkman.io" | bash
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
echo "Try generating a Kotlin file:"
echo "  python3 generate_kotlin.py -o generated_code/example.kt"
echo ""
echo "Or run a batch test:"
echo "  python3 batch_test.py -n 10"
