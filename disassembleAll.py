import os,sys

apk = sys.argv[1]
app_name = apk.split('.')[0]

os.system('java -jar apktool_2.2.3.jar d '+apk+' -f')
os.system('unzip '+apk+' -d temp')
os.system('cd dex2jar-2.0 && d2j-dex2jar.bat ../temp/classes.dex -o temp1.jar --force && cd ..')
os.system('cd dex2jar-2.0 && d2j-dex2jar.bat ../temp/classes2.dex -o temp2.jar --force && cd ..')
os.system('java -Xms1024m -jar cfr_0_122.jar dex2jar-2.0/temp1.jar --outputdir '+app_name+'/java')
os.system('java -Xms1024m -jar cfr_0_122.jar dex2jar-2.0/temp2.jar --outputdir '+app_name+'/java')
os.system('rmdir /s /q temp')


