#!/bin/bash
# Script to create the PDF file for WSTG

# Clean and create required build folders
clean_build () {
    # Clean the build folder
    rm -rf build
    # Create the required build folders
    mkdir -p build/md
    mkdir -p build/pdf
    mkdir -p build/images
}

# Prepare build folder with necessary files
prepare_build () {
    # Copy Markdown and Image files to build directory
    # Replace path separators "/" with ">>>" in .md files for better splitting in later stages
    find document -name "*.md" | while IFS= read -r FILE; do cp -v "$FILE" build/md/"${FILE//\//>>>}"; done
    find document -name "images"  -exec cp -r {}/. build/images/. ";"
    cp .github/pdf/assets/cover.jpg build/images/book-cover.jpg
    cp .github/pdf/assets/cover-$VERSION.jpg build/images/book-cover-$VERSION.jpg
    cp .github/pdf/assets/back-cover.png build/images/back-cover.png
    cp .github/pdf/assets/second-cover.png build/images/second-cover.png

    # Rename README files by prepending "0-0.0_" to keep them in the correct order
    find build/md -name "*README.md" | while IFS= read -r FILE; do mv -v "$FILE" "${FILE//README/0-0.0_README}"; done

    # Extract version nuber from version tag
    VERSION_NUMBER=`echo $VERSION | sed 's/v//'`
    # Update build version number in pdf-config
    sed -i "s/{PDF Version}/$VERSION/g" .github/pdf/pdf-config.json

    # Copy images to the temporary folder to generate chapter wise PDFs
    cp -r build/images build/pdf/
}

# Create the Markdown file for the front cover and generate front cover with md-to-pdf
create_front_cover () {
# Create the cover image with versioned image if exists else use the default with version number
VERSIONED_COVER_IMAGE_FILE=images/book-cover-$VERSION.jpg
if [[ -f "build/$VERSIONED_COVER_IMAGE_FILE" ]]; then
    echo "<img src=\"$VERSIONED_COVER_IMAGE_FILE\" />" > build/cover-$VERSION.md
else
    echo "<img src=\"images/book-cover.jpg\" />
        <h1 style=\"position:fixed; top:61.44%; right:37%; color: #ffffff !important;
                    border:none; font-weight: 500; font-size:33px;
                    font-style: normal;\" >$VERSION_NUMBER</h1>" > build/cover-$VERSION.md
fi
# Generate front cover with md-to-pdf
md-to-pdf  --config-file .github/pdf/pdf-config.json  --pdf-options '{"margin":"0mm", "format": "A4"}' build/cover-$VERSION.md
# Remove Blank pages from the cover page if any
remove_blank_pages build/cover-$VERSION.pdf
}

# Create the Markdown file for the second cover and generate second cover with md-to-pdf
create_second_cover () {
echo "<img src=\"images/second-cover.png\" />" > build/second-cover-$VERSION.md
# Generate second cover with md-to-pdf
md-to-pdf  --config-file .github/pdf/pdf-config.json  --pdf-options '{"margin":"0mm", "format": "A4"}' build/second-cover-$VERSION.md
# Remove Blank pages from the cover page if any
remove_blank_pages build/second-cover-$VERSION.pdf
}

# Create the Markdown file for the back cover and generate back cover with md-to-pdf
create_back_cover () {
echo "<img src=\"images/back-cover.png\"  />" > build/back-$VERSION.md
# Generate back cover with md-to-pdf
md-to-pdf  --config-file .github/pdf/pdf-config.json  --pdf-options '{"margin":"0mm", "format": "A4"}' build/back-$VERSION.md
# Remove Blank pages from the cover page if any
remove_blank_pages build/back-$VERSION.pdf
}

# Some PDF files has a blank page at the end due to newlines or box padding.
# Remove those blank last pages if it is less than 13000 bytes in PDF files
remove_blank_pages () {
    pdftk $1 cat end output lastpage.pdf
    size=$(du -b lastpage.pdf | cut -f 1)
    if [ $size -lt "13000" ]; then
        page_count=$(pdftk $1 dump_data | grep NumberOfPages | awk  '{print $2}')
        page_count=$(( $page_count - 1 ))
        pdftk A="$1" cat A1-$page_count output tempfile.pdf
        mv tempfile.pdf $1
        rm lastpage.pdf
    fi
}

# Add page break after each chapter
add_page_break () {
    echo '<div style="page-break-after: always;"></div>'
}

