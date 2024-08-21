#!/bin/bash

# Navigate to the repository directory
cd /home/pi/piBASE

# Check if the directory exists
if [ $? -ne 0 ]; then
    echo "Directory not found! Please check the path and try again."
    exit 1
fi

# Prompt for a commit message
read -p "Enter commit message: " commit_message

# Add all files to the staging area
git add .

# Commit the changes with the provided message
git commit -m "$commit_message"

# Check if commit was successful
if [ $? -ne 0 ]; then
    echo "Commit failed. Please check for any errors."
    exit 1
fi

# Push the changes to the remote repository
git push origin main

# Check if push was successful
if [ $? -ne 0 ]; then
    echo "Push failed. Please check for any errors."
    exit 1
fi

echo "Changes have been successfully pushed to the repository!"
