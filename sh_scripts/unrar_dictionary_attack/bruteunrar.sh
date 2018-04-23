#!/bin/bash

while IFS='' read -r line || [[ -n "$line" ]]; do
	unrar e $1 p $line > /dev/null 2>&1
done < "$2"
