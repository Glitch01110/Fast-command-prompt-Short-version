#!/usr/bin/env python3
"""
Fast Command Prompt - Short Version
A tool for managing system packages and operations via command line
"""

import subprocess
import argparse
import sys
import os
import shutil
import urllib.parse
from pathlib import Path


def run_command(command, description="", cwd=None):
    """Execute a command safely and handle errors."""
    try:
        if description:
            print(f"[*] {description}...")
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            cwd=cwd
        )
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[!] Error: {description or 'Command execution'} failed")
        if e.stderr:
            print(f"    {e.stderr}")
        return False
    except Exception as e:
        print(f"[!] Unexpected error: {e}")
        return False


def extract_repo_name(url):
    """Extract repository name from GitHub URL."""
    if url.endswith('.git'):
        url = url[:-4]
    if url.endswith('/'):
        url = url[:-1]
    return os.path.basename(url)


def install_from_source(repo_path):
    """Try to install from source code using common methods."""
    repo_path = Path(repo_path)
    if not repo_path.exists():
        return False
    
    success = False
    
    # Check for setup.py (Python package)
    if (repo_path / "setup.py").exists():
        print(f"[*] Found setup.py, installing Python package...")
        success = run_command(
            ["python3", "setup.py", "install"],
            f"Installing from setup.py",
            cwd=str(repo_path)
        )
    
    # Check for requirements.txt
    if (repo_path / "requirements.txt").exists():
        print(f"[*] Found requirements.txt, installing dependencies...")
        run_command(
            ["pip3", "install", "-r", "requirements.txt"],
            "Installing requirements",
            cwd=str(repo_path)
        )
    
    # Check for Makefile
    if (repo_path / "Makefile").exists():
        print(f"[*] Found Makefile, building and installing...")
        if run_command(["make"], "Building", cwd=str(repo_path)):
            success = run_command(
                ["sudo", "make", "install"],
                "Installing",
                cwd=str(repo_path)
            )
    
    # Check for CMakeLists.txt
    if (repo_path / "CMakeLists.txt").exists():
        print(f"[*] Found CMakeLists.txt, building with CMake...")
        build_dir = repo_path / "build"
        build_dir.mkdir(exist_ok=True)
        if run_command(["cmake", ".."], "Configuring CMake", cwd=str(build_dir)):
            if run_command(["make"], "Building", cwd=str(build_dir)):
                success = run_command(
                    ["sudo", "make", "install"],
                    "Installing",
                    cwd=str(build_dir)
                )
    
    # Check for install.sh
    if (repo_path / "install.sh").exists():
        print(f"[*] Found install.sh, running installer...")
        run_command(["chmod", "+x", "install.sh"], "Making install.sh executable", cwd=str(repo_path))
        success = run_command(
            ["bash", "install.sh"],
            "Running install.sh",
            cwd=str(repo_path)
        )
    
    # Check for install script in root
    install_scripts = ["install", "install.py", "build.sh", "build.py"]
    for script in install_scripts:
        script_path = repo_path / script
        if script_path.exists():
            print(f"[*] Found {script}, running...")
            if script.endswith('.sh'):
                run_command(["chmod", "+x", script], f"Making {script} executable", cwd=str(repo_path))
                success = run_command(["bash", script], f"Running {script}", cwd=str(repo_path))
            elif script.endswith('.py'):
                success = run_command(["python3", script], f"Running {script}", cwd=str(repo_path))
            break
    
    return success


