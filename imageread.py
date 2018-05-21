from PIL import Image
from tesserocr import image_to_text,PSM
import pickle
import _thread
import operator

def splitImage(image):
	w,h=image.size
	im1=image.crop(box=(0,600,1*w/2,h-550))
	im2=image.crop(box=(0.96*w/2,600,w,h-550))
	return im1,im2

def splitLowResImage(image,odd):
	w,h=image.size
	if odd==1:
		f=0.95
	else:
		f=1
	im1=image.crop(box=(0,250,f*w/2,h-229))
	im2=image.crop(box=(f*w/2,250,w,h-229))
	return im1,im2

def textToDictTables(text):
	text=text.split('\n')
	word=''
	for j in range(len(text)):
		text[j]=text[j].strip()
		if text[j]!="":
			for i in range(len(text[j])):
				if text[j][i]=='T' and text[j][i+1].isdigit():
					print("{} {}-->{}".format(word,text[j][:i],text[j][i:]))
					word=''
					break
			'''
			if text[j][-1].isdigit():
				if j+1<len(text) and len(text[j+1])>=2 and text[j+1][0]=="T" and text[j+1][1].isdigit():
					for k in range(len(text[j])):
						if text[j][k].isdigit():
							word=text[j][:k]
							break
				#word=''
			else:
				word=''
				#word=word+' '+text[j]
			'''
			
	return {"1":1}

def textToDict(text):
	#print(text)
	for letter in text:
		if ord(letter)>127:
			text.replace(letter,'')
	text=text.split('\n')
	letter='A'
	for j in range(len(text)):
		line=text[j].strip()
		if line!="":
			letter=line[0]
			break
	word=""
	dicti={}
	dictt={}
	for j in range(len(text)):
		ff=0
		line=text[j].strip()
		#print(line)
		if line!="":
			#print(letter,line[0])
			#input()
			if len(line)==1:
				letter=line[0]
			else:
				if line[0]!=letter:
					line=word+' '+line
					ff=1
				flag=0	
				if line[:8]=="see also":
					continue
				for i in range(len(line)):
					if line[i]=="T" and line[i+1].isdigit():
						flag=1
						#print("{}-->{}".format(line[:i],line[i:]))
						w1=line[:i]
						n1=line[i:]
						w1=w1.strip()
						n1=n1.strip()
						dictt[w1]=n1
						break
					elif line[i].isdigit():
						w1=line[:i]
						n1=line[i:]
						w1=w1.strip()
						n1=n1.strip()
						dicti[w1]=n1
						flag=1
						if ff==0:
							word=w1
						break
				if flag==0:
					#word=word+' '+line
					word=line
		#print(word,letter)			
	

	for key in dicti:
		dicti[key]=dicti[key].replace(" ","")
		#print(key,dicti[key])
	for key in dictt:
		dictt[key]=dictt[key].replace(" ","")
		#print(key,dictt[key])
	return dicti,dictt

def imagetoDict(image,number):
	im1,im2=splitLowResImage(image,number%2)
	text1=image_to_text(im1,psm=PSM.SINGLE_BLOCK)
	text2=image_to_text(im2,psm=PSM.SINGLE_BLOCK)

	(d1,dt1),(d2,dt2)=textToDict(text1),textToDict(text2)
	d3=dict(d1)
	d3.update(d2)
	dt3=dict(dt1)
	dt3.update(dt2)
	return d3,dt3

def imagenumbertoDict(number):
	filename="data/deweydecimalcla04dewe_Page_"
	number=16+number
	if number<=99:
		st="0"+str(number)
	else:
		st=str(number)
	im=Image.open("{}{}.png".format(filename,st))
	return imagetoDict(im,number)

#[start,end]
def multipleimagestoDict(start,end):
	d={}
	dt={}
	for i in range(start,end+1):
		d1,dt1=imagenumbertoDict(i)
		d.update(d1)
		dt.update(dt1)
		print("Done page {}".format(i))
	return d,dt

#[start,end]
def multipleimagestoDictMultiThreaded(start,end):
	d={}
	for i in range(start,end+1):
		_thread.start_new_thread(imagenumbertoDict,(i,))
		#d.update(d1)
		print("Done page {}".format(i))
	return d

def getallimagesasDict():
	return multipleimagestoDict(1,726)

def convertDicttosaveableform(d):
	l=sorted(d["main"].items(),key=operator.itemgetter(1))
	t=d["tables"]
	k={}
	kk={}
	for i in range(1,8):
		k["{}".format(i)]=[]
	for key in t:
		d=t[key]
		d=''.join(g for g in d if g.isdigit())
		k[d[0]].append((key,d[1:]))
	for key in k:
		kk[key]=sorted(k[key],key=operator.itemgetter(1))
	ans={}
	ans["main"]=l
	ans["tables"]=kk
	return ans

def saveDictasFile(d):
	with open("DDC.pickle","wb") as f:
		pickle.dump(d,f)

def main():
	#saveDictasFile(getallimagesasDict())
	#k=imagenumbertoDictTables(25)
	k1,k2=getallimagesasDict()
	d={}
	d["main"]=k1
	d["tables"]=k2
	saveDictasFile(convertDicttosaveableform(d))
	'''
	for key in k1:
		print(key,k1[key])
	'''

if __name__=="__main__":
	main()