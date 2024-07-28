# Create a requirements.txt file
echo "Creating requirements.txt..."
pip freeze > requirements.txt

# Add all changes to git
echo "Adding changes to git..."
git add .

# Commit changes with the current timestamp
timestamp=$(date +"%Y-%m-%d %H:%M:%S")
commit_message="Update and push at $timestamp"
echo "Committing changes with message: '$commit_message'"
git commit -m "$commit_message"

# Push changes to the repository
echo "Pushing changes to GitHub..."
git push .

echo "Done!"