#!/sh


loop(){
for f in $1/*; do
	#echo $f
	if [ -d $f ]; then
		#echo "$f is a dir"
		loop $f
	else
		#echo "$f is not a dir"
		#echo "$f"
		echo "\n\nFile: $f\n"
	        exiftool $f
	        echo "\n\n"
	        echo "------------------------"
	fi
done
}

loop $1
