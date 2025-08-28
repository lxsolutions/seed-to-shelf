








#!/bin/bash

# Push Seed to Chef monorepo to GitHub
echo "Pushing Seed to Chef monorepo to GitHub..."

cd /workspace/seed-to-chef || exit 1

git remote -v | grep github > /dev/null
if [ $? -ne 0 ]; then
    echo "Adding GitHub remote..."
    git remote add origin https://github.com/lxsolutions/seed-to-chef.git
fi

echo "Pushing to main branch..."
git push origin main --force-with-lease

echo "Seed to Chef monorepo pushed to GitHub!"
echo "Repository: https://github.com/lxsolutions/seed-to-chef"






