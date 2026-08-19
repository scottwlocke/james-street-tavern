#!/usr/bin/env bash
#
# Install PowerShell + Starship + FiraCode Nerd Font + Catppuccin Powerline theme
# Works on most modern Linux distributions
#

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

info()  { echo -e "${GREEN}[INFO]${NC}  $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*"; exit 1; }
step()  { echo -e "\n${CYAN}==>${NC} $*"; }

# ---------------------------------------------------------------------------
# Prerequisites
# ---------------------------------------------------------------------------
step "Checking prerequisites..."

for cmd in curl tar; do
    command -v "$cmd" >/dev/null 2>&1 || error "'$cmd' is required but not installed."
done

# Install unzip + fontconfig if missing (best-effort)
if ! command -v unzip >/dev/null 2>&1 || ! command -v fc-cache >/dev/null 2>&1; then
    info "Installing unzip and/or fontconfig..."
    if command -v apt-get >/dev/null 2>&1; then
        sudo apt-get update -qq
        sudo apt-get install -y -qq unzip fontconfig
    elif command -v dnf >/dev/null 2>&1; then
        sudo dnf install -y -q unzip fontconfig
    elif command -v yum >/dev/null 2>&1; then
        sudo yum install -y -q unzip fontconfig
    elif command -v pacman >/dev/null 2>&1; then
        sudo pacman -Sy --noconfirm unzip fontconfig
    elif command -v zypper >/dev/null 2>&1; then
        sudo zypper install -y unzip fontconfig
    else
        warn "Could not install unzip/fontconfig/chsh automatically. Please install them manually."
    fi
fi


# ---------------------------------------------------------------------------
# 1. Detect architecture & distro
# ---------------------------------------------------------------------------
step "Detecting system..."

ARCH=$(uname -m)
case "$ARCH" in
    x86_64)        PS_ARCH="x64"   ;;
    aarch64|arm64) PS_ARCH="arm64" ;;
    armv7l|armhf)  PS_ARCH="arm32" ;;
    *) error "Unsupported architecture: $ARCH" ;;
esac
info "Architecture: $ARCH → PowerShell package: linux-$PS_ARCH"

if [ -f /etc/os-release ]; then
    # shellcheck source=/dev/null
    . /etc/os-release
    DISTRO_NAME="${PRETTY_NAME:-$ID $VERSION_ID}"
else
    DISTRO_NAME="Unknown Linux"
fi
info "Linux: $DISTRO_NAME"

# ---------------------------------------------------------------------------
# 2. Install PowerShell from GitHub
# ---------------------------------------------------------------------------
step "Installing PowerShell from GitHub..."

LATEST_TAG=$(curl -fsSL --progress-bar https://api.github.com/repos/PowerShell/PowerShell/releases/latest \
    | grep -oP '"tag_name":\s*"\K[^"]+' || true)

[ -z "$LATEST_TAG" ] && error "Could not determine latest PowerShell version."

VERSION="${LATEST_TAG#v}"
info "Latest PowerShell version: $VERSION"

PACKAGE="powershell-${VERSION}-linux-${PS_ARCH}.tar.gz"
DOWNLOAD_URL="https://github.com/PowerShell/PowerShell/releases/download/${LATEST_TAG}/${PACKAGE}"
TMP_FILE="/tmp/${PACKAGE}"

info "Downloading $PACKAGE ..."
curl -fL --no-progress-bar -o "$TMP_FILE" "$DOWNLOAD_URL" \
    || error "Download failed: $DOWNLOAD_URL"

INSTALL_DIR="/opt/microsoft/powershell/7"
info "Extracting to $INSTALL_DIR ..."
sudo mkdir -p "$INSTALL_DIR"
sudo tar -zxf "$TMP_FILE" -C "$INSTALL_DIR"
sudo chmod +x "$INSTALL_DIR/pwsh"

# Symlink
sudo rm -f /usr/bin/pwsh
sudo ln -s "$INSTALL_DIR/pwsh" /usr/bin/pwsh
rm -f "$TMP_FILE"


info "PowerShell $VERSION installed successfully."

# ---------------------------------------------------------------------------
# 3. Install Starship
# ---------------------------------------------------------------------------
step "Installing Starship..."

# Non-interactive install to /usr/local/bin
curl -sS https://starship.rs/install.sh | sh -s -- -y >/dev/null 2>&1

if ! command -v starship >/dev/null 2>&1; then
    error "Starship installation failed."
fi
info "Starship $(starship --version | head -1) installed."

