import subprocess
import sys

def install_chocolatey():
    try:
        subprocess.run(['choco', '--version'], check=True, stdout=subprocess.PIPE)
        print("Chocolatey is already installed.")
    except subprocess.CalledProcessError:
        print("Installing Chocolatey...")
        subprocess.run([
            'powershell', '-NoProfile', '-Command',
            'iex ((New-Object System.Net.WebClient).DownloadString("https://community.chocolatey.org/install.ps1"))'
        ], check=True)

def install_tool(tool, installer_cmd):
    print(f"Installing {tool}...")
    try:
        subprocess.run(installer_cmd, check=True)
    except subprocess.CalledProcessError:
        print(f"Failed to install {tool}.")
        sys.exit(1)

def install_python():
    try:
        subprocess.run(['python', '--version'], check=True, stdout=subprocess.PIPE)
        print("Python is already installed.")
    except subprocess.CalledProcessError:
        print("Installing Python...")
        install_tool("Python", ['choco', 'install', 'python', '-y'])

def install_owasp_zap():
    try:
        result = subprocess.run(['zap', '-version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("OWASP ZAP is already installed.")
        print("OWASP ZAP version:", result.stdout.decode().strip())
    except FileNotFoundError:
        print("OWASP ZAP not found. Installing OWASP ZAP...")
        try:
            subprocess.run(['choco', 'install', 'owasp-zap', '-y'], check=True)
        except subprocess.CalledProcessError as e:
            print("Failed to install OWASP ZAP:", e)
            sys.exit(1)

def install_trufflehog():
    try:
        subprocess.run(['pip', 'show', 'truffleHog'], check=True, stdout=subprocess.PIPE)
        print("TruffleHog is already installed.")
    except subprocess.CalledProcessError:
        print("Installing TruffleHog...")
        subprocess.run(['pip', 'install', 'truffleHog'], check=True)

def install_gitleaks():
    try:
        result = subprocess.run(['gitleaks', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Gitleaks is already installed.")
        print("Gitleaks version:", result.stdout.decode().strip())
    except FileNotFoundError:
        print("Gitleaks not found. Installing Gitleaks...")
        try:
            subprocess.run(['choco', 'install', 'gitleaks', '-y'], check=True)
        except subprocess.CalledProcessError as e:
            print("Failed to install Gitleaks:", e)

def main():
    # Run as Administrator
    if 'administrators' not in subprocess.run(['whoami', '/groups'], capture_output=True, text=True).stdout.lower():
        print("Please run this script as an Administrator!")
        sys.exit(1)

    install_chocolatey()
    # install_tool("OWASP ZAP", ['choco', 'install', 'owasp-zap', '-y'])
    # install_tool("Gitleaks", ['choco', 'install', 'gitleaks', '-y'])
    install_python()
    install_trufflehog()
    install_gitleaks()
    install_owasp_zap()


    print("Installation complete!")

if __name__ == '__main__':
    main()
