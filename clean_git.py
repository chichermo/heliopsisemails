import os
import subprocess
import time

print("🧹 Cleaning Git repository...")

# Force remove .git directory
if os.path.exists(".git"):
    try:
        subprocess.run("rmdir /s /q .git", shell=True, check=True)
        print("✅ Removed .git directory")
    except:
        print("⚠️ Could not remove .git, continuing...")

# Wait a moment
time.sleep(1)

# Initialize new Git repository
print("🚀 Initializing new Git repository...")
subprocess.run("git init", shell=True, check=True)
print("✅ Git initialized")

# Configure Git
print("⚙️ Configuring Git...")
subprocess.run('git config user.email "heliopsis@outlook.be"', shell=True, check=True)
subprocess.run('git config user.name "Heliopsis"', shell=True, check=True)
print("✅ Git configured")

# Add all files
print("📁 Adding files...")
subprocess.run("git add .", shell=True, check=True)
print("✅ Files added")

# Commit
print("💾 Committing...")
subprocess.run('git commit -m "Initial commit: Complete Heliopsis Email System"', shell=True, check=True)
print("✅ Committed")

# Add remote
print("🔗 Adding remote...")
subprocess.run("git remote add origin https://github.com/chichermo/heliopsisemails.git", shell=True, check=True)
print("✅ Remote added")

# Push
print("🚀 Pushing to GitHub...")
subprocess.run("git push -u origin main", shell=True, check=True)
print("✅ Pushed to GitHub!")

print("🎉 All done!")