# ---------------------------------------------------------------------------
# 4. Install FiraCode Nerd Font
# ---------------------------------------------------------------------------
step "Installing FiraCode Nerd Font..."

FONTS_DIR="${HOME}/.local/share/fonts"
mkdir -p "$FONTS_DIR"

FONT_ZIP="/tmp/FiraCodeNerdFont.zip"
info "Downloading FiraCode Nerd Font..."
curl -fL --no-progress-bar \
    -o "$FONT_ZIP" \
    "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/FiraCode.zip" \
    || error "Failed to download FiraCode Nerd Font."

info "Extracting fonts to $FONTS_DIR ..."
unzip -o -q "$FONT_ZIP" -d "$FONTS_DIR"
rm -f "$FONT_ZIP"

# Remove Windows Compatible variants (optional cleanup)
find "$FONTS_DIR" -iname '*Windows Compatible*' -delete 2>/dev/null || true

info "Refreshing font cache..."
fc-cache -f >/dev/null 2>&1 || warn "fc-cache failed (font may still work after restart)."

info "FiraCode Nerd Font installed."

# ---------------------------------------------------------------------------
# 5. Configure Starship with Catppuccin Powerline theme
# ---------------------------------------------------------------------------
step "Configuring Starship with Catppuccin Powerline theme..."

mkdir -p "${HOME}/.config"
starship preset catppuccin-powerline --force -o "${HOME}/.config/starship.toml"
info "Catppuccin Powerline theme applied → ~/.config/starship.toml"

# ---------------------------------------------------------------------------
# 6. Shell integration
# ---------------------------------------------------------------------------
step "Adding Starship to shell configs..."

# Bash
if [ -f "${HOME}/.bashrc" ]; then
    if ! grep -q 'starship init bash' "${HOME}/.bashrc"; then
        echo '' >> "${HOME}/.bashrc"
        echo '# Starship prompt' >> "${HOME}/.bashrc"
        echo 'eval "$(starship init bash)"' >> "${HOME}/.bashrc"
        info "Added Starship init to ~/.bashrc"
    else
        info "Starship already configured in ~/.bashrc"
    fi
fi

# Zsh
if [ -f "${HOME}/.zshrc" ]; then
    if ! grep -q 'starship init zsh' "${HOME}/.zshrc"; then
        echo '' >> "${HOME}/.zshrc"
        echo '# Starship prompt' >> "${HOME}/.zshrc"
        echo 'eval "$(starship init zsh)"' >> "${HOME}/.zshrc"
        info "Added Starship init to ~/.zshrc"
    else
        info "Starship already configured in ~/.zshrc"
    fi
fi

# PowerShell profile (Linux location)
PWSH_PROFILE_DIR="${HOME}/.config/powershell"
PWSH_PROFILE="${PWSH_PROFILE_DIR}/Microsoft.PowerShell_profile.ps1"
mkdir -p "$PWSH_PROFILE_DIR"

if [ ! -f "$PWSH_PROFILE" ] || ! grep -q 'starship init powershell' "$PWSH_PROFILE" 2>/dev/null; then
    cat >> "$PWSH_PROFILE" << 'EOF'

# Starship prompt
if (Get-Command starship -ErrorAction SilentlyContinue) {
    Invoke-Expression (&starship init powershell)
}
EOF
    info "Added Starship init to PowerShell profile"
else
    info "Starship already configured in PowerShell profile"
fi

# Set as Default Shell
sudo chsh vscode -s $(which pwsh)

# ---------------------------------------------------------------------------
# Done
# ---------------------------------------------------------------------------
echo
info "=============================================="
info " Installation complete!"
info "=============================================="
echo
echo -e "  ${GREEN}•${NC} PowerShell   →  $(pwsh -NoLogo -Command '\$PSVersionTable.PSVersion' 2>/dev/null || echo 'installed')"
echo -e "  ${GREEN}•${NC} Starship     →  $(starship --version 2>/dev/null | head -1)"
echo -e "  ${GREEN}•${NC} Font         →  FiraCode Nerd Font"
echo -e "  ${GREEN}•${NC} Theme        →  Catppuccin Powerline (Mocha)"
echo
warn "IMPORTANT: Set your terminal font to 'FiraCode Nerd Font' (or 'FiraCode Nerd Font Mono')"
warn "           for the icons and powerline glyphs to render correctly."
echo
info "Restart your terminal or run:  source ~/.bashrc   (or ~/.zshrc)"
info "Then start PowerShell with:    pwsh"
echo