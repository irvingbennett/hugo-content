#!/bin/bash

LIST_FILE="caption.txt"
OUTPUT_TAR="posts_to_fix.tar.gz"

if [ ! -f "$LIST_FILE" ]; then
    echo "❌ Error: $LIST_FILE not found in the current directory!"
    exit 1
fi

echo "📦 Reading $LIST_FILE and preparing archive..."

# Read lines safely, handling whitespace and stripping carriage returns
files_to_add=()
while IFS= read -r line || [[ -n "$line" ]]; do
    # Strip carriage returns and leading/trailing whitespace
    clean_path=$(echo "$line" | tr -d '\r' | xargs)
    
    if [ -n "$clean_path" ]; then
        if [ -f "$clean_path" ]; then
            files_to_add+=("$clean_path")
        else
            echo "⚠️  Skipping (File not found): $clean_path"
        fi
    fi
done < "$LIST_FILE"

if [ ${#files_to_add[@]} -eq 0 ]; then
    echo "❌ No valid files found to add to the archive."
    exit 1
fi

echo "🗜️  Archiving ${#files_to_add[@]} files into $OUTPUT_TAR..."
tar -cvzf "$OUTPUT_TAR" "${files_to_add[@]}"

echo "🎯 Finished! You can now download $OUTPUT_TAR and drop it into AI Studio."
