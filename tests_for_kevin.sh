#!/bin/bash
for dir in `ls server`
do
    for file in `ls server/$dir`
    do
        to_run=`echo "$file" | egrep -o "[^.]+_test\.py"`
        if [[ "$to_run" != "" ]]
        then
            pytest "server/$dir/$to_run"
        fi
    done
done
rm -r .pytest_cache
for dir in `ls server`
do
    if [[ "$dir" == "__pycache__" ]]
    then
        `rm -r server/$dir`
    fi
    for file in `ls server/$dir`
    do
        if [[ "$file" == "__pycache__" ]]
        then
            `rm -r server/$dir/$file`
        fi
    done
done