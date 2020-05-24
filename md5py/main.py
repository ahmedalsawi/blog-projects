
import sys
import md5

def main():
       data = sys.argv[1]
       md5sum = md5.md5sum(data)
       print(md5sum)

if __name__ == "__main__":
    main()
