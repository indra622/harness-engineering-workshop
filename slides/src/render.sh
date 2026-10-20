#!/bin/sh
# Render a PPTX to PDF and PNG pages with headless LibreOffice and pdftoppm.
#
# Usage (from the project root):
#   sh slides/src/render.sh slides/previews/representative-v01.pptx
#
# Writes <name>.pdf next to the PPTX and <name>/page-N.png (one per slide).
# LibreOffice runs with a throwaway profile so it never touches a desktop
# session. Set LO_PROFILE_DIR to choose where that profile lives.
#
# Some LibreOffice builds read fonts through their own fontconfig and do not
# see Nanum Gothic when it lives in a system asset folder. Unless
# FONTCONFIG_FILE is already set, this script writes a small fontconfig file
# inside the throwaway profile that adds the folder fc-match reports for
# Nanum Gothic. Nothing outside the profile folder is changed.
set -eu

PPTX="$1"
DIR=$(dirname "$PPTX")
NAME=$(basename "$PPTX" .pptx)
PROFILE="${LO_PROFILE_DIR:-$(mktemp -d)}"
DPI="${RENDER_DPI:-110}"

if [ -z "${FONTCONFIG_FILE:-}" ]; then
  FONT_FILE=$(fc-match "Nanum Gothic" --format='%{file}')
  FONT_DIR=$(dirname "$FONT_FILE")
  mkdir -p "$PROFILE/fc-cache"
  cat > "$PROFILE/fonts.conf" <<EOF
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <dir>$FONT_DIR</dir>
  <dir>/System/Library/Fonts</dir>
  <dir>/Library/Fonts</dir>
  <dir prefix="xdg">fonts</dir>
  <cachedir>$PROFILE/fc-cache</cachedir>
</fontconfig>
EOF
  FONTCONFIG_FILE="$PROFILE/fonts.conf"
  export FONTCONFIG_FILE
fi

soffice -env:UserInstallation="file://$PROFILE" --headless --norestore \
  --convert-to pdf --outdir "$DIR" "$PPTX"

mkdir -p "$DIR/$NAME"
rm -f "$DIR/$NAME"/page-*.png
pdftoppm -r "$DPI" -png "$DIR/$NAME.pdf" "$DIR/$NAME/page"
ls "$DIR/$NAME"
