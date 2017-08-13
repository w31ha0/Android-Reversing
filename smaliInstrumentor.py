import os,sys,re

def getAllRegisters(methodContents,methodName):
	regex = "[v|p]\d"
	regex2 = "[v|p]\d\d"
	matches = []
	for line in methodContents:
		results = re.findall(regex, line)
		for result in results:
			if result not in matches:
				matches.append(result)		
		results = re.findall(regex2, line)
		for result in results:
			if result not in matches:
				matches.append(result)	
	return matches
		
relative_path = sys.argv[1]
dir_path = os.path.dirname(os.path.realpath(__file__)) + "/" + relative_path
filesToInstrument = ["NetworkUtils.smali"]
tempFilestoInstrument = ["SystemKeyStore.smali","PinningTrustManager.smali","CertificateChainCleaner.smali","Security.smali","CertificatePinner.smali","XMPPTCPConnection.smali",
"StageDetectionUtil.smali","zzh.smali","zzaue.smali","RealConnection.smali","TrustRootIndex.smali","OkHostnameVerifier.smali","OkHttpClient.smali","zzd.smali","AndroidPlatform.smali",
"Platform.smali","BasicCertificateChainCleaner.smali","TLSUtils$AcceptAllTrustManager.smali","TrustRootIndex$AndroidTrustRootIndex.smali","TrustRootIndex$BasicTrustRootIndex.smali","AndroidPlatform$AndroidCertificateChainCleaner.smali"]

def searchForRegistersToUse(registers):
	toUse = []
	for i in range(0,15):
		register = "v"+str(i)
		if register not in registers:
			toUse.append(register)
			if len(toUse) >= 2:
				return toUse
	return None

def getTotalNumberOfRegisters(registers):
	highestV = -1
	highestP = -1
	for register in registers:
		type = register[0]
		if type == "v":
			index = int(register[1:])
			if index > highestV:
				highestV = index
		elif type == "p":
			index = int(register[1:])
			if index > highestP:
				highestP = index
				
	if highestP == -1:
		highestP = 0
	else:
		highestP = highestP + 1
	if highestV == -1:
		highestV = 0
	else:
		highestV = highestV + 1	
				
	return highestP + highestV

for path, subdirs, files in os.walk(dir_path):
		for name in files:
			if name.endswith('smali') and name in filesToInstrument:
				fullpath = os.path.join(path, name)
				fd = open(fullpath,'r+')
				content = fd.readlines()
				newContent = content[:]
				lineNo = 1
				methodStart = False
				methodContents = []
				methodName = ""
				startline = 0
				for line in content:
					if ".method" in line:
						methodStart = True
						methodName = "unknown"
						array = line.split(' ')
						for part in array:
							if "(" in part and ")" in part:
								methodName = part.strip()
						startline = lineNo
					elif ".end method" in line:
						methodStart = False
						registers = getAllRegisters(methodContents,methodName)
						methodContents = []
						noOfRegisters = getTotalNumberOfRegisters(registers)
						if "scrollIfNecessary" in methodName:
							print str(noOfRegisters) + " registers for " + methodName + str(registers)
						if noOfRegisters > 14:
							print "Skipping " + methodName + " due to insufficient registers"
						elif "locals" in newContent[startline]:
							oldNumberOfRegisters = newContent[startline].split(' ')[-1].strip()
							if oldNumberOfRegisters.isdigit():
								oldNumberOfRegisters = int(oldNumberOfRegisters)
								newContent[startline] = "\t.locals " + str(oldNumberOfRegisters+2)
								registersToUse = searchForRegistersToUse(registers)
								register1 = registersToUse[0]
								register2 = registersToUse[1]
								str1 = 	"\tsget-object " + register1 + ", Ljava/lang/System;->out:Ljava/io/PrintStream;"
								str2 =  '\tconst-string ' + register2 + ', "<'+name+'>Trace:Calling ' + methodName + '"'
								str3 = "\tinvoke-virtual {" + register1 + ", " + register2 + "}, Ljava/io/PrintStream;->println(Ljava/lang/String;)V"			
								newContent.insert(startline+1,"\n")
								newContent.insert(startline+2,str1)
								newContent.insert(startline+3,"\n\n")		
								newContent.insert(startline+4,str2)
								newContent.insert(startline+5,"\n\n")
								newContent.insert(startline+6,str3)
								newContent.insert(startline+7,"\n")
								lineNo += 7
					elif methodStart == True:
						methodContents.append(line)
					lineNo += 1
				fd.seek(0)
				fd.writelines(newContent)
				fd.close()
					
						