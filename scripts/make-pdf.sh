#!/bin/bash
# Script to create the PDF file for WSTG
echo "Creating PDF for version $1"
# Clean the build folder
rm -rf build

# Create the required build folders
mkdir -p build/md
mkdir -p build/images

# Copy files to build directory
cd document
find . -name "*.md"  -exec cp {} ../build/md ";"
find . -name "images"  -exec cp -r {}/. ../build/images/. ";"

# Rename some files to keep the correct order
cd ../build/md
find . -name 'Appx.*.md' -exec bash -c ' mv $0 ${0/Appx/6_Appx}' {} \;
mv OWASP_Testing_Guide_v4_Table_of_Contents.md 0_A_OWASP_Testing_Guide_v4_Table_of_Contents.md

# Update version in pdf-config
sed -i "s/{PDF Version}/$1/g" ../../pdf-config.json

# Creating the cover page
echo "<body class=\"cover-page\"><div class=\"cover-page\"></div><h1>OWASP Testing Guide </h1>
<h2>Version: $1</h2></body>" > ../wstg-$1.md
# Create the final single markdown file.
ls | sort -n | while read x; do cat $x | sed -e 's/^# /<div style=\"page-break-after: always\;\"><\/div>\
\
# /'  >> ../wstg-$1.md; done

# Convert the markdown to PDF
md-to-pdf  --config-file ../../pdf-config.json ../wstg-$1.md