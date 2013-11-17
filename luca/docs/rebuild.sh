#!/bin/bash

STATEMENTS="statement-bank.txt statement-visa.txt"

for rulefile in rules*.yaml
do
    base=$(echo $rulefile | sed 's/rules/output/;s/.yaml//')
    TERM=ansi COLUMNS=48 luca tally -ct $rulefile $STATEMENTS > $base.txt
    (echo '<pre>';
        cat $base.txt | ansi2html -i;
        echo '</pre>') > $base.html
done
