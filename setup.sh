#!/bin/bash

# File name
FILE_NAME="mistral-7b-instruct-v0.2.Q4_K_M.gguf"

# Check if the file already exists
if [ ! -f "/data/$FILE_NAME" ]; then
    # Download the file
    wget -O "/data/$FILE_NAME" https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf
fi

# Make the binary executable
chmod 755 "/data/$FILE_NAME"

# Execute the binary
# sh -c for if mac has zsh issues
sh -c "/data/$FILE_NAME --host 0.0.0.0"