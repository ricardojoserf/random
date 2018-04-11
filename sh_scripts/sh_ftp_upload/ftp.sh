#!/sh
HOST='66.220.9.50'
USER='ricardojoserf'
PASSWD='qweqweqwe'
FILE=$1

ftp -n $HOST <<END_SCRIPT
quote USER $USER
quote PASS $PASSWD
binary
cd test
put $FILE
quit
END_SCRIPT
exit 0