# Replace internal markdown Links inside headings with html anchor tags (<a>)
# within the respective heading tag ( <h1>, <h2> .. ) and link href as the heading text
# eg: ## 0. [Foreword by Eoin Keary](0-Foreword/README.md)  ->  <h2><a href="Foreword by Eoin Keary">Foreword by Eoin Keary</a></h2>
# spaces inside the href will be addressed in later steps
replace_internal_markdown_links_with_in_headers_with_html_tags () {
    sed 's/\(^#\{2\} \)\(\[\(.*\)\]\(.*\)\(\?\:\n\+\|$\)\)/<h2><a href=\"#\3\">\3<\/a><\/h2>/'  | \
    sed 's/\(^#\{1\} \)\([0-9. ]*\) \(\[\(.*\)\]\(.*\)\(\?\:\n\+\|$\)\)/<h1>\2 <a href=\"#\4\">\4<\/a><\/h1>/'  | \
    sed 's/\(^#\{2\} \)\([0-9. ]*\) \(\[\(.*\)\]\(.*\)\(\?\:\n\+\|$\)\)/<h2>\2 <a href=\"#\4\">\4<\/a><\/h2>/' | \
    sed 's/\(^#\{2\} \)\(Appendix [ABCDEF]\.\) \(\[\(.*\)\]\(.*\)\(\?\:\n\+\|$\)\)/<h2>\2 <a href=\"#\4\">\4<\/a><\/h2>/' | \
    sed 's/\(^#\{3\} \)\([0-9. ]*\) \(\[\(.*\)\]\(.*\)\(\?\:\n\+\|$\)\)/<h3>\2 <a href=\"#\4\">\4<\/a><\/h3>/'| \
    sed 's/\(^#\{4\} \)\([0-9. ]*\) \(\[\(.*\)\]\(.*\)\(\?\:\n\+\|$\)\)/<h4>\2 <a href=\"#\4\">\4<\/a><\/h4>/' | \
    sed 's/\(^#\{5\} \)\([0-9. ]*\) \(\[\(.*\)\]\(.*\)\(\?\:\n\+\|$\)\)/<h5>\2 <a href=\"#\4\">\4<\/a><\/h5>/' $1
}

# Replace markdown headers with heading tags (<h1>, <h2> etc..)
# and add header text as `id` elementto get referenced by internal links
# eg: # Testing for Cookies Attributes  ->
#     <h1 id="Testing for Cookies Attributes">Testing for Cookies Attributes</h1>
# spaces inside the id will be addressed in later steps
replace_markdown_headers_with_html_tags () {
    sed 's/\(^#\{1\} \) *\([^\n]\+\?\))*\(\?\:\n\+\|$\)/<h1 id=\"\2\">\2<\/h1>/' | \
    sed 's/\(^#\{2\} \) *\([^\n]\+\?\))*\(\?\:\n\+\|$\)/<h2 id=\"\2\">\2<\/h2>/' | \
    sed 's/\(^#\{3\} \) *\([^\n]\+\?\))*\(\?\:\n\+\|$\)/<h3 id=\"\2\">\2<\/h3>/' | \
    sed 's/\(^#\{4\} \) *\([^\n]\+\?\))*\(\?\:\n\+\|$\)/<h4 id=\"\2\">\2<\/h4>/' | \
    sed 's/\(^#\{5\} \) *\([^\n]\+\?\))*\(\?\:\n\+\|$\)/<h5 id=\"\2\">\2<\/h5>/' $1
}

# Replace internal markdown Links with html anchor tags (<a>)
# Set link href as the heading text, Remove subsection numbers from href.
# Exclude links starts with http, make sure not to replace external links
# eg: [testing browser storage](../11-Client-side_Testing/12-Testing_Browser_Storage.md) ->
#     <a href="Testing_Browser_Storage.md">testing browser storage</a>
# Underscore and .md in the href addressed in later steps
replace_internal_markdown_links_with_html_tags () {
    # Appendix internal links.
    sed '/[\[^\[\]*](http[^\[]*\.md)/! s/\[\([^\[]*\)\]([^\[]*[ABCDEF]-\([^(]*\.md\))/<a href=\"#\2\">\1<\/a>/g' | \
    # For all other internal links.
    sed '/[\[^\[\]*](http[^\[]*\.md)/! s/\[\([^\[]*\)\]([^\[]*[0-9]\-\([^(]*\.md\))/<a href=\"#\2\">\1<\/a>/g' $1
}

# Replace Markdown links with fragment identifiers with html <a> tag.
# Remove file path and keep fragment identifier alone.
# Exclude urls start with http (Helps to exclude urls to external markdown files with fragment)
# eg: [Identify Application Entry Points](06-Identify_Application_Entry_Points.md#v74-error-handling) ->
#     <a href="#v74-error-handling">Identify Application Entry Points</a>
replace_internal_markdown_links_having_fragments_with_html_tags () {
    sed '/[\[^\[\]*](http[^\[]*\.md#\([^\)]\+\))/! s/\[\([^\n]\+\)\]([^\n]\+.md#\([^\)]\+\))/<a href=\"#\2\">\1<\/a>/' | \
    # Links with fragment identifiers alone
    sed 's/\[\([^\[]\+\)\](#\([^\)]\+\))/<a href=\"#\2\">\1<\/a>/' $1
}

