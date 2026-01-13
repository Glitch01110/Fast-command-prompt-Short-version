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


def run_command(command, description="", cwd=None, show_output=True):
    """Execute a command safely and handle errors with real-time output."""
    try:
        if description:
            print(f"\n{'='*60}")
            print(f"[*] {description}...")
            print(f"{'='*60}")
            print(f"[>] Command: {' '.join(command)}")
            if cwd:
                print(f"[>] Working directory: {cwd}")
            print(f"{'-'*60}\n")
        
        # Show output in real-time
        if show_output:
            result = subprocess.run(
                command,
                check=True,
                text=True,
                cwd=cwd
            )
        else:
            # For commands that need captured output
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                cwd=cwd
            )
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
        
        print(f"\n{'='*60}")
        print(f"[+] Success: {description or 'Command executed successfully'}")
        print(f"{'='*60}\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n{'='*60}")
        print(f"[!] Error: {description or 'Command execution'} failed")
        print(f"[!] Exit code: {e.returncode}")
        if hasattr(e, 'stderr') and e.stderr:
            print(f"[!] Error output:\n{e.stderr}")
        if hasattr(e, 'stdout') and e.stdout:
            print(f"[!] Standard output:\n{e.stdout}")
        print(f"{'='*60}\n")
        return False
    except FileNotFoundError as e:
        print(f"\n{'='*60}")
        print(f"[!] Error: Command not found: {command[0]}")
        print(f"[!] Please install the required tool: {command[0]}")
        print(f"{'='*60}\n")
        return False
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"[!] Unexpected error: {type(e).__name__}: {e}")
        print(f"{'='*60}\n")
        return False


def get_dir_size(path):
    """Get directory size in human readable format."""
    try:
        total = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.exists(filepath):
                    total += os.path.getsize(filepath)
        
        # Convert to human readable
        for unit in ['B', 'KB', 'MB', 'GB']:
            if total < 1024.0:
                return f"{total:.2f} {unit}"
            total /= 1024.0
        return f"{total:.2f} TB"
    except:
        return "Unknown"


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
        print(f"[!] Path does not exist: {repo_path}")
        return False
    
    print(f"\n{'='*60}")
    print(f"[*] Scanning for installation methods in: {repo_path.absolute()}")
    print(f"{'='*60}\n")
    
    success = False
    found_methods = []
    
    # Check for setup.py (Python package)
    if (repo_path / "setup.py").exists():
        found_methods.append("setup.py (Python package)")
        print(f"[*] ✓ Found setup.py")
    
    # Check for requirements.txt
    if (repo_path / "requirements.txt").exists():
        found_methods.append("requirements.txt (Python dependencies)")
        print(f"[*] ✓ Found requirements.txt")
    
    # Check for Makefile
    if (repo_path / "Makefile").exists():
        found_methods.append("Makefile (C/C++ build)")
        print(f"[*] ✓ Found Makefile")
    
    # Check for CMakeLists.txt
    if (repo_path / "CMakeLists.txt").exists():
        found_methods.append("CMakeLists.txt (CMake build)")
        print(f"[*] ✓ Found CMakeLists.txt")
    
    # Check for install.sh
    if (repo_path / "install.sh").exists():
        found_methods.append("install.sh (Install script)")
        print(f"[*] ✓ Found install.sh")
    
    # Check for install script in root
    install_scripts = ["install", "install.py", "build.sh", "build.py"]
    for script in install_scripts:
        if (repo_path / script).exists():
            found_methods.append(f"{script} (Build/Install script)")
            print(f"[*] ✓ Found {script}")
            break
    
    if not found_methods:
        print(f"[!] No known installation method found")
        print(f"[*] Available files in directory:")
        try:
            for item in sorted(repo_path.iterdir()):
                item_type = "DIR" if item.is_dir() else "FILE"
                print(f"    [{item_type}] {item.name}")
        except:
            pass
        return False
    
    print(f"\n[*] Found {len(found_methods)} installation method(s):")
    for method in found_methods:
        print(f"    - {method}")
    print()
    
    # Try installation methods in order
    # Check for requirements.txt first (dependencies)
    if (repo_path / "requirements.txt").exists():
        print(f"[*] Installing Python dependencies first...")
        run_command(
            ["pip3", "install", "-r", "requirements.txt"],
            "Installing Python requirements",
            cwd=str(repo_path)
        )
    
    # Check for setup.py (Python package)
    if (repo_path / "setup.py").exists():
        print(f"[*] Attempting installation via setup.py...")
        success = run_command(
            ["python3", "setup.py", "install"],
            f"Installing Python package from setup.py",
            cwd=str(repo_path)
        )
        if success:
            return True
    
    # Check for Makefile
    if (repo_path / "Makefile").exists():
        print(f"[*] Attempting installation via Makefile...")
        if run_command(["make"], "Building with make", cwd=str(repo_path)):
            success = run_command(
                ["sudo", "make", "install"],
                "Installing with make install",
                cwd=str(repo_path)
            )
            if success:
                return True
    
    # Check for CMakeLists.txt
    if (repo_path / "CMakeLists.txt").exists():
        print(f"[*] Attempting installation via CMake...")
        build_dir = repo_path / "build"
        build_dir.mkdir(exist_ok=True)
        if run_command(["cmake", ".."], "Configuring with CMake", cwd=str(build_dir)):
            if run_command(["make"], "Building with make", cwd=str(build_dir)):
                success = run_command(
                    ["sudo", "make", "install"],
                    "Installing with make install",
                    cwd=str(build_dir)
                )
                if success:
                    return True
    
    # Check for install.sh
    if (repo_path / "install.sh").exists():
        print(f"[*] Attempting installation via install.sh...")
        run_command(["chmod", "+x", "install.sh"], "Making install.sh executable", cwd=str(repo_path))
        success = run_command(
            ["bash", "install.sh"],
            "Running install.sh",
            cwd=str(repo_path)
        )
        if success:
            return True
    
    # Check for install script in root
    install_scripts = ["install", "install.py", "build.sh", "build.py"]
    for script in install_scripts:
        script_path = repo_path / script
        if script_path.exists():
            print(f"[*] Attempting installation via {script}...")
            if script.endswith('.sh'):
                run_command(["chmod", "+x", script], f"Making {script} executable", cwd=str(repo_path))
                success = run_command(["bash", script], f"Running {script}", cwd=str(repo_path))
            elif script.endswith('.py'):
                success = run_command(["python3", script], f"Running {script}", cwd=str(repo_path))
            if success:
                return True
            break
    
    return success


