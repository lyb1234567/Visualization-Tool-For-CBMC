#!/bin/bash
rm *.c
for file in *
do
    if [[ -f $file && -x $file && $file != *.sh ]]; then
        echo "$file"
        if file "$file" | grep -q "executable"; then
            rm "$file"
        fi
    fi
done
