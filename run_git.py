import os
import subprocess

print("🚀 Starting Git setup...")

# Remove .git if exists
if os.path.exists(".git"):
    import shutil
    shutil.rmtree(".git")
    print("🗑️ Removed old .git")

# Run Git commands
commands = [
    'git init',
    'git config --global user.email "heliopsis@outlook.be"',
    'git config --global user.name "Heliopsis"',
    'git add .',
    'git commit -m "Initial commit: Complete Heliopsis Email System in English"',
    'git remote add origin https://github.com/chichermo/heliopsisemails.git',
    'git push -u origin main'
]

for cmd in commands:
    print(f"▶️ Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Success: {cmd}")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {cmd}")
        print(f"   Error: {e.stderr}")
        break

print("🎯 Git setup complete!")