def print_header():
    """Print program header."""
    print("\n" + "="*60)
    print(" "*15 + "Fast Command Prompt")
    print(" "*10 + "System Management Tool")
    print("="*60)
    print(f"[*] Python version: {sys.version.split()[0]}")
    print(f"[*] Working directory: {os.getcwd()}")
    print(f"[*] User: {os.getenv('USER', 'Unknown')}")
    print("="*60 + "\n")


def print_summary(success, operations_count):
    """Print operation summary."""
    print("\n" + "="*60)
    print(" "*20 + "OPERATION SUMMARY")
    print("="*60)
    print(f"[*] Total operations: {operations_count}")
    if success:
        print(f"[+] Status: All operations completed successfully")
        print(f"[+] Result: SUCCESS")
    else:
        print(f"[!] Status: Some operations failed")
        print(f"[!] Result: FAILED")
    print("="*60 + "\n")


def main():
    print_header()
    
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
    
    # Count operations
    operations_count = sum(1 for v in vars(args).values() if v)
    
    print(f"[*] Starting {operations_count} operation(s)...\n")
    
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
        print(f"\n{'#'*60}")
        print(f"[*] Auto-Install Mode")
        print(f"[*] Packages to install: {packages}")
        print(f"[*] Steps: Update → Install")
        print(f"{'#'*60}\n")
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
        print(f"\n{'#'*60}")
        print(f"[*] GitHub Clone Mode")
        print(f"[*] Repositories will be saved to: {repos_dir.absolute()}")
        print(f"{'#'*60}\n")
        
        for repo_url in args.github:
            repo_name = extract_repo_name(repo_url)
            repo_path = repos_dir / repo_name
            
            print(f"\n{'#'*60}")
            print(f"[*] Processing repository: {repo_name}")
            print(f"[*] URL: {repo_url}")
            print(f"[*] Target path: {repo_path.absolute()}")
            print(f"{'#'*60}\n")
            
            if repo_path.exists():
                print(f"[!] Repository '{repo_name}' already exists at: {repo_path.absolute()}")
                print(f"[!] Skipping clone.")
                print(f"[*] Use --github-install to update and install, or remove the directory")
                continue
            
            success &= run_command(
                ["git", "clone", "--progress", repo_url, str(repo_path)],
                f"Cloning repository: {repo_name} from {repo_url}"
            )
            if repo_path.exists():
                print(f"\n{'='*60}")
                print(f"[+] Repository successfully cloned!")
                print(f"[+] Location: {repo_path.absolute()}")
                print(f"[+] Size: {get_dir_size(repo_path)}")
                print(f"{'='*60}\n")
    
    if args.github_install:
        # Create repos directory if it doesn't exist
        repos_dir = Path(args.github_dir)
        repos_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n{'#'*60}")
        print(f"[*] GitHub Clone & Install Mode")
        print(f"[*] Repositories will be saved to: {repos_dir.absolute()}")
        print(f"{'#'*60}\n")
        
        for repo_url in args.github_install:
            repo_name = extract_repo_name(repo_url)
            repo_path = repos_dir / repo_name
            
            print(f"\n{'#'*60}")
            print(f"[*] Processing repository: {repo_name}")
            print(f"[*] URL: {repo_url}")
            print(f"[*] Target path: {repo_path.absolute()}")
            print(f"{'#'*60}\n")
            
            # Clone or update repository
            if repo_path.exists():
                print(f"[*] Repository '{repo_name}' already exists")
                print(f"[*] Checking for updates...")
                print(f"[*] Current size: {get_dir_size(repo_path)}")
                success &= run_command(
                    ["git", "pull", "--progress"],
                    f"Updating repository: {repo_name}",
                    cwd=str(repo_path)
                )
            else:
                success &= run_command(
                    ["git", "clone", "--progress", repo_url, str(repo_path)],
                    f"Cloning repository: {repo_name} from {repo_url}"
                )
                if repo_path.exists():
                    print(f"[+] Repository cloned! Size: {get_dir_size(repo_path)}")
            
            # Try to install from source
            if repo_path.exists():
                print(f"\n{'#'*60}")
                print(f"[*] Attempting to auto-install: {repo_name}")
                print(f"[*] Scanning for installation methods...")
                print(f"{'#'*60}\n")
                install_success = install_from_source(repo_path)
                if install_success:
                    print(f"\n{'='*60}")
                    print(f"[+] Successfully installed {repo_name}!")
                    print(f"{'='*60}\n")
                else:
                    print(f"\n{'='*60}")
                    print(f"[!] Could not auto-install {repo_name}")
                    print(f"[*] Repository location: {repo_path.absolute()}")
                    print(f"[*] Please check the repository README for manual installation")
                    print(f"{'='*60}\n")
    
    if args.download:
        # Create downloads directory if it doesn't exist
        downloads_dir = Path(args.download_dir)
        downloads_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n{'#'*60}")
        print(f"[*] Download Mode")
        print(f"[*] Files will be saved to: {downloads_dir.absolute()}")
        print(f"{'#'*60}\n")
        
        for url in args.download:
            filename = os.path.basename(urllib.parse.urlparse(url).path)
            if not filename:
                filename = "downloaded_file"
            file_path = downloads_dir / filename
            
            print(f"\n{'#'*60}")
            print(f"[*] Downloading file")
            print(f"[*] URL: {url}")
            print(f"[*] Filename: {filename}")
            print(f"[*] Target: {file_path.absolute()}")
            print(f"{'#'*60}\n")
            
            # Try wget first, then curl
            if shutil.which("wget"):
                success &= run_command(
                    ["wget", "--progress=bar:force", "-O", str(file_path), url],
                    f"Downloading {filename} from {url}"
                )
            elif shutil.which("curl"):
                success &= run_command(
                    ["curl", "-L", "--progress-bar", "-o", str(file_path), url],
                    f"Downloading {filename} from {url}"
                )
            else:
                print(f"\n{'='*60}")
                print(f"[!] Error: Neither wget nor curl is available")
                print(f"[*] Please install one: sudo apt install wget curl")
                print(f"{'='*60}\n")
                success = False
            
            if file_path.exists():
                file_size = os.path.getsize(file_path)
                size_str = f"{file_size / 1024:.2f} KB" if file_size < 1024*1024 else f"{file_size / (1024*1024):.2f} MB"
                print(f"\n{'='*60}")
                print(f"[+] File successfully downloaded!")
                print(f"[+] Location: {file_path.absolute()}")
                print(f"[+] Size: {size_str}")
                print(f"{'='*60}\n")
                
                # If it's a script, make it executable
                if filename.endswith(('.sh', '.py')):
                    print(f"[*] Detected script file, making executable...")
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
    
    # Print summary
    print_summary(success, operations_count)
    
    if success:
        print("[+] All tasks completed successfully.")
    else:
        print("[!] Some tasks failed. Please check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()