# 🚀 Fast Command Prompt - Short Version

<div dir="rtl">

## 📋 نظرة عامة

**Fast Command Prompt** هو أداة سطر أوامر قوية ومتعددة الاستخدامات لإدارة النظام وتثبيت الحزم والأدوات من مصادر مختلفة. تم تصميمها لتسهيل إدارة النظام وتثبيت التطبيقات بطريقة سريعة وآمنة.

### ✨ الميزات الرئيسية

- 🔄 إدارة حزم APT (تحديث، ترقية، تثبيت، إزالة)
- 📦 دعم تثبيت من مصادر متعددة (deb, snap, flatpak, pip)
- 🐙 تحميل وتثبيت تلقائي من GitHub
- 📥 تحميل ملفات من أي موقع
- 🔧 تثبيت تلقائي من الكود المصدري
- 🛡️ تنفيذ آمن للأوامر مع معالجة الأخطاء
- ⚡ أوامر مختصرة وسهلة الاستخدام

</div>

---

## 📖 Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [APT Package Management](#apt-package-management)
  - [Package Installation Methods](#package-installation-methods)
  - [GitHub Integration](#github-integration)
  - [File Downloads](#file-downloads)
  - [Source Code Installation](#source-code-installation)
  - [System Operations](#system-operations)
- [Examples](#examples)
- [Advanced Usage](#advanced-usage)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

### 🔧 System Management
- Update package lists
- Upgrade system packages
- Install/remove packages
- Auto-remove unnecessary packages
- Auto-clean package cache
- System shutdown

### 📦 Multiple Installation Methods
- **APT**: Standard Debian/Ubuntu packages
- **DEB**: Direct .deb file installation
- **Snap**: Snap package installation
- **Flatpak**: Flatpak package installation
- **Pip**: Python package installation
- **Source Code**: Automatic installation from source

### 🐙 GitHub Integration
- Clone repositories from GitHub
- Auto-install from GitHub repositories
- Automatic update detection
- Support for multiple repositories

### 📥 File Downloads
- Download files from any URL
- Automatic executable permissions for scripts
- Support for wget and curl

### 🔍 Smart Source Installation
Automatically detects and installs from:
- `setup.py` (Python packages)
- `requirements.txt` (Python dependencies)
- `Makefile` (make install)
- `CMakeLists.txt` (CMake build)
- `install.sh` / `install.py`
- Custom build scripts

---

## 📋 Requirements

- **Python**: 3.6 or higher
- **Operating System**: Linux (Debian/Ubuntu based)
- **Dependencies**:
  - `git` (for GitHub cloning)
  - `wget` or `curl` (for file downloads)
  - `apt` (for package management)
  - `sudo` (for system operations)

### Optional Dependencies
- `snapd` (for snap packages)
- `flatpak` (for flatpak packages)
- `pip3` (for Python packages)
- `make` (for Makefile builds)
- `cmake` (for CMake builds)

---

## 🚀 Installation

### Method 1: Direct Usage
```bash
# Clone or download the script
git clone <repository-url>
cd Fast-command-prompt-Short-version

# Make it executable
chmod +x Fast-command-prompt-Short-version.py

# Run directly
python3 Fast-command-prompt-Short-version.py --help
```

### Method 2: System-wide Installation
```bash
# Copy to /usr/local/bin
sudo cp Fast-command-prompt-Short-version.py /usr/local/bin/fcp

# Make executable
sudo chmod +x /usr/local/bin/fcp

# Now you can use it from anywhere
fcp --help
```

---

## 📚 Usage

### APT Package Management

#### Update Package List
```bash
python3 Fast-command-prompt-Short-version.py --update
# or short form
python3 Fast-command-prompt-Short-version.py -ud
```

#### Upgrade System Packages
```bash
python3 Fast-command-prompt-Short-version.py --upgrade
# or short form
python3 Fast-command-prompt-Short-version.py -ug
```

#### Install Packages
```bash
# Install single package
python3 Fast-command-prompt-Short-version.py --install nginx

# Install multiple packages
python3 Fast-command-prompt-Short-version.py -i nginx python3-pip git

# Auto-install (update first, then install)
python3 Fast-command-prompt-Short-version.py --auto-install nginx
```

#### Remove Packages
```bash
python3 Fast-command-prompt-Short-version.py --remove package-name
python3 Fast-command-prompt-Short-version.py -r package1 package2
```

#### Auto-remove Unnecessary Packages
```bash
python3 Fast-command-prompt-Short-version.py --autoremove
python3 Fast-command-prompt-Short-version.py -ar
```

#### Auto-clean Package Cache
```bash
python3 Fast-command-prompt-Short-version.py --autoclean
python3 Fast-command-prompt-Short-version.py -ac
```

---

### Package Installation Methods

#### Install .deb Package
```bash
python3 Fast-command-prompt-Short-version.py --install-deb package.deb
python3 Fast-command-prompt-Short-version.py -deb file1.deb file2.deb
```

#### Install Snap Package
```bash
python3 Fast-command-prompt-Short-version.py --install-snap code
python3 Fast-command-prompt-Short-version.py -snap code discord
```

#### Install Flatpak Package
```bash
python3 Fast-command-prompt-Short-version.py --install-flatpak com.example.app
python3 Fast-command-prompt-Short-version.py -flatpak app1 app2
```

#### Install Python Package (Pip)
```bash
python3 Fast-command-prompt-Short-version.py --install-pip requests
python3 Fast-command-prompt-Short-version.py -pip requests flask numpy
```

---

### GitHub Integration

#### Clone Repository from GitHub
```bash
# Clone single repository
python3 Fast-command-prompt-Short-version.py --github https://github.com/user/repo

# Clone multiple repositories
python3 Fast-command-prompt-Short-version.py -gh https://github.com/user/repo1 https://github.com/user/repo2

# Custom directory
python3 Fast-command-prompt-Short-version.py --github-dir ~/my-repos --github https://github.com/user/repo
```

#### Clone and Auto-Install from GitHub
```bash
# Clone and automatically try to install
python3 Fast-command-prompt-Short-version.py --github-install https://github.com/user/repo

# If repository exists, it will update first
python3 Fast-command-prompt-Short-version.py -gh-install https://github.com/user/repo
```

**How it works:**
1. Clones the repository (or updates if exists)
2. Automatically detects installation method:
   - `setup.py` → `python3 setup.py install`
   - `requirements.txt` → `pip3 install -r requirements.txt`
   - `Makefile` → `make && sudo make install`
   - `CMakeLists.txt` → `cmake .. && make && sudo make install`
   - `install.sh` → `bash install.sh`
   - Other install scripts

---

### File Downloads

#### Download Files from URL
```bash
# Download single file
python3 Fast-command-prompt-Short-version.py --download https://example.com/file.sh

# Download multiple files
python3 Fast-command-prompt-Short-version.py -dl https://site.com/file1.sh https://site.com/file2.py

# Custom download directory
python3 Fast-command-prompt-Short-version.py --download-dir ~/Downloads --download https://example.com/file.sh
```

**Features:**
- Automatically makes `.sh` and `.py` files executable
- Uses `wget` or `curl` (whichever is available)
- Saves to `./downloads` by default

---

### Source Code Installation

#### Install from Local Source Directory
```bash
python3 Fast-command-prompt-Short-version.py --install-source ./my-project
python3 Fast-command-prompt-Short-version.py -src /path/to/project
```

The tool will automatically detect and use the appropriate installation method.

---

### System Operations

#### Make Files Executable
```bash
python3 Fast-command-prompt-Short-version.py --chmod script.sh
python3 Fast-command-prompt-Short-version.py -ch file1.sh file2.py
```

#### Shutdown System
```bash
python3 Fast-command-prompt-Short-version.py --shutdown
python3 Fast-command-prompt-Short-version.py -sh
```

---

## 💡 Examples

### Example 1: Complete System Update
```bash
python3 Fast-command-prompt-Short-version.py -ud -ug -ar -ac
```
This will:
1. Update package list
2. Upgrade all packages
3. Auto-remove unnecessary packages
4. Auto-clean cache

### Example 2: Install Development Tools
```bash
python3 Fast-command-prompt-Short-version.py --auto-install git python3-pip build-essential
```

### Example 3: Install Tool from GitHub
```bash
python3 Fast-command-prompt-Short-version.py --github-install https://github.com/user/awesome-tool
```

### Example 4: Download and Install Script
```bash
# Download installation script
python3 Fast-command-prompt-Short-version.py --download https://example.com/install.sh

# The script is automatically made executable
# Now you can run it
./downloads/install.sh
```

### Example 5: Install Multiple Package Types
```bash
python3 Fast-command-prompt-Short-version.py \
  --install nginx \
  --install-snap code \
  --install-pip requests flask \
  --github-install https://github.com/user/tool
```

### Example 6: Custom Directories
```bash
python3 Fast-command-prompt-Short-version.py \
  --github-dir ~/Projects \
  --download-dir ~/Downloads \
  --github https://github.com/user/repo \
  --download https://example.com/file.sh
```

---

## 🔧 Advanced Usage

### Combining Multiple Operations
You can combine multiple operations in a single command:

```bash
python3 Fast-command-prompt-Short-version.py \
  --update \
  --auto-install nginx python3-pip \
  --github-install https://github.com/user/tool \
  --autoremove \
  --autoclean
```

### Using Short Options
All options have short forms for faster typing:

```bash
# Short forms
-ud  → --update
-ug  → --upgrade
-i   → --install
-r   → --remove
-sh  → --shutdown
-ar  → --autoremove
-ac  → --autoclean
-ch  → --chmod
-gh  → --github
-dl  → --download
-src → --install-source
```

### Error Handling
The tool provides detailed error messages and continues with other operations even if one fails:

```bash
python3 Fast-command-prompt-Short-version.py \
  --install nonexistent-package \
  --install git
# First will fail, second will succeed
```

---

## 🐛 Troubleshooting

### Issue: "Command not found" errors

**Solution:** Ensure required tools are installed:
```bash
sudo apt update
sudo apt install git wget curl
```

### Issue: Permission denied errors

**Solution:** Some operations require sudo. The tool will prompt when needed, or run with sudo:
```bash
sudo python3 Fast-command-prompt-Short-version.py --upgrade
```

### Issue: GitHub clone fails

**Possible causes:**
- Git not installed: `sudo apt install git`
- Network issues: Check internet connection
- Repository doesn't exist: Verify the URL

### Issue: Auto-installation fails

**Solution:** The tool tries multiple methods. If all fail:
1. Check the repository's README for manual installation
2. The repository is cloned to `./repos/` (or custom directory)
3. Install manually from the cloned directory

### Issue: Download fails

**Possible causes:**
- Neither wget nor curl installed: `sudo apt install wget curl`
- Invalid URL: Verify the URL is correct
- Network issues: Check internet connection

---

## 📝 Command Reference

### Quick Reference Table

| Option | Short | Description |
|--------|-------|-------------|
| `--update` | `-ud` | Update package list |
| `--upgrade` | `-ug` | Upgrade system packages |
| `--install` | `-i` | Install package(s) |
| `--remove` | `-r` | Remove package(s) |
| `--auto-install` | `-auto` | Update then install |
| `--autoremove` | `-ar` | Auto-remove packages |
| `--autoclean` | `-ac` | Auto-clean cache |
| `--chmod` | `-ch` | Make file(s) executable |
| `--install-deb` | `-deb` | Install .deb file(s) |
| `--install-snap` | `-snap` | Install snap package(s) |
| `--install-flatpak` | `-flatpak` | Install flatpak package(s) |
| `--install-pip` | `-pip` | Install Python package(s) |
| `--github` | `-gh` | Clone GitHub repository |
| `--github-install` | `-gh-install` | Clone and install from GitHub |
| `--download` | `-dl` | Download file(s) from URL |
| `--install-source` | `-src` | Install from source directory |
| `--shutdown` | `-sh` | Shutdown system |
| `--github-dir` | `-gh-dir` | Custom GitHub repos directory |
| `--download-dir` | `-dl-dir` | Custom downloads directory |

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### How to Contribute
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- Built with Python 3
- Uses standard Linux tools (apt, git, wget, curl)
- Inspired by the need for faster system management

---

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review the examples in this README
3. Open an issue on GitHub

---

## 🔄 Version History

- **v1.0.0**: Initial release with basic APT management
- **v2.0.0**: Added GitHub integration and source installation
- **v2.1.0**: Added file downloads and multiple package managers

---

<div dir="rtl">

## 📌 ملاحظات مهمة

- ⚠️ بعض الأوامر تتطلب صلاحيات `sudo`
- 🔒 الأداة تستخدم تنفيذ آمن للأوامر (بدون `shell=True`)
- 📁 الملفات المحمولة تُحفظ في `./downloads` افتراضياً
- 🐙 المستودعات المحملة تُحفظ في `./repos` افتراضياً
- ✅ الأداة توفر رسائل واضحة عن نجاح أو فشل كل عملية

</div>

---

**Made with ❤️ for faster system management**
