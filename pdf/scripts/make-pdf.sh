#!/bin/bash
# Script to create the PDF file for WSTG
VERSION=$1
echo "Creating PDF for version $VERSION"

# Clean the build folder
rm -rf build

# Create the required build folders
mkdir -p build/md
mkdir -p build/pdf
mkdir -p build/images

# Copy Markdown and Image files to build directory
# Replace path separators "/" with ">>>" in .md files for better splitting in later stages
find document -name "*.md" | while IFS= read -r FILE; do cp -v "$FILE" build/md/"${FILE//\//>>>}"; done
find document -name "images"  -exec cp -r {}/. build/images/. ";"
cp pdf/assets/cover.jpg build/images/book-cover.jpg
cp pdf/assets/back-cover.png build/images/back-cover.png
cp pdf/assets/second-cover.png build/images/second-cover.png

# Rename README files by prepending "0-0.0_" to keep them in the correct order
find build/md -name "*README.md" | while IFS= read -r FILE; do mv -v "$FILE" "${FILE//README/0-0.0_README}"; done

# Update build version number in pdf-config
sed -i "s/{PDF Version}/$VERSION/g" pdf/pdf-config.json

# Create the Markdown file for the cover pages
echo "<img src=\"images/book-cover.jpg\" style=\"overflow:hidden; margin-bottom:-25px;\" />
        <h1 style=\"position:fixed; top:52.48%; right:46.9%; color: white;
                    border:none; font-family: 'Montserrat';font-weight: 500;
                    font-style: normal;\" >$VERSION</h1>" > build/cover-$VERSION.md
echo "<img src=\"images/second-cover.png\" style=\"overflow:hidden; margin-bottom:-25px;\" />" > build/second-cover-$VERSION.md
echo "<img src=\"images/back-cover.png\" style=\"overflow:hidden; margin-bottom:-25px;\" />" > build/back-$VERSION.md

