#!/bin/bash
# Script to create the Json checklist file for WSTG

cd document/4-Web_Application_Security_Testing

# Start the json string
echo "{" > testing-checklist.json
# Open categories
echo "    \"categories\": {"  >> testing-checklist.json
# Iterate all category folders to get the categories
for d in */ ; do
    # Split the folder name to get category and category number
    # Select folders start form 01
    while IFS='-' read -ra FOLD; do
        if [ ${FOLD[0]} -gt 0 ]
        then
            category=${FOLD[1]}
            # Start category sub section
            # Add coma from the second entry of the list
            if [ ${FOLD[0]} -gt 1 ];then
                echo "        ,\"${category%?}\": {" | tr '_' ' '  >> testing-checklist.json
            else
                echo "        \"${category%?}\": {" | tr '_' ' '  >> testing-checklist.json
            fi
            # Get category ID from the first file
            cid=`cat $d/01-* | grep "|WSTG-.*" | cut -d "|" -f 2 | sed 's/-01//'`
            # Add category ID and start tests
            echo "            \"id\":\"${cid}\","  >> testing-checklist.json
            echo "            \"tests\":["  >> testing-checklist.json
            count=0
            for file in $d*.md; do
                # Remove README
                if [[ $file != *"README.md" ]];then
                    # Add coma from the second entry of the list
                    if [ $count -gt 0 ];then
                        echo "                ,{"  >> testing-checklist.json
                    else
                        echo "                {"  >> testing-checklist.json
                    fi
                    # Get test ID, test name and reference link from the file
                    tid=`cat $file | grep "|WSTG-.*" | cut -d "|" -f 2`
                    tname=$(head -n 1 $file)
                    tname=${tname:2}
                    tref=`echo $file | sed 's/.md/.html/'`
                    # Add test ID, test name and reference link from the file
                    echo "                \"name\":\"${tname}\","  >> testing-checklist.json
                    echo "                \"id\":\"${tid}\","  >> testing-checklist.json
                    echo "                \"Reference\":\"https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/$tref\""  >> testing-checklist.json
                    echo "                }"  >> testing-checklist.json
                    count=$((count+1))
                fi
            done
            # Close tests list
            echo "            ]"  >> testing-checklist.json
            # Close category sub section
            echo "        }"  >> testing-checklist.json
        fi
    done <<< "$d"
done
# Close categories
echo "    }"  >> testing-checklist.json
# End Json string
echo "}"  >> testing-checklist.json

# Move generated file to checklist folder
mv testing-checklist.json ../../checklist/Testing-checklist.json