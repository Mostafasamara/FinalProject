import subprocess

# Get list of installed packages
installed_packages = subprocess.run(["pip", "freeze"], capture_output=True, text=True).stdout.split("\n")

# Uninstall each package
for package in installed_packages:
    if package:  # Skip empty lines
        package_name = package.split("==")[0]  # Extract package name
        print(f"Uninstalling {package_name}...")
        subprocess.run(["pip", "uninstall", "-y", package_name])

print("✅ All packages uninstalled!")
