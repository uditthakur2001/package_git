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

    # Download and install Gitleaks
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

def run_gitleaks(repo_path, report_format="json", output_file="gitleaks_report.json"):
    """Run Gitleaks on the specified repository."""
    command = [
        "gitleaks",
        "detect",
        "-s", repo_path,
        "-r", output_file,
        "--format", report_format
    ]
    run_command(command)
    print(f"Scan complete. Report saved to {output_file}.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python gitleaks_app.py <repo_path> [report_format] [output_file]")
        sys.exit(1)

    repo_path = sys.argv[1]
    report_format = sys.argv[2] if len(sys.argv) > 2 else "json"
    output_file = sys.argv[3] if len(sys.argv) > 3 else "gitleaks_report.json"

    # Ensure Gitleaks is installed
    install_gitleaks()

    # Run Gitleaks
    run_gitleaks(repo_path, report_format, output_file)

if __name__ == "__main__":
    main()
