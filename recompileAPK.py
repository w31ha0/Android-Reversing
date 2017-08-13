import sys,os,time

name = sys.argv[1]
apkfile = name + ".apk"
package = ""

f = open(name+'/AndroidManifest.xml','r')
contents = f.readlines()[0].split(' ')
for line in contents:
	if "package" in line:
		package = line.split('=')[1].strip('" ')
		print "Found package " + package
		break
		
if package == "":
	print "Could not find package..Exiting"
	sys.exit(0)
	
os.system('cd '+name+' && rmdir /s /q dist')
os.system('cd '+name+' && rmdir /s /q build')
os.system('java -jar apktool_2.2.3.jar b '+name)
time.sleep(2)
os.system('apksigner sign --ks my-release-key.jks --ks-pass pass:123456 '+name+'/dist/'+apkfile)
os.system('adb uninstall '+package)
os.system('adb install '+name+'/dist/'+apkfile)
os.system('adb shell monkey -p '+package+' -c android.intent.category.LAUNCHER 1')
