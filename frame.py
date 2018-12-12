import wget
import gzip
import subprocess
import os
import glob
import sqlite3
import pandas as pd
from pandas import DataFrame as df
import io
import time

class Phenotype:
	def __init__(self, rowlist, snipit):
		self.snipit = snipit
		self.rowlist = rowlist
		self.phenocode = self.rowlist[0]
		self.pheno_desc = self.rowlist[1]
		self.sex = self.rowlist[3]
		self.filename = self.rowlist[4]
		self.savename = self.filename.split(".bgz")[0]
		self.wget = self.rowlist[5]
		self.header = []
		Phenotype.download(self)


	def calc(self):
		start = time.time()
		df = pd.read_csv(io.StringIO('\n'.join(self.data)), delim_whitespace=True)
		where = df.loc[df["variant"].isin(self.snipit)]
		print(where)
		end = time.time()
		print("PANDAS ANALYZE TOOK:")
		print(end - start)
		where.to_csv(self.savename, sep='\t', encoding='utf-8')
		os.remove(self.filename)

	def gzip(self):
		with gzip.open(self.filename, "rt") as f:
			filecontent = f.read()
		self.data = filecontent.split("\n")
		print(self.filename + " SAVED TO MEMORY")

	def download(self):
		#filet = glob.glob("*.bgz")
		#filet = [x for x in filet if self.filename in x]
		#if filet:
			#return
		filet = glob.glob("*.tsv")
		filet = [x for x in filet if self.savename in x]
		if filet:
			return
		else:
			os.system(self.wget)
			Phenotype.gzip(self)
			Phenotype.calc(self)

q = open("index_snps_500kB_mafsub.txt", "r")
q = q.read()
snipit = q.split("\n")
snipit = list(map(lambda x: x.replace("chr", ""), snipit))


f = open("UKBB GWAS Imputed v3 - File Manifest Release 20180731 - Manifest 201807.tsv", "r")
f = f.read()
f = f.split("\n")

dis_len = len(f)



while dis_len - 1 > 10: 
	print(f[dis_len-1])
	rows = f[dis_len-1].split("\t")
	obj = Phenotype(rows,snipit)
	del obj
	ww = open("frame_tehty.txt", "a")
	ww.write(str(dis_len))
	ww.write("\n")
	ww.close()
	dis_len -= 1
