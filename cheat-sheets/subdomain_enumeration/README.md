Oneliners

### IP,open_port1;open_port2;...

for i in $(cat /tmp/aaa); do res=$(nmap --top-ports 20 --open $i | grep open | cut -d "/" -f 1 | tr "\n" ";"); echo $i","$res; done | tee /tmp/www

for i in $(cat /tmp/aaa); do res=$(nmap --open $i | grep open | cut -d "/" -f 1 | tr "\n" ";"); echo $i","$res; done | tee /tmp/www


### IP,https:IP:8443 if 8443 open

port="443"; for i in $(cat /tmp/aaa); do res=$(nmap --open -p $port $i | grep open | cut -d " " -f 1 | cut -d "/" -f 1); if [ ! -z $res ]; then echo $i",https://"$i":"$port; else echo $i",No"; fi; done | tee /tmp/www

port="8443"; for i in $(cat /tmp/aaa); do res=$(nmap --open -p $port $i | grep open | cut -d " " -f 1 | cut -d "/" -f 1); if [ ! -z $res ]; then echo $i",https://"$i":"$port; else echo $i",No"; fi; done | tee /tmp/www

port="80"; for i in $(cat /tmp/aaa); do res=$(nmap --open -p $port $i | grep open | cut -d " " -f 1 | cut -d "/" -f 1); if [ ! -z $res ]; then echo $i",http://"$i":"$port; else echo $i",No"; fi; done | tee /tmp/www

port="8080"; for i in $(cat /tmp/aaa); do res=$(nmap --open -p $port $i | grep open | cut -d " " -f 1 | cut -d "/" -f 1); if [ ! -z $res ]; then echo $i",http://"$i":"$port; else echo $i",No"; fi; done | tee /tmp/www

