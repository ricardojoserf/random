#!/sh

filename="a.txt"
m1=$(md5sum $filename)

while true; do
	sleep 1
	m2=$(md5sum $filename)
	if [ "$m1" != "$m2" ] ; then
		echo "ccc"
		exit 1
	fi
done
