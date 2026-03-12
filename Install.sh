#!/bin/bash

set -e

echo "=== Image Creator External - Post Installation ==="
echo

# Check if skill is installed
source_dir="$HOME/.agents/skills/image-creator-external"
if [ ! -d "$source_dir" ]; then
    echo "Error: Skill not found at $source_dir"
    echo "Please run: npx skills add yige666s/image-creator-external first"
    exit 1
fi

# Ask user to select target tool
echo "Select the tool to create symlink for:"
echo "1) openclaw (~/.openclaw/skills)"
echo "2) claudecode (~/.claude/skills)"
echo "3) both"
read -p "Enter your choice (1, 2, or 3): " choice

create_symlink() {
    local target_dir=$1
    local tool_name=$2

    mkdir -p "$target_dir"
    local target_link="$target_dir/image-creator-external"

    if [ -L "$target_link" ] || [ -e "$target_link" ]; then
        echo "⚠️  Already exists: $target_link"
        read -p "Recreate it? (y/n): " recreate
        if [[ "$recreate" =~ ^[Yy]$ ]]; then
            rm -rf "$target_link"
        else
            echo "Skipped $tool_name"
            return
        fi
    fi

    ln -s "$source_dir" "$target_link"
    echo "✓ Created symlink for $tool_name: $target_link"
}

case $choice in
    1)
        create_symlink "$HOME/.openclaw/skills" "openclaw"
        ;;
    2)
        create_symlink "$HOME/.claude/skills" "claudecode"
        ;;
    3)
        create_symlink "$HOME/.openclaw/skills" "openclaw"
        create_symlink "$HOME/.claude/skills" "claudecode"
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo
echo "✅ Post-installation completed!"
