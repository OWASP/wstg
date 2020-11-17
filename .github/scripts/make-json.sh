#!/bin/bash
# Script to create the Json checklist file for WSTG

cd document/4-Web_Application_Security_Testing

# Start the json string
echo "{" > checklist.json
# Open categories
echo "    \"categories\": {"  >> checklist.json
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
                echo "        ,\"${category%?}\": {" | tr '_' ' '  >> checklist.json
            else
                echo "        \"${category%?}\": {" | tr '_' ' '  >> checklist.json
            fi
            # Get category ID from the first file
            cid=`cat $d/01-* | grep "|WSTG-.*" | cut -d "|" -f 2 | sed 's/-01//'`
            # Add category ID and start tests
            echo "            \"id\":\"${cid}\","  >> checklist.json
            echo "            \"tests\":["  >> checklist.json
            count=0
            for file in $d*.md; do
                # Remove README
                if [[ $file != *"README.md" ]];then
                    # Add coma from the second entry of the list
                    if [ $count -gt 0 ];then
                        echo "                ,{"  >> checklist.json
                    else
                        echo "                {"  >> checklist.json
                    fi
                    # Get test ID, test name and reference link from the file
                    tid=`cat $file | grep "|WSTG-.*" | cut -d "|" -f 2`
                    # Get Objective of the test from the file
                    objective=`awk "/## Test Objectives/{flag=1; next} /## /{flag=0} flag" $file | tr '\n' ' '  `
                    read -r tname < $file
                    tname=${tname:2}
                    tref=`echo $file | sed 's/.md/.html/'`
                    # Add test ID, test name and reference link from the file
                    echo "                \"name\":\"${tname}\","  >> checklist.json
                    echo "                \"id\":\"${tid}\","  >> checklist.json
                    echo "                \"Reference\":\"https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/$tref\","  >> checklist.json
                    echo "                \"Objective\":\"${objective}\""  >> checklist.json
                    echo "                }"  >> checklist.json
                    count=$((count+1))
                fi
            done
            # Close tests list
            echo "            ]"  >> checklist.json
            # Close category sub section
            echo "        }"  >> checklist.json
        fi
    done <<< "$d"
done
# Close categories
echo "    }"  >> checklist.json
# End Json string
echo "}"  >> checklist.json
cat checklist.json

# Move generated file to checklist folder
mv checklist.json ../../checklist/.