# Create the single document Markdown file
# Sed section 1: Add page break after each chapter
# Sed section 2: Correct Markdown file links with fragment identifiers. Remove file path and keep fragment identifier alone.
ls build/md | sort -n | while read x; do cat build/md/$x | sed -e 's/^# /<div style=\"page-break-after: always\;\"><\/div>\
\
# /' | sed 's/\[\([^\n]\+\)\]([^\n]\+.md#\([^\)]\+\)/[\1](#\2/' | \
# Sed section 3 - 8: Replace internal Links inside headings with anchor tags inside the respective heading and link href as the heading text
sed 's/\(^#\{2\} \)\(\[\(.*\)\]\(.*\)\(\?\:\n\+\|$\)\)/<h2><a href=\"#\3\">\3<\/a><\/h2>/'  | \
sed 's/\(^#\{1\} \)\([0-9. ]*\) \(\[\(.*\)\]\(.*\)\(\?\:\n\+\|$\)\)/<h1>\2 <a href=\"#\4\">\4<\/a><\/h1>/'  | \
sed 's/\(^#\{2\} \)\([0-9. ]*\) \(\[\(.*\)\]\(.*\)\(\?\:\n\+\|$\)\)/<h2>\2 <a href=\"#\4\">\4<\/a><\/h2>/' | \
sed 's/\(^#\{2\} \)\(Appendix [ABCDE]\.\) \(\[\(.*\)\]\(.*\)\(\?\:\n\+\|$\)\)/<h2>\2 <a href=\"#\4\">\4<\/a><\/h2>/' | \
sed 's/\(^#\{3\} \)\([0-9. ]*\) \(\[\(.*\)\]\(.*\)\(\?\:\n\+\|$\)\)/<h3>\2 <a href=\"#\4\">\4<\/a><\/h3>/'| \
sed 's/\(^#\{4\} \)\([0-9. ]*\) \(\[\(.*\)\]\(.*\)\(\?\:\n\+\|$\)\)/<h4>\2 <a href=\"#\4\">\4<\/a><\/h4>/' | \
sed 's/\(^#\{5\} \)\([0-9. ]*\) \(\[\(.*\)\]\(.*\)\(\?\:\n\+\|$\)\)/<h5>\2 <a href=\"#\4\">\4<\/a><\/h5>/' | \
# Sed section 9 - 13: Add header text as `id` element for heading to get referenced by links
sed 's/\(^#\{1\} \) *\([^\n]\+\?\))*\(\?\:\n\+\|$\)/<h1 id=\"\2\">\2<\/h1>/' | \
sed 's/\(^#\{2\} \) *\([^\n]\+\?\))*\(\?\:\n\+\|$\)/<h2 id=\"\2\">\2<\/h2>/' | \
sed 's/\(^#\{3\} \) *\([^\n]\+\?\))*\(\?\:\n\+\|$\)/<h3 id=\"\2\">\2<\/h3>/' | \
sed 's/\(^#\{4\} \) *\([^\n]\+\?\))*\(\?\:\n\+\|$\)/<h4 id=\"\2\">\2<\/h4>/' | \
sed 's/\(^#\{5\} \) *\([^\n]\+\?\))*\(\?\:\n\+\|$\)/<h5 id=\"\2\">\2<\/h5>/' | \
# Sed section 14: Set href for internal links. Remove subsection numbers from href.
sed 's/\[\([^\[]*\)\]([^\[]*[0-9]\-\([^(]*\.md\))/<a href=\"#\2\">\1<\/a>/g' | \
# Sed section 15: Set href for Appendix internal links. Remove subsection numbers from href.
sed 's/\[\([^\[]*\)\]([^\[]*[ABCDE]-\([^(]*\.md\))/<a href=\"#\2\">\1<\/a>/g' | \
# pyhton section 16: convert all chars inside href to lower case
python -c "import re; import sys; print(re.sub(r'href=\"(#[^\"]*\.md)\"', lambda m: m.group().lower(), sys.stdin.read()))"  | \
# pyhton section 17: Replace the spaces inside `href` values with hyphen
python -c "import re; import sys; print(re.sub(r'href=\"(#[^\"]*\.md)\"', lambda m: m.group().replace(' ', '-'), sys.stdin.read()))" | \
# pyhton section 18: Replace the `_` inside `href` values with hyphen
python -c "import re; import sys; print(re.sub(r'href=\"(#[^\"]*\.md)\"', lambda m: m.group().replace('_', '-'), sys.stdin.read()))"  | \
# pyhton section 19: remove readme.md from the file path inside href
python -c "import re; import sys; print(re.sub(r'href=\"(#[^\"]*/readme\.md)\"', lambda m: m.group().replace('/readme.md', ''), sys.stdin.read()))"  | \
# pyhton section 20: remove .md from all file path inside href
python -c "import re; import sys; print(re.sub(r'href=\"(#[^\"]*\.md)\"', lambda m: m.group().replace('.md', ''), sys.stdin.read()))"  | \
# pyhton section 21: Replace the spaces inside 'id' value with hyphen
python -c "import re; import sys; print(re.sub(r'id=\"([^\n]+)\"', lambda m: m.group().replace(' ', '-'), sys.stdin.read()))"  | \
# pyhton section 22: convert all chars inside id to lower case
python -c "import re; import sys; print(re.sub(r'id=\"([^\n]+)\"', lambda m: m.group().lower(), sys.stdin.read()))"  | \
# pyhton section 23 - 25: Remove `:`, `,`, `.` inside id values
python -c "import re; import sys; print(re.sub(r'id=\"([^\n]+)\"', lambda m: m.group().replace(':', ''), sys.stdin.read()))"  | \
python -c "import re; import sys; print(re.sub(r'id=\"([^\n]+)\"', lambda m: m.group().replace('.', ''), sys.stdin.read()))"  | \
python -c "import re; import sys; print(re.sub(r'id=\"([^\n]+)\"', lambda m: m.group().replace(',', ''), sys.stdin.read()))"  | \
# pyhton section 26: Replace the space with hyphen inside href values
python -c "import re; import sys; print(re.sub(r'href=\"(#[^\"]*)\"', lambda m: m.group().replace(' ', '-'), sys.stdin.read()))" | \
# pyhton section 27: convert all chars inside href to lower case
python -c "import re; import sys; print(re.sub(r'href=\"(#[^\"]*)\"', lambda m: m.group().lower(), sys.stdin.read()))"  | \
# Sed section 28: Move the number out of href
sed 's/<h1 id=\"[0-9.]*-\(.*\)\">\(.*\)<\/h1>/<h1 id="\1">\2<\/h1>/' | \
# Sed section 29: Add design to image name text
sed 's/\*\(Figure [0-9.\-]*\: .*\)\*/<div class="image-name-tag-wrap"><span class="image-name-tag">\1<\/span><\/div>/' >>  build/wstg-doc-$VERSION.md ; done

