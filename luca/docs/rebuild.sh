#!/bin/bash

STATEMENTS="statement-bank.txt statement-visa.txt"

for rulefile in rules*.yaml
do
    base=$(echo $rulefile | sed 's/rules/output/;s/.yaml//')
    if echo $rulefile | grep -q 't\.'
    then
        opt="-ct"
    else
        opt="-c"
    fi
    TERM=ansi COLUMNS=48 luca tally $opt $rulefile $STATEMENTS > $base.txt
    (echo '<pre>';
        cat $base.txt | ansi2html -i;
        echo '</pre>') > $base.html
done
