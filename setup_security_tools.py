import subprocess
import sys
import shutil
import gitleaks


def install_tool(tool_name, install_command, version_command):
    try:
        result = subprocess.run(version_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"{tool_name} is already installed.")
        print(f"{tool_name} version:", result.stdout.decode().strip())
    except subprocess.CalledProcessError:
        print(f"{tool_name} not found or not installed correctly. Installing {tool_name}...")
        try:
            subprocess.run(install_command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {tool_name}:", e)
            sys.exit(1)
    except FileNotFoundError:
        print(f"{tool_name} is not installed. Attempting to install...")
        try:
            subprocess.run(install_command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {tool_name}:", e)
            sys.exit(1)

def install_owasp_zap():
    install_tool('OWASP ZAP', ['choco', 'install', 'owasp-zap', '-y'], ['zap', '-version'])

def install_trufflehog():
    try:
        subprocess.run(['pip', 'show', 'truffleHog'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("TruffleHog is already installed.")
    except subprocess.CalledProcessError:
        print("TruffleHog not found. Installing TruffleHog...")
        try:
            subprocess.run(['pip', 'install', 'truffleHog'], check=True)
        except subprocess.CalledProcessError as e:
            print("Failed to install TruffleHog:", e)
            sys.exit(1)


def run_script():
    gitleaks.main()

def main():
    install_owasp_zap()
    install_trufflehog()
    print("Installation complete!")

if __name__ == '__main__':
    run_script()
    main()
