#!/bin/bash

set -e

echo "=== Image Creator External Skill Installer ==="
echo

# Check if npx is installed
if ! command -v npx &> /dev/null; then
    echo "npx is not installed."
    read -p "Would you like to install Node.js (which includes npx)? (y/n): " install_node
    if [[ "$install_node" =~ ^[Yy]$ ]]; then
        echo "Please install Node.js from https://nodejs.org/ or use a package manager:"
        echo "  - macOS: brew install node"
        echo "  - Linux: apt install nodejs npm (or equivalent)"
        exit 1
    else
        echo "Installation cancelled. npx is required to continue."
        exit 1
    fi
fi

# Install skill using npx
echo "Installing skill via npx..."
npx skills add yige666s/image-creator-external

# Ask user to select target tool
echo
echo "Select the tool to install this skill for:"
echo "1) openclaw"
echo "2) claudecode"
read -p "Enter your choice (1 or 2): " choice

case $choice in
    1)
        target_dir="$HOME/.openclaw/skills"
        tool_name="openclaw"
        ;;
    2)
        target_dir="$HOME/.claude/skills"
        tool_name="claudecode"
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

# Create target directory if it doesn't exist
mkdir -p "$target_dir"

# Create symlink
source_dir="$HOME/.agents/skills/image-creator-external"
target_link="$target_dir/image-creator-external"

if [ -L "$target_link" ]; then
    echo "Symlink already exists at $target_link"
    read -p "Do you want to recreate it? (y/n): " recreate
    if [[ "$recreate" =~ ^[Yy]$ ]]; then
        rm "$target_link"
    else
        echo "Installation completed (symlink unchanged)."
        exit 0
    fi
fi

ln -s "$source_dir" "$target_link"
echo "✓ Created symlink: $target_link -> $source_dir"
echo
echo "Installation completed for $tool_name!"
