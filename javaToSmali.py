import os,sys

input = sys.argv[1]
classname = input.split('.')[0]

os.system('javac '+input)
os.system('dx --dex --output=classes.dex '+classname+'.class')
os.system('java -jar baksmali.jar d classes.dex')
os.system('del /f classes.dex')
os.system('del /f '+classname+'.class')