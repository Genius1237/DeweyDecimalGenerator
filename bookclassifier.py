import imageread
import operator
import classifier_multi
import pickle
import bisect
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB

#Singleton Class
#Access only with getInstance()
class DDCClassifier(object):
	
	version=3
	ddcversion=3
	path="pickles/{}/".format(version)
	ddcpath="pickles/DDC/{}/".format(ddcversion)
	__instance__=None

	def getInstance():
		if DDCClassifier.__instance__ is None:
			DDCClassifier.__instance__=DDCClassifier()
		return DDCClassifier.__instance__

	def __init__(self):
		self.pickles={}
		self.d={}
		self.m=[]
		try:
			with open(DDCClassifier.path+"DDCClassifier.pickle","rb") as f:
				self.pickles=pickle.load(f)
		except:
			print("Training files missing or Need to Train")
		try:
			with open(self.ddcpath+"DDC.pickle","rb") as f:
				d2=pickle.load(f)
				d1=d2['main']
			self.d['main']=[]
			for k in d1:
				if DDCClassifier.isCode(k[1]) and len(k[1].replace('.',''))>=3:
					self.d['main'].append((k[0],k[1].replace('.','')))
			self.m=[k[1][:3] for k in self.d['main']]
			self.d['tables']=d2['tables']
		except:
			print("DDC index file missing")

	def gettablevalue(self,string,number):
		a=[]
		for n in ['1','2','3','4','5','6','7']:
			print(len(self.t["{}".format(n)]))
		#h=classifier_multi.trainandclassify(self.t["{}".format(number)])
		print(len(h))
		#return h.classify(classifier_multi.words_to_dict(classifier_multi.sentence_to_tokens(string)))

	def isCode(text):
		for letter in text:
			if not (letter.isdigit() or letter=='.'):
				return False
		return True

	def trainHundredsLevel(self):
		da=[]
		for i in range(len(self.d['main'])):
			da.append((self.d['main'][i][0],self.d['main'][i][1][0]))
		self.pickles["hundreds"]=classifier_multi.trainandclassify(da)
		#hundreds is an instance of NaiveBayesClassifier

	def trainTensLevel(self):
		da=[]
		for i in range(10):
			da.append([])
		for i in range(len(self.d['main'])):
			da[int(self.d['main'][i][1][0])].append((self.d['main'][i][0],self.d['main'][i][1][1]))
		self.pickles["tens"]=[]
		#tens is a list of NaiveBayesClassifier
		for i in range(10):
			self.pickles["tens"].append(classifier_multi.trainandclassify(da[i]))

	def trainUnitsLevel(self):
		da=[]
		for i in range(10):
			da.append([])
			for j in range(10):
				da[i].append([])
		for i in range(len(self.d['main'])):
			da[int(self.d['main'][i][1][0])][int(self.d['main'][i][1][1])].append((self.d['main'][i][0],self.d['main'][i][1][2]))
		
		for i in range(10):
			for j in range(10):
				if len(da[i][j])==0:
					da[i][j].append(('',''))
		
		self.pickles["units"]=[]
		#units is a list of list of NaiveBayesClassifier
		for i in range(10):
			self.pickles["units"].append([])
			for j in range(10):
				#print("{},{},{}".format(i,j,len(da[i][j])))
				#input()
				self.pickles["units"][i].append(classifier_multi.trainandclassify(da[i][j]))

	def trainTables(self):
		'''
		with open(DDCClassifier.ddcpath+"DDC.pickle","rb") as f:
			t=pickle.load(f)['tables']
		pickles={"tables":{}}
		print("1")
		for key in t:
			pickles["tables"][key]=classifier_multi.trainandclassify(t[key])
		print("2")
		with open("LOL.pickle","wb") as f:
			pickle.dump(pickles,format)
		'''
		t=self.d['tables']
		classifier={}
		for k in t:
			data=t[k]
			d=[]

			for s in data:
				l=classifier_multi.sentence_to_tokens(s[0])
				d.append((classifier_multi.words_to_dict(l),s[1]))
		
			n=len(d)
			sn=[]
			for i in range(n):
				sn.append((d[i][0],d[i][1]))

			classifier[k]=SklearnClassifier(MultinomialNB())
			classifier[k].train(sn)
		self.pickles['tables']=classifier

	def decimalFirstPart(self,h,t,u,d):
		s="{}{}{}".format(h,t,u)
		l=bisect.bisect_left(self.m,s)
		r=bisect.bisect_right(self.m,s)
		m=self.d['main'][l:r]
		#print(self.d['main'])
		c=classifier_multi.trainandclassify(m)
		p=c.prob_classify(d)
		
		return p.max()[3:]

	#If files are missing, need to train
	def train(self):
		#Lost around 2000 examples due to error in reading the DDC code as a code
		#Lost around 100 examples due to the DDC code not being greater than or equal to length 2(The dividing line being picked up as a 1)
		self.trainHundredsLevel()
		self.trainTensLevel()
		self.trainUnitsLevel()
		self.trainTables()
		self.save()

	def save(self):
		with open(self.path+"DDCClassifier.pickle","wb") as f:
			pickle.dump(self.pickles,f)


	def classify(self,s):
		d=classifier_multi.words_to_dict(classifier_multi.sentence_to_tokens(s))

		h=self.pickles["hundreds"].classify(d)
		t=self.pickles["tens"][int(h)].classify(d)
		u=self.pickles["units"][int(h)][int(t)].classify(d)
		d1=self.decimalFirstPart(h,t,u,d)

		if len(d1)==0:
			return "{}{}{}".format(h,t,u)
		else:
			return "{}{}{}.{}".format(h,t,u,d1)
		


def main():
	print("Loading")
	ddc=DDCClassifier.getInstance()
	#ddc.train()
	#exit()
	#'''
	print("Loading Done")
	#ddc.trainTables()
	while True:
		'''
		n=int(input())
		s=input()
		#print(ddc.gettablevalue(s,n))
		'''
		#'''
		print("Enter main topic of the book:",end=' ')
		try:
			s=input()
		except KeyboardInterrupt as e:
			exit()
		print(ddc.classify(s))
		#'''
	#'''
	

if __name__=="__main__":
	main()
'''
WORK REMAINING
INTEGRATE THE TABLES CLASSIFIER INTO THE OBJECT
CLEANUP
'''