## URLS

cat a | grep -Eo "(http|https)://[a-zA-Z0-9./?=_-]*" | sort -u

cat a | grep -Eo "(http|https)://[a-zA-Z0-9./?=_-]*" | tr '[:upper:]' '[:lower:]' | sort -u

## All to lowercase

cat a | tr '[:upper:]' '[:lower:]'


## Gobuster

gobuster dir -r -k -u URL -w ../dict/content_discovery_all.txt --wildcard