def main():
    parser = argparse.ArgumentParser(
        description="Fast Command Prompt - System management tool",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "-ud", "--update",
        action="store_true",
        help="Update package list (apt update)"
    )
    parser.add_argument(
        "-ug", "--upgrade",
        action="store_true",
        help="Upgrade system packages (apt full-upgrade -y)"
    )
    parser.add_argument(
        "-i", "--install",
        nargs="+",
        metavar="PACKAGE",
        help="Install package(s) (apt install)"
    )
    parser.add_argument(
        "-r", "--remove",
        nargs="+",
        metavar="PACKAGE",
        help="Remove package(s) (apt remove)"
    )
    parser.add_argument(
        "-sh", "--shutdown",
        action="store_true",
        help="Shutdown the system"
    )
    parser.add_argument(
        "-ar", "--autoremove",
        action="store_true",
        help="Autoremove unnecessary packages (apt autoremove)"
    )
    parser.add_argument(
        "-ac", "--autoclean",
        action="store_true",
        help="Autoclean unnecessary packages (apt autoclean)"
    )
    parser.add_argument(
        "-ch", "--chmod",
        nargs="+",
        metavar="FILE",
        help="Make file(s) executable (chmod +x)"
    )
    parser.add_argument(
        "-deb", "--install-deb",
        nargs="+",
        metavar="FILE",
        help="Install .deb package(s) (dpkg -i)"
    )
    parser.add_argument(
        "-snap", "--install-snap",
        nargs="+",
        metavar="PACKAGE",
        help="Install snap package(s) (snap install)"
    )
    parser.add_argument(
        "-flatpak", "--install-flatpak",
        nargs="+",
        metavar="PACKAGE",
        help="Install flatpak package(s) (flatpak install)"
    )
    parser.add_argument(
        "-pip", "--install-pip",
        nargs="+",
        metavar="PACKAGE",
        help="Install Python package(s) (pip install)"
    )
    parser.add_argument(
        "-auto", "--auto-install",
        nargs="+",
        metavar="PACKAGE",
        help="Auto install: update first, then install package(s)"
    )
    parser.add_argument(
        "-gh", "--github",
        nargs="+",
        metavar="URL",
        help="Clone repository from GitHub (git clone)"
    )
    parser.add_argument(
        "-gh-install", "--github-install",
        nargs="+",
        metavar="URL",
        help="Clone and install from GitHub automatically"
    )
    parser.add_argument(
        "-dl", "--download",
        nargs="+",
        metavar="URL",
        help="Download file(s) from URL (wget)"
    )
    parser.add_argument(
        "-dl-dir", "--download-dir",
        default="./downloads",
        metavar="DIR",
        help="Directory for downloads (default: ./downloads)"
    )
    parser.add_argument(
        "-gh-dir", "--github-dir",
        default="./repos",
        metavar="DIR",
        help="Directory for cloned repositories (default: ./repos)"
    )
    parser.add_argument(
        "-src", "--install-source",
        nargs="+",
        metavar="PATH",
        help="Install from source code directory"
    )
    
    args = parser.parse_args()
    
    # Check if any option was provided
    if not any(vars(args).values()):
        parser.print_help()
        sys.exit(1)
    
    success = True
    
    # Execute commands only if their options are provided
    if args.update:
        success &= run_command(
            ["apt", "update"],
            "Updating package list"
        )
    
    if args.upgrade:
        success &= run_command(
            ["apt", "full-upgrade", "-y"],
            "Upgrading system packages"
        )
    
    if args.install:
        packages = " ".join(args.install)
        success &= run_command(
            ["apt", "install", "-y"] + args.install,
            f"Installing package(s): {packages}"
        )
    
    if args.auto_install:
        packages = " ".join(args.auto_install)
        print(f"[*] Auto-installing package(s): {packages}")
        # Update first
        if run_command(["apt", "update"], "Updating package list"):
            # Then install
            success &= run_command(
                ["apt", "install", "-y"] + args.auto_install,
                f"Installing package(s): {packages}"
            )
        else:
            success = False
    
    if args.remove:
        packages = " ".join(args.remove)
        success &= run_command(
            ["apt", "remove", "-y"] + args.remove,
            f"Removing package(s): {packages}"
        )
    
    if args.autoremove:
        success &= run_command(
            ["apt", "autoremove", "-y"],
            "Autoremoving unnecessary packages"
        )
    
    if args.autoclean:
        success &= run_command(
            ["apt", "autoclean"],
            "Autocleaning unnecessary packages"
        )
    
    if args.chmod:
        for file_path in args.chmod:
            if os.path.exists(file_path):
                success &= run_command(
                    ["chmod", "+x", file_path],
                    f"Making {file_path} executable"
                )
            else:
                print(f"[!] Error: File '{file_path}' not found")
                success = False
    
    if args.install_deb:
        for deb_file in args.install_deb:
            if os.path.exists(deb_file):
                success &= run_command(
                    ["dpkg", "-i", deb_file],
                    f"Installing .deb package: {deb_file}"
                )
                # Fix dependencies if needed
                run_command(
                    ["apt", "install", "-f", "-y"],
                    "Fixing dependencies"
                )
            else:
                print(f"[!] Error: File '{deb_file}' not found")
                success = False
    
    if args.install_snap:
        packages = " ".join(args.install_snap)
        success &= run_command(
            ["snap", "install"] + args.install_snap,
            f"Installing snap package(s): {packages}"
        )
    
    if args.install_flatpak:
        packages = " ".join(args.install_flatpak)
        success &= run_command(
            ["flatpak", "install", "-y"] + args.install_flatpak,
            f"Installing flatpak package(s): {packages}"
        )
    
    if args.install_pip:
        packages = " ".join(args.install_pip)
        success &= run_command(
            ["pip3", "install"] + args.install_pip,
            f"Installing Python package(s): {packages}"
        )
    
    if args.github:
        # Create repos directory if it doesn't exist
        repos_dir = Path(args.github_dir)
        repos_dir.mkdir(parents=True, exist_ok=True)
        
        for repo_url in args.github:
            repo_name = extract_repo_name(repo_url)
            repo_path = repos_dir / repo_name
            
            if repo_path.exists():
                print(f"[!] Repository '{repo_name}' already exists. Skipping clone.")
                print(f"    Use --github-install to update and install, or remove {repo_path}")
                continue
            
            print(f"[*] Cloning {repo_url}...")
            success &= run_command(
                ["git", "clone", repo_url, str(repo_path)],
                f"Cloning repository: {repo_name}"
            )
            if repo_path.exists():
                print(f"[+] Repository cloned to: {repo_path}")
    
    if args.github_install:
        # Create repos directory if it doesn't exist
        repos_dir = Path(args.github_dir)
        repos_dir.mkdir(parents=True, exist_ok=True)
        
        for repo_url in args.github_install:
            repo_name = extract_repo_name(repo_url)
            repo_path = repos_dir / repo_name
            
            # Clone or update repository
            if repo_path.exists():
                print(f"[*] Repository '{repo_name}' exists, updating...")
                success &= run_command(
                    ["git", "pull"],
                    f"Updating repository: {repo_name}",
                    cwd=str(repo_path)
                )
            else:
                print(f"[*] Cloning {repo_url}...")
                success &= run_command(
                    ["git", "clone", repo_url, str(repo_path)],
                    f"Cloning repository: {repo_name}"
                )
            
            # Try to install from source
            if repo_path.exists():
                print(f"\n[*] Attempting to install {repo_name}...")
                install_success = install_from_source(repo_path)
                if install_success:
                    print(f"[+] Successfully installed {repo_name}")
                else:
                    print(f"[!] Could not auto-install {repo_name}")
                    print(f"    Repository is at: {repo_path}")
                    print(f"    Please install manually or check the repository for installation instructions")
    
    if args.download:
        # Create downloads directory if it doesn't exist
        downloads_dir = Path(args.download_dir)
        downloads_dir.mkdir(parents=True, exist_ok=True)
        
        for url in args.download:
            filename = os.path.basename(urllib.parse.urlparse(url).path)
            if not filename:
                filename = "downloaded_file"
            file_path = downloads_dir / filename
            
            print(f"[*] Downloading {url}...")
            # Try wget first, then curl
            if shutil.which("wget"):
                success &= run_command(
                    ["wget", "-O", str(file_path), url],
                    f"Downloading to {file_path}"
                )
            elif shutil.which("curl"):
                success &= run_command(
                    ["curl", "-L", "-o", str(file_path), url],
                    f"Downloading to {file_path}"
                )
            else:
                print("[!] Error: Neither wget nor curl is available")
                success = False
            
            if file_path.exists():
                print(f"[+] File downloaded to: {file_path}")
                # If it's a script, make it executable
                if filename.endswith(('.sh', '.py')):
                    run_command(["chmod", "+x", str(file_path)], f"Making {filename} executable")
    
    if args.install_source:
        for source_path in args.install_source:
            source_path = Path(source_path)
            if source_path.exists():
                print(f"[*] Installing from source: {source_path}")
                install_success = install_from_source(source_path)
                if install_success:
                    print(f"[+] Successfully installed from {source_path}")
                else:
                    print(f"[!] Could not auto-install from {source_path}")
                    success = False
            else:
                print(f"[!] Error: Path '{source_path}' not found")
                success = False
    
    if args.shutdown:
        print("[!] Shutting down the system...")
        run_command(
            ["shutdown", "now"],
            "System shutdown"
        )
    
    if success:
        print("\n[+] All tasks completed successfully.")
    else:
        print("\n[!] Some tasks failed. Please check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()