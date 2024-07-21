#!/bin/bash

# Ensure the Docker network exists (this is just a safeguard step now)
docker network create my-network || true

# Clone the repository
git clone <https://github.com/changyuhsin1999/Travel_Assistant> repo

# Change to the repository directory
cd repo

# Copy the llamafile from Downloads to the repository directory
cp ~/Downloads/mistral-7b-instruct-v0.1-Q4_K_M.llamafile .

# Make the llamafile executable
chmod +x mistral-7b-instruct-v0.1-Q4_K_M.llamafile