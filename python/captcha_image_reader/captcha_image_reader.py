import Image
import pytesseract
import sys

def check(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def main():
    text = pytesseract.image_to_string(Image.open(sys.argv[1]))
    if check(text):
    	print text
    else:
    	print "fail"

if __name__ == "__main__":
    main()


