#!/bin/bash
# Script to create the PDF file for WSTG
echo "Creating PDF for version $1"
# Clean the build folder
rm -rf build

# Create the required build folders
mkdir -p build/md
mkdir -p build/images

# Copy files to build directory
find document -name "*.md" | while IFS= read -r FILE; do cp -v "$FILE" build/md/"${FILE//\//_}"; done
find document -name "images"  -exec cp -r {}/. build/images/. ";"

# Rename some files to keep the correct order
find build/md -name "*README.md" | while IFS= read -r FILE; do mv -v "$FILE" "${FILE//README/0-0.0_README}"; done

# Update version in pdf-config
sed -i "s/{PDF Version}/$1/g" pdf-config.json

# Creating the cover page
echo "<body class=\"cover-page\"><div class=\"cover-page\"></div><h1>OWASP Testing Guide </h1>
<h2>Version: $1</h2></body>" > build/wstg-$1.md

ls -al build/images
# Create the final single markdown file.
ls build/md | sort -n | while read x; do cat build/md/$x | sed -e 's/^# /<div style=\"page-break-after: always\;\"><\/div>\
\
# /' | sed 's/\[\([^\n]\+\)\]([^\n]\+.md#\([^\)]\+\)/[\1](#\2/' | sed 's/\(^#\{1\} \)\(\[\([0-9. ]*\)\(.*\)\]\(.*\)\(\?\:\n\+\|$\)\)/<h1><a href=\"#\4\">\4<\/a><\/h1>/'  | sed 's/\(^#\{2\} \)\(\[\([0-9. ]*\)\(.*\)\]\(.*\)\(\?\:\n\+\|$\)\)/<h2><a href=\"#\4\">\4<\/a><\/h2>/' | sed 's/\(^#\{3\} \)\(\[\([0-9. ]*\)\(.*\)\]\(.*\)\(\?\:\n\+\|$\)\)/<h3><a href=\"#\4\">\4<\/a><\/h3>/'| sed 's/\(^#\{4\} \)\(\[\([0-9. ]*\)\(.*\)\]\(.*\)\(\?\:\n\+\|$\)\)/<h4><a href=\"#\4\">\4<\/a><\/h4>/' | sed 's/\(^#\{5\} \)\(\[\([0-9. ]*\)\(.*\)\]\(.*\)\(\?\:\n\+\|$\)\)/<h5><a href=\"#\4\">\4<\/a><\/h5>/' | sed 's/\(^#\{1\} \) *\([^\n]\+\?\))*\(\?\:\n\+\|$\)/<h1 id=\"\2\">\2<\/h1>/' | sed 's/\(^#\{2\} \) *\([^\n]\+\?\))*\(\?\:\n\+\|$\)/<h2 id=\"\2\">\2<\/h2>/' | sed 's/\(^#\{3\} \) *\([^\n]\+\?\))*\(\?\:\n\+\|$\)/<h3 id=\"\2\">\2<\/h3>/' | sed 's/\(^#\{4\} \) *\([^\n]\+\?\))*\(\?\:\n\+\|$\)/<h4 id=\"\2\">\2<\/h4>/' | sed 's/\(^#\{5\} \) *\([^\n]\+\?\))*\(\?\:\n\+\|$\)/<h5 id=\"\2\">\2<\/h5>/' | sed 's/\(\[\([0-9. ]*\)\(.*\)\]([0-9_.\/\-]*\(.*\).md)\(\?\:\n\+\|$\)\)/\2 <a href=\"#\3\">\3<\/a>/' | python -c "import re; import sys; print(re.sub(r'id=\"([^\n]+)\"', lambda m: m.group().replace(' ', '-'), sys.stdin.read()))"  | python -c "import re; import sys; print(re.sub(r'href=\"([^\n]+)\"', lambda m: m.group().replace(' ', '-'), sys.stdin.read()))" | sed 's/<h1 id=\"[0-9.]*-\(.*\)\">\(.*\)<\/h1>/<h1 id="\1">\2<\/h1>/'  >> build/wstg-$1.md; done

# Convert the markdown to PDF
md-to-pdf  --config-file pdf-config.json build/wstg-$1.md
