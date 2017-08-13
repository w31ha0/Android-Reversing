import sys,os

dir_path = sys.argv[1]
latestId = 0
IdLimit = 245313/2/2/2/2/2/2/2/2/2
record = {}
f = open('out.xgmml','w')

NODE_GRAPHICS = '<graphics type="ELLIPSE" h="40.0" w="40.0" width="3" fill="#ff0000" outline="#000000">\n</graphics>\n'
EDGE_GRAPHICS = '<graphics width="2" fill="#0000e1">\n</graphics>\n'

def parseContent(content):
    global record,latestId,f
    methodName = "unknown"
    classname = ""
    srcId = -1

    for line in content:
        if ".class" in line:
            classname = line.split(' ')[-1].strip()
        if ".method" in line:
            array = line.split(' ')
            for part in array:
                if "(" in part and ")" in part:
                    methodName = part.strip().replace('<','').replace('>','')
                    methodName = classname+"-"+methodName
                    record[methodName] = latestId
                    f.write('<node id="'+str(latestId)+'" label="'+methodName+'">\n')
                    f.write(NODE_GRAPHICS)
                    f.write('</node>\n')
                    srcId = latestId
                    #print "Recorded method " + methodName + " as node " + str(latestId)
                    latestId += 1
        elif ".end method" in line:
          methodName = "unknown"
        if methodName != "unknown":
            if "invoke" in line:
                invokedMethod = line.split(' ')[-1].strip().replace('<','').replace('>','')
                try:
                    destId = record[invokedMethod]
                except KeyError:
                    record[invokedMethod] = latestId
                    destId = latestId
                    f.write('<node id="'+str(latestId)+'" label="'+invokedMethod+'">\n')
                    f.write(NODE_GRAPHICS)
                    f.write('</node>\n')
                    #print "Recorded method " + invokedMethod + " as node " + str(latestId)
                    latestId += 1
                #print str(srcId)
                f.write('<edge id="'+str(latestId)+'" label="'+methodName+'  '+invokedMethod+'" source="'+str(srcId)+'" target="'+str(destId)+'">\n')
                f.write(EDGE_GRAPHICS)
                f.write('</edge>\n')
                #print "Recorded method invokation from " + methodName + " to "+invokedMethod+" as edge " + str(latestId)
                latestId += 1
            
            
f.write("<?xml version='1.0'?>\n")
f.write('<graph label="Androguard XGMML AnserverBot-001fa1574a73e9a8481e26df2aa6104eb2406b57.apk" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ns1="http://www.w3.org/1999/xlink" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns="http://www.cs.rpi.edu/XGMML" directed="1">\n')                
        
for path, subdirs, files in os.walk(dir_path):
    for name in files:
        #if latestId > IdLimit:
         #   break
        if name.endswith('smali') and "$" not in name:
            fullpath = os.path.join(path, name)
            content = open(fullpath,'r').readlines()
            parseContent(content)
            
print "latest id is " + str(latestId)
f.write('</graph>')            
f.close()