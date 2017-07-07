#from sys import argv

with open("file.txt", "r") as ins:
    array = []
    for line in ins:
        array.append(line)
    print len(array)