# Create cover pages by converting Markdown to PDF
md-to-pdf  --config-file pdf/pdf-config.json  --pdf-options '{"margin":"0mm", "format": "A4"}' build/cover-$VERSION.md
md-to-pdf  --config-file pdf/pdf-config.json  --pdf-options '{"margin":"0mm", "format": "A4"}' build/second-cover-$VERSION.md
md-to-pdf  --config-file pdf/pdf-config.json  --pdf-options '{"margin":"0mm", "format": "A4"}' build/back-$VERSION.md

# Create Document body pages by converting Markdown to PDF
md-to-pdf  --config-file pdf/pdf-config.json build/wstg-doc-$VERSION.md

# Combine Cover page and Document body
pdftk build/cover-$VERSION.pdf build/second-cover-$VERSION.pdf build/wstg-doc-$VERSION.pdf build/back-$VERSION.pdf cat output build/wstg-com-$VERSION.pdf

# Create chapter wise Markdown files for generating bookmarks
# Sed and Python sections are exactly same as the previous one
ls build/md | sort -n | while read x; do cat build/md/$x | sed -e 's/^# /<div style=\"page-break-after: always\;\"><\/div>\
\
# /' | sed 's/\[\([^\n]\+\)\]([^\n]\+.md#\([^\)]\+\)/[\1](#\2/' | \
sed 's/\(^#\{2\} \)\(\[\(.*\)\]\(.*\)\(\?\:\n\+\|$\)\)/<h2><a href=\"#\3\">\3<\/a><\/h2>/'  | \
sed 's/\(^#\{1\} \)\([0-9. ]*\) \(\[\(.*\)\]\(.*\)\(\?\:\n\+\|$\)\)/<h1>\2 <a href=\"#\4\">\4<\/a><\/h1>/'  | \
sed 's/\(^#\{2\} \)\([0-9. ]*\) \(\[\(.*\)\]\(.*\)\(\?\:\n\+\|$\)\)/<h2>\2 <a href=\"#\4\">\4<\/a><\/h2>/' | \
sed 's/\(^#\{3\} \)\([0-9. ]*\) \(\[\(.*\)\]\(.*\)\(\?\:\n\+\|$\)\)/<h3>\2 <a href=\"#\4\">\4<\/a><\/h3>/'| \
sed 's/\(^#\{4\} \)\([0-9. ]*\) \(\[\(.*\)\]\(.*\)\(\?\:\n\+\|$\)\)/<h4>\2 <a href=\"#\4\">\4<\/a><\/h4>/' | \
sed 's/\(^#\{5\} \)\([0-9. ]*\) \(\[\(.*\)\]\(.*\)\(\?\:\n\+\|$\)\)/<h5>\2 <a href=\"#\4\">\4<\/a><\/h5>/' | \
sed 's/\(^#\{1\} \) *\([^\n]\+\?\))*\(\?\:\n\+\|$\)/<h1 id=\"\2\">\2<\/h1>/' | \
sed 's/\(^#\{2\} \) *\([^\n]\+\?\))*\(\?\:\n\+\|$\)/<h2 id=\"\2\">\2<\/h2>/' | \
sed 's/\(^#\{3\} \) *\([^\n]\+\?\))*\(\?\:\n\+\|$\)/<h3 id=\"\2\">\2<\/h3>/' | \
sed 's/\(^#\{4\} \) *\([^\n]\+\?\))*\(\?\:\n\+\|$\)/<h4 id=\"\2\">\2<\/h4>/' | \
sed 's/\(^#\{5\} \) *\([^\n]\+\?\))*\(\?\:\n\+\|$\)/<h5 id=\"\2\">\2<\/h5>/' | \
sed 's/\[\([^\[]*\)\]([^\[]*[0-9]\-\([^(]*\.md\))/<a href=\"#\2\">\1<\/a>/g' | \
sed 's/\[\([^\[]*\)\]([^\[]*[ABCDE]-\([^(]*\.md\))/<a href=\"#\2\">\1<\/a>/g' | \
python -c "import re; import sys; print(re.sub(r'href=\"(#[^\"]*\.md)\"', lambda m: m.group().lower(), sys.stdin.read()))"  | \
python -c "import re; import sys; print(re.sub(r'href=\"(#[^\"]*\.md)\"', lambda m: m.group().replace(' ', '-'), sys.stdin.read()))" | \
python -c "import re; import sys; print(re.sub(r'href=\"(#[^\"]*\.md)\"', lambda m: m.group().replace('_', '-'), sys.stdin.read()))"  | \
python -c "import re; import sys; print(re.sub(r'href=\"(#[^\"]*/readme\.md)\"', lambda m: m.group().replace('/readme.md', ''), sys.stdin.read()))"  | \
python -c "import re; import sys; print(re.sub(r'href=\"(#[^\"]*\.md)\"', lambda m: m.group().replace('.md', ''), sys.stdin.read()))"  | \
python -c "import re; import sys; print(re.sub(r'id=\"([^\n]+)\"', lambda m: m.group().replace(' ', '-'), sys.stdin.read()))"  | \
python -c "import re; import sys; print(re.sub(r'id=\"([^\n]+)\"', lambda m: m.group().lower(), sys.stdin.read()))"  | \
python -c "import re; import sys; print(re.sub(r'id=\"([^\n]+)\"', lambda m: m.group().replace(':', ''), sys.stdin.read()))"  | \
python -c "import re; import sys; print(re.sub(r'id=\"([^\n]+)\"', lambda m: m.group().replace('.', ''), sys.stdin.read()))"  | \
python -c "import re; import sys; print(re.sub(r'id=\"([^\n]+)\"', lambda m: m.group().replace(',', ''), sys.stdin.read()))"  | \
python -c "import re; import sys; print(re.sub(r'href=\"(#[^\"]*)\"', lambda m: m.group().replace(' ', '-'), sys.stdin.read()))" | \
python -c "import re; import sys; print(re.sub(r'href=\"(#[^\"]*)\"', lambda m: m.group().lower(), sys.stdin.read()))"  | \
sed 's/<h1 id=\"[0-9.]*-\(.*\)\">\(.*\)<\/h1>/<h1 id="\1">\2<\/h1>/' | \
sed 's/\*\(Figure [0-9.\-]*\: .*\)\*/<div class="image-name-tag-wrap"><span class="image-name-tag">\1<\/span><\/div>/'  >  build/pdf/$x ; done

