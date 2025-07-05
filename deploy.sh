#!/bin/bash

# 🚀 Quick Deployment Script for Kenyan Payroll System
# This script helps you deploy to Vercel quickly

echo "🇰🇪 Kenyan Payroll Management System - Vercel Deployment"
echo "======================================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
fi

# Add all files
echo "📦 Adding files to Git..."
git add .

# Commit changes
echo "💾 Committing changes..."
read -p "Enter commit message (or press Enter for default): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Deploy Kenyan Payroll System to Vercel"
fi
git commit -m "$commit_msg"

# Check if remote exists
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "🔗 Setting up GitHub remote..."
    read -p "Enter your GitHub username: " github_username
    read -p "Enter repository name (default: kenyan-payroll-system): " repo_name
    if [ -z "$repo_name" ]; then
        repo_name="kenyan-payroll-system"
    fi
    
    git remote add origin "https://github.com/$github_username/$repo_name.git"
    echo "✅ Remote added: https://github.com/$github_username/$repo_name.git"
    echo ""
    echo "🚨 IMPORTANT: Create this repository on GitHub first!"
    echo "   1. Go to https://github.com/new"
    echo "   2. Repository name: $repo_name"
    echo "   3. Make it public or private"
    echo "   4. Don't initialize with README (we have files already)"
    echo "   5. Click 'Create repository'"
    echo ""
    read -p "Press Enter when you've created the repository on GitHub..."
fi

# Push to GitHub
echo "🚀 Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ Code pushed to GitHub successfully!"
echo ""
echo "🌐 Next Steps for Vercel Deployment:"
echo "1. Go to https://vercel.com/dashboard"
echo "2. Click 'New Project'"
echo "3. Import your GitHub repository"
echo "4. Configure these settings:"
echo "   - Framework Preset: Other"
echo "   - Build Command: chmod +x build_files.sh && ./build_files.sh"
echo "   - Output Directory: staticfiles_build"
echo "5. Deploy!"
echo ""
echo "🗄️ Don't forget to:"
echo "1. Create a Postgres database in Vercel"
echo "2. Set environment variables:"
echo "   - DATABASE_URL (from your Postgres database)"
echo "   - SECRET_KEY (generate a secure one)"
echo "   - VERCEL=1"
echo "   - DJANGO_SUPERUSER_USERNAME=admin"
echo "   - DJANGO_SUPERUSER_EMAIL=admin@yourcompany.com"
echo "   - DJANGO_SUPERUSER_PASSWORD=YourSecurePassword123!"
echo ""
echo "🎉 Your Kenyan Payroll System will be live soon!"
