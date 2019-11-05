## URLS

cat a | grep -Eo "(http|https)://[a-zA-Z0-9./?=_-]*" | sort -u

cat a | grep -Eo "(http|https)://[a-zA-Z0-9./?=_-]*" | tr '[:upper:]' '[:lower:]' | sort -u

## All to lowercase

cat a | tr '[:upper:]' '[:lower:]'
