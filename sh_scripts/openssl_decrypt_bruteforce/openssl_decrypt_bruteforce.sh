#!/sh

file="$1"
dictionary="$2"
cipher="$3"

if [ "$#" -ne 3 ]; then
	echo "Usage: \n\nsh aes_128_bruteforce.sh $file $dictionary $cipher \n\nExample: \n\nsh aes_128_bruteforce.sh text.enc rockyou.txt aes-128-cbc"
	exit 1
fi

echo "\nCracking file $file with dictionary $dictionary and cipher $cipher. \n\n"
while IFS='' read -r line || [[ -n "$line" ]]; do
	#echo "$line"
	error=$(openssl enc -d -$cipher -in "$file" -k "$line"  2>&1)
	if [ "$error" != "bad magic number" ]; then
		echo "$line"
		echo $error
	fi
done < "$dictionary"

