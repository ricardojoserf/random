#!/bin/bash

while IFS='' read -r line || [[ -n "$line" ]]; do
	unrar e flag.rar p $line
done < "$1"
