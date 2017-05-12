import os
files = os.listdir(".")

for filename in files:
    potion=os.path.splitext(filename)
    if portion[1]==".JPG":
        newname=portion[0]+".jpg"
        os.rename(filename,newname)