# Convert all chars inside href to lower case
# Handles the href with .md extention ( Keeps this .md inside the href to identify internal markdown links)
convert_internal_markdown_href_to_lower_case () {
    python -c "import re; import sys; print(re.sub(r'href=\"(#[^\"]*\.md)\"', lambda m: m.group().lower(), sys.stdin.read()))"
}

# Replace the spaces and _ inside `href` values with hyphen
# Handles the href with .md extention ( Keeps this .md inside the href to identify internal markdown links)
replace_space_and_underscore_with_hyphen_in_internal_markdown_href () {
    # Replace space and underscore
    python -c "import re; import sys; print(re.sub(r'href=\"(#[^\"]*\.md)\"', lambda m: m.group().replace(' ', '-').replace('_', '-'), sys.stdin.read()))"
}

# Remove readme.md and .md extentions from href
# This extention inside href used to identify the internal markdown links
remove_markdown_file_extention_from_href () {
    # Remove readme.md
    python -c "import re; import sys; print(re.sub(r'href=\"(#[^\"]*/readme\.md)\"', lambda m: m.group().replace('/readme.md', ''), sys.stdin.read()))"  | \
    # Remove .md
    python -c "import re; import sys; print(re.sub(r'href=\"(#[^\"]*\.md)\"', lambda m: m.group().replace('.md', ''), sys.stdin.read()))"
}

# Replace the spaces inside 'id' value with hyphen
replace_space_with_hyphen_in_id () {
    python -c "import re; import sys; print(re.sub(r'id=\"([^\n]+)\"', lambda m: m.group().replace(' ', '-'), sys.stdin.read()))"
}

# Convert all chars inside id to lower case
convert_id_to_lower_case () {
    python -c "import re; import sys; print(re.sub(r'id=\"([^\n]+)\"', lambda m: m.group().lower(), sys.stdin.read()))"
}

# Remove `:`, `,`, `.` inside id values
remove_special_chars_from_id () {
    python -c "import re; import sys; print(re.sub(r'id=\"([^\n]+)\"', lambda m: m.group().replace(':', '').replace(':', '').replace('.', '').replace(',', ''), sys.stdin.read()))"
}

# Replace spaces with hyphen inside href value
replace_space_with_hyphen_in_href () {
    python -c "import re; import sys; print(re.sub(r'href=\"(#[^\"]*)\"', lambda m: m.group().replace(' ', '-'), sys.stdin.read()))"
}

# Convert all chars inside href to lower case
convert_href_to_lower_case () {
    python -c "import re; import sys; print(re.sub(r'href=\"(#[^\"]*)\"', lambda m: m.group().lower(), sys.stdin.read()))"
}

# Move chapter number out of href links
remove_chapter_numbers_from_link () {
    sed 's/<h1 id=\"[0-9.]*-\(.*\)\">\(.*\)<\/h1>/<h1 id="\1">\2<\/h1>/' $1
}

# Add design to image and remove extra '\'
add_design_to_images () {
    sed 's/\!\[\([^\[]*\)\](\(.*\)).$/<div class="image-center"><img src="\2" alt="\1"><\/div>/' $1
}

# Add design to image name text
add_design_to_image_name_tag () {
   sed 's/\*\(Figure [0-9.ABCDEF\-]*\: .*\)\*/<div class="image-name-tag-wrap"><span class="image-name-tag">\1<\/span><\/div>/'  $1
}

# Add design to the test case id table
add_design_to_test_case_id_table () {
    # sed -e '/<table>/,/<th>ID<\/th>/ s/<table>/<table class="test-case-id-table">/' $1
    # sed 's/\|ID[.]*\|[\n]\|[-]*\|[\n]\|(WSTG-[A-Z]*-[0-9]*)\|/<table class="test-case-id-table"><thead><tr><th>ID</th></tr></thead><tbody><tr><td>\1</td></tr></tbody></table>/' $1
    # sed 's/<table>\s<thead>\s<tr>\s<th>ID<\/th>\s<\/tr>\s<\/thead>/<table class="test-case-id-table"><thead><tr><th>ID<\/th><\/tr>\/thead>/' $1
    sed '
    /|ID.*|/,/|WSTG-[A-Z]*-[0-9]*|/ {
        s/|ID.*|//
        s/|[-]*|//
        s/|\(WSTG-[A-Z]*-[0-9]*\)|/<ul class="arrowbox"><li class="first">ID<\/li><li class="second">\1<\/li><\/ul>/
    }
    ' $1
}

