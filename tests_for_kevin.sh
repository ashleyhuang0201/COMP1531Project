#!/bin/bash
`alias pytest-3=pytest `
for dir in `ls server`
do
    for file in `ls server/$dir`
    do
        if [[ "$file" == "__pycache__" ]]
        then
            `rm -r $file`
        fi
        to_run=`echo "$file" | egrep -o "[^.]+_test\.py"`
        if [[ "$to_run" != "" ]]
        then
            pytest "server/$dir/$to_run"
        fi
    done
done