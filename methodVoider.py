import os,sys,re

relative_path = sys.argv[1]
dir_path = os.path.dirname(os.path.realpath(__file__)) + "/" + relative_path
filesToInstrument = ["AdUnitActivity.smali","AppLovinInterstitialActivity.smali"]

for path, subdirs, files in os.walk(dir_path):
        for name in files:
            if name.endswith('smali') and name in filesToInstrument:
                fullpath = os.path.join(path, name)
                fd = open(fullpath,'r+')
                content = fd.readlines()
                lineNo = 1
                for line in content:
                    if ".method" in line and line.strip()[-1] == 'V':
                        if content[lineNo] != "\treturn-void":
                            content.insert(lineNo,"\treturn-void\n")
                            print "Voided " + line
                        else:
                            print line+" already voided"
                    else:
                        print "Skipping "+line+" because its not a void method"
                    lineNo += 1   
                fd.seek(0)
                fd.writelines(content)
                fd.close()
                    
                        