# Preprocess markdown files to support internal links and image designs
preprocess_markdown_to_support_md_to_pdf () {
    cat build/md/$1 | \
    replace_internal_markdown_links_with_in_headers_with_html_tags | \
    replace_markdown_headers_with_html_tags | \
    replace_internal_markdown_links_with_html_tags | \
    # Sed section: Workaround to address the bug in duplicate fragment links in 4.1.
    sed 's/\[\([^\n]\+\)\](#tools)/\1/i' |\
    sed 's/\[\([^\n]\+\)\](#references)/\1/i' |\
    sed 's/\[\([^\n]\+\)\](#Remediation)/\1/i' |\
    sed 's/\[\([^\n]\+\)\]([^\n]\+.md#remediation)/\1/i' | \
    replace_internal_markdown_links_having_fragments_with_html_tags |\
    convert_internal_markdown_href_to_lower_case  | \
    replace_space_and_underscore_with_hyphen_in_internal_markdown_href | \
    remove_markdown_file_extention_from_href | \
    replace_space_with_hyphen_in_id | \
    convert_id_to_lower_case  | \
    remove_special_chars_from_id  | \
    replace_space_with_hyphen_in_href  | \
    convert_href_to_lower_case | \
    remove_chapter_numbers_from_link | \
    add_design_to_images | \
    add_design_to_test_case_id_table | \
    { add_design_to_image_name_tag; add_page_break;}
}

extract_chapter_details_and_page_number_from_pdf () {
    # Extracts folder names and number of pages in each chapter
    # Write this to chapters.txt inside build folder
    IFS='>>>' read -ra FILE <<< "$1";
    for i in "${FILE[@]}"; do
        echo $i | \
        sed 's/build\/pdf\/document/section: /'  | \
        sed 's/\([0-9.]\+\)-\(.*\)\.pdf/\1 \; file: \2 \;/' | \
        sed 's/\([0-9.]\+\)-\(.*\)/\1 \; sectionTitle: \2 \; subsection: /' | \
        sed 's/\([ABCDEF]\)-\(.*\)\.pdf/\1 - \2\;/' | \
        sed 's/_/ /g' | \
        tr -d '\n' >> build/chapters.txt;
    done;
    pdftk $1 dump_data | grep NumberOfPages | awk  '{print "numberofpages: " $2 " ;"}' >>  build/chapters.txt;
}

# Generate 'bookmarks' file inside the build folder with data from chapters.txt
generate_bookmark_data_from_chapter_details () {
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
    sectionTitle1=""
    sectionTitle2=""
done < build/chapters.txt;

}

# ---------------------------------------------------------------------------------------------

VERSION=$1
echo "Creating PDF for version $VERSION"

clean_build

prepare_build

create_front_cover
create_second_cover
create_back_cover

# Preporcess the markdown to create the single document Markdown file
ls build/md | sort -n | while read x; do preprocess_markdown_to_support_md_to_pdf $x  >>  build/wstg-doc-$VERSION.md ; done

# Create document body pages by converting Markdown to PDF
md-to-pdf  --config-file .github/pdf/pdf-config.json build/wstg-doc-$VERSION.md

# Remove Blank pages from the combined PDF
remove_blank_pages build/wstg-doc-$VERSION.pdf

# Combine Cover page and Document body
pdftk build/cover-$VERSION.pdf build/second-cover-$VERSION.pdf build/wstg-doc-$VERSION.pdf build/back-$VERSION.pdf cat output build/wstg-com-$VERSION.pdf

# Create chapter wise Markdown files for generating bookmarks
ls build/md | sort -n | while read x; do  preprocess_markdown_to_support_md_to_pdf $x >  build/pdf/$x ; done

# Generate chapter wise PDF files and extract chapter details
for f in build/pdf/*.md ; do
    md-to-pdf  --config-file .github/pdf/pdf-config.json $f && rm $f;
    pdf_gen_file=${f/%.md/.pdf}
    # Remove blank pages from generated PDF
    remove_blank_pages $pdf_gen_file
    # Extracts chapter details and write to chapters.txt
    extract_chapter_details_and_page_number_from_pdf $pdf_gen_file
done

generate_bookmark_data_from_chapter_details

# Dumping PDF metadata from already created PDF to pdf_data file inside the build folder
pdftk build/wstg-com-$VERSION.pdf dump_data_utf8 output build/pdf_data

# Clear dumped pdf_data file of any previous bookmarks
sed -i '/Bookmark/d' build/pdf_data

# Inserting previously created bookmarks in to the pdf_data file
sed -i "/NumberOfPages/r build/bookmarks" build/pdf_data

# Create the final pdf by inserting the metadata from pdf_data file
pdftk build/wstg-com-$VERSION.pdf update_info_utf8 build/pdf_data output build/wstg-$VERSION.pdf
