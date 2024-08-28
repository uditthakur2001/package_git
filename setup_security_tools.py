import subprocess
import sys
import os
import shutil

def run_command(command):
    """Run a system command and print the output."""
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        sys.exit(1)

def install_gitleaks():
    """Install Gitleaks if not already installed."""
    if shutil.which("gitleaks") is not None:
        print("Gitleaks is already installed.")
        return

    gitleaks_url = "https://github.com/gitleaks/gitleaks/releases/latest/download/gitleaks-windows-amd64.exe"
    gitleaks_exe = "gitleaks.exe"
    print("Downloading Gitleaks...")
    run_command(["curl", "-L", "-o", gitleaks_exe, gitleaks_url])

    # Move Gitleaks to a directory in the PATH
    gitleaks_path = os.path.join(os.getenv("ProgramFiles"), "Gitleaks")
    if not os.path.exists(gitleaks_path):
        os.makedirs(gitleaks_path)

    shutil.move(gitleaks_exe, os.path.join(gitleaks_path, gitleaks_exe))

    # Add Gitleaks to PATH
    os.environ["PATH"] += os.pathsep + gitleaks_path

    print("Gitleaks installed successfully.")
    version = subprocess.run(["gitleaks", "--version"], check=True, stdout=subprocess.PIPE, text=True)
    print(f"Gitleaks version: {version.stdout.strip()}")

def install_trufflehog():
    """Install TruffleHog using pip if not already installed."""
    try:
        subprocess.run(['pip', 'show', 'truffleHog'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("TruffleHog is already installed.")
    except subprocess.CalledProcessError:
        print("TruffleHog not found. Installing TruffleHog...")
        try:
            subprocess.run(['pip', 'install', 'truffleHog'], check=True)
            print("TruffleHog installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install TruffleHog: {e}")
            sys.exit(1)

# def install_zap():
#     """Install OWASP ZAP using Chocolatey."""
#     if shutil.which("zap") is not None:
#         print("OWASP ZAP is already installed.")
#         return

#     print("Installing OWASP ZAP...")
#     try:
#         subprocess.run(["choco", "install", "owasp-zap", "-y"], check=True)
#         print("OWASP ZAP installed successfully.")
#     except subprocess.CalledProcessError as e:
#         print(f"Failed to install OWASP ZAP: {e}")
#         sys.exit(1)

def main():
    # Ensure Chocolatey is installed
    if shutil.which("choco") is None:
        print("Chocolatey is not installed. Installing Chocolatey...")
        install_choco()

    # Install the tools
    install_gitleaks()
    install_trufflehog()
    # install_zap()

    print("All tools have been installed successfully!")

def install_choco():
    """Install Chocolatey if not already installed."""
    try:
        subprocess.run(
            [
                "powershell",
                "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
            ],
            check=True
        )
        print("Chocolatey installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Chocolatey: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
