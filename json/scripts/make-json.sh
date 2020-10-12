#!/bin/bash
cd document/4-Web_Application_Security_Testing
echo "{" > testing-checklist.json
echo "    \"categories\": {"  >> testing-checklist.json
for d in */ ; do
    while IFS='-' read -ra FOLD; do
        # echo ${FOLD[0]}
        if [ ${FOLD[0]} -gt 0 ]
        then
            category=${FOLD[1]}
            if [ ${FOLD[0]} -gt 1 ];then
                echo "        ,\"${category%?}\": {" | tr '_' ' '  >> testing-checklist.json
            else
                echo "        \"${category%?}\": {" | tr '_' ' '  >> testing-checklist.json
            fi

            cid=`cat $d/01-* | grep "|WSTG-.*" | cut -d "|" -f 2 | sed 's/-01//'`
            echo "            \"id\":\"${cid}\","  >> testing-checklist.json
            echo "            \"tests\":["  >> testing-checklist.json
            count=0
            for file in $d*.md; do
                if [[ $file != *"README.md" ]];then
                    if [ $count -gt 0 ];then
                        echo "                ,{"  >> testing-checklist.json
                    else
                        echo "                {"  >> testing-checklist.json
                    fi
                    tid=`cat $file | grep "|WSTG-.*" | cut -d "|" -f 2`
                    tname=$(head -n 1 $file)
                    tname=${tname:2}
                    tref=`echo $file | sed 's/.md/.html/'`
                    echo "                \"name\":\"${tname}\","  >> testing-checklist.json
                    echo "                \"id\":\"${tid}\","  >> testing-checklist.json
                    echo "                \"Reference\":\"https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/$tref\""  >> testing-checklist.json
                    echo "                }"  >> testing-checklist.json
                    count=$((count+1))
                fi
            done
            echo "            ]"  >> testing-checklist.json
            echo "        }"  >> testing-checklist.json
        fi
        # for i in "${FOLD[@]}"; do
        #     if
        # done
    done <<< "$d"
done
echo "    }"  >> testing-checklist.json
echo "}"  >> testing-checklist.json

mv testing-checklist.json ../../checklist/Testing-checklist.json