# Copy images to the temporary folder to generate chapter wise PDFs
cp -r build/images build/pdf/

# Generate chapter wise PDF files
for f in build/pdf/*.md ; do
    md-to-pdf  --config-file pdf/pdf-config.json $f && rm $f;
done


# In rare cases some PDF files has a blank page at the end due to newlines or box padding.
# This affects the bookmark creation. So Remove those last pages if it is less than 13000 bytes
for f in build/pdf/*.pdf; do
    pdftk $f cat end output lastpage.pdf
    size=$(du -b lastpage.pdf | cut -f 1)
    if [ $size -lt "13000" ]; then
        page_count=$(pdftk $f dump_data | grep NumberOfPages | awk  '{print $2}')
        page_count=$(( $page_count - 1 ))
        pdftk A="$f" cat A1-$page_count output tempfile.pdf
        mv tempfile.pdf $f
        rm lastpage.pdf
    fi
done;

# Generate chapter details from individual chapter PDF files
# Extracts folder names and number of pages in each chapter
# Write this to chapters.txt inside build folder
for f in build/pdf/*.pdf; do
    IFS='>>>' read -ra FILE <<< "$f";
    for i in "${FILE[@]}"; do
        echo $i | \
        sed 's/build\/pdf\/document/section: /'  | \
        sed 's/\([0-9.]\+\)-\(.*\)\.pdf/\1 \; file: \2 \;/' | \
        sed 's/\([0-9.]\+\)-\(.*\)/\1 \; sectionTitle: \2 \; subsection: /' | \
        sed 's/\([ABCDE]\)-\(.*\)\.pdf/\1 - \2\;/' | \
        sed 's/_/ /g' | \
        tr -d '\n' >> build/chapters.txt;
    done;
    pdftk $f dump_data | grep NumberOfPages | awk  '{print "numberofpages: " $2 " ;"}' >>  build/chapters.txt;
done;

# Generate 'bookmarks' file inside the build folder with data from chapters.txt
sectionValue="";
subsection1Value="";
subsection2Value="";
pagenumber=3;
headerlevel=0;
subsection1="";
subsection2="";
while read line; do
    IFS=';'
    read -ra entry <<< "$line";
    for i in ${entry[@]}; do
        IFS=':'
        read -r title value <<< $i
        title=$(echo $title | sed 's/ *$//g' | sed 's/^ *//g')
        value=$(echo $value | sed 's/ *$//g' | sed 's/^ *//g')

        if [ "$title" == "subsection" ]; then
            headerlevel=$(($headerlevel+1));
            if [ $headerlevel -ne 0 ]; then
                title="subsection$headerlevel";
            fi
        fi

        if [ "$title" == "sectionTitle" ]; then
            if [ $headerlevel -ne 0 ]; then
                title="sectionTitle$headerlevel";
            fi
        fi
        if [ "$title" == "file" ]; then
            headerlevel=$(($headerlevel+1));
        fi
        declare "$title=$value";
    done
    if [[ -n $sectionTitle ]]; then
        echo "BookmarkBegin" >> build/bookmarks;
        if [ "$sectionValue" != "$section" ]; then
            sectionValue=$section;
            echo "BookmarkTitle:" $section - $sectionTitle >> build/bookmarks;
            echo "BookmarkLevel: 1"  >> build/bookmarks;
        else
            if [[ -n $sectionTitle1 ]]; then
                if [ "$subsection1Value" != "$subsection1" ]; then
                    subsection1Value=$subsection1;
                    if [ "$sectionTitle" == "Appendix" ] ; then
                        echo "BookmarkTitle:" $subsection1  >> build/bookmarks;
                    else
                        echo "BookmarkTitle:" $subsection1 - $sectionTitle1 >> build/bookmarks;
                    fi
                    echo "BookmarkLevel: 2"  >> build/bookmarks;
                else
                    if [[ -n $sectionTitle2 ]]; then
                        if [ "$subsection2Value" != "$subsection2" ]; then
                            subsection2Value=$subsection2;
                            echo "BookmarkTitle:" $subsection2 - $sectionTitle2 >> build/bookmarks;
                        else
                            if [ "$file" == "0.0 README" ] ; then
                                echo "BookmarkTitle:" $subsection2 - $sectionTitle2 >> build/bookmarks;
                            else
                                echo "BookmarkTitle:" $subsection2 - $file >> build/bookmarks;
                            fi
                        fi
                    else
                        if [ "$file" == "0.0 README" ] ; then
                            echo "BookmarkTitle:" $subsection2 - sectionTitle1 >> build/bookmarks;
                        else
                            echo "BookmarkTitle:" $subsection2 - $file >> build/bookmarks;
                        fi
                    fi
                    echo "BookmarkLevel: 3" >> build/bookmarks;
                fi
            else
                if [ "$file" == "0.0 README" ] ; then
                    echo "BookmarkTitle:" $subsection1 - $sectionTitle >> build/bookmarks;
                else
                    echo "BookmarkTitle:" $subsection1 - $file >> build/bookmarks;
                fi
                echo "BookmarkLevel: 2"  >> build/bookmarks;
            fi
        fi
        echo "BookmarkPageNumber:" $pagenumber >> build/bookmarks;
    else
        echo "BookmarkBegin" >> build/bookmarks;
        echo "BookmarkTitle: Table of Contents"  >> build/bookmarks;
        echo "BookmarkLevel: 1"  >> build/bookmarks;
        echo "BookmarkPageNumber:" $pagenumber >> build/bookmarks;
    fi
    pagenumber=$(($pagenumber+$numberofpages));
    numberofpages=0;
    headerlevel=0;

done < build/chapters.txt;


# Dumping PDF metadata from already created PDF to pdf_data file inside the build folder
pdftk build/wstg-com-$VERSION.pdf dump_data_utf8 output build/pdf_data

# Clear dumped pdf_data file of any previous bookmarks
sed -i '/Bookmark/d' build/pdf_data

# Inserting previously created bookmarks in to the pdf_data file
sed -i "/NumberOfPages/r build/bookmarks" build/pdf_data

# Create the final pdf by inserting the metadata from pdf_data file
pdftk build/wstg-com-$VERSION.pdf update_info_utf8 build/pdf_data output build/wstg-$VERSION.pdf
