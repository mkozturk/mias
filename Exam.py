#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xlrd

class Exampaper:
	
	def __init__(self, idnumber = "0", stdname = "name", examname = "TheExam", answers = [], keyslist = []):
		self.idnumber = idnumber
		self.stdname = stdname
		self.examname = examname
		self.answers = answers
		self.keyslist = keyslist
		self.evaluate()

	def getID(self):
		return self.idnumber
	
	def getName(self):
		return self.name
	
	def getAnswers(self):
		return self.answers
	
	def getKeys(self):
		return self.keyslist
	
	def evaluate(self):
		self.ncorrect = 0
		self.nwrong = 0
		self.nempty = 0
		assert(len(self.answers)==len(self.keyslist))
		for i in range(len(self.answers)):
			if self.answers[i] == "":
				self.nempty += 1
			elif self.answers[i] == self.keyslist[i]:
				self.ncorrect += 1
			else:
				self.nwrong += 1
	
	def __str__(self):
		s = self.idnumber + " "+ self.name + "\n"
		# Display empty answers as "_"
		answerstring =""
		for a in self.answers:
			if not a:
				answerstring += "_"
			else:
				answerstring += a
		s += answerstring + "\n"
		s += str(self.ncorrect) + " correct\n"
		s += str(self.nwrong) + " wrong\n"
		s += str(self.nempty) + " empty\n"
		return s
		

class Exam:
	def __init__(self, name = "", papers=[]):
		self.name = name # The name of the exam, e.g. "Reading A" or "IT 101 B"
		self.papers = papers # A list of Exampaper objects
	
	def __add__(self,other):
		return Exam(self.name + " and " + other.name, self.papers + other.papers)
	
	def parseFromExcel(self, filename, sheetindex=0, sheetname=None, columnlist=None):
		# Items are on columns.
		# If columnlist == None, all columns in file are taken as responses.
		# Otherwise, only specified columns are taken.
		# 
		# Row 1: The solution key.
		# Rows 2 and beyond: Student exam papers.
		#
		
		book = xlrd.open_workbook(filename)
		if sheetname == None:
			sheet = book.sheet_by_index(sheetindex)
		else:
			sheet = book.sheet_by_name(sheetname)
		self.name = sheet.name
		
		if columnlist==None:
			columnlist = range(sheet.ncols)
		
		# Get the solution key (a list of strings)
		solution_key = [sheet.cell_value(0,c) for c in columnlist]
		
		# Get student data
		self.papers = []
		for row in range(1, sheet.nrows):
			student_id = sheet.cell_value(row,0)
			student_name = sheet.cell_value(row,1)
			student_answers = [sheet.cell_value(row,c) for c in columnlist]
			# Replace empty strings with "_":
			student_answers = [a if a else "_" for a in student_answers]
			self.papers.append( Exampaper( student_id, student_name, self.name, student_answers, solution_key ) )
	
	def upperquartile(self):
		# Returns a list of Exampaper objects that are in the upper quartile of the exam.
		# Assumes score = ncorrect (for another formula, e.g. ncorrect - nwrong/4, modify the "key" function).
		papers_rev_sorted = sorted(self.papers, key=lambda p: p.ncorrect, reverse=True)
		n = len(self.papers)
		return papers_rev_sorted[:int(n/4)]
	
	def lowerquartile(self):
		# Returns a list of Exampaper objects that are in the lower quartile of the exam.
		# Assumes score = ncorrect (for another formula, e.g. ncorrect - nwrong/4, modify the "key" function).
		papers_sorted = sorted(self.papers, key=lambda p: p.ncorrect)
		n = len(self.papers)
		return papers_sorted[:int(n/4)]
	
	def parse_choices(self):
		# Returns a list of all choices in the exam, e.g., ["A","B","C","D"].
		# This can be used in displaying a table of response distributions.
		choicelist = []
		for p in self.papers:
			choicelist += p.answers + p.keyslist
			choicelist = list(set(choicelist))
		return choicelist
		 
	def distribution(self, item, papers=None):
		# Returns the distribution of choices for a given item (item: integer value between 0 and nquestions).
		# If papers is None, all papers are scanned. Otherwise, only the members of the given list is scanned.
		
		# Note that if "papers" has more than one booklet
		# (same questions with choices shuffled)
		# this metric becomes meaningless, unless choices are un-shuffled.
		count = {} # keys: choices; values: their count.
		if papers==None:
			papers = self.papers
		
		for p in papers:
			choice = p.answers[item]
			if choice not in count.keys():
				count[choice] = 1
			else:
				count[choice] += 1
		
		# Normalize
		total = sum(count.values())
		for c in count.keys():
			count[c] /= total
		return count
	
	def difficulty(self, item, papers=None):
		# Returns the difficulty index (% of correct answers) for an item.
		
		# Note that self.papers may have different solution keys
		# if they belong to different booklets. That's handled correctly.
		
		# Note: This is inefficient. "distribution" and "difficulty"
		# process the data repeatedly. Alternatively, store the data as
		# an object attribute and reuse.
		
		# If papers is None, scan all papers in the exam.
		if not papers:
			papers = self.papers
			
		count = 0
		for p in papers:
			if p.answers[item] == p.keyslist[item]:
				count += 1

		return count/len(papers)
	
	def discrimination(self, item):
		#Returns the Discrimination Index for a given item.
		uppers = self.upperquartile()
		lowers = self.lowerquartile()
		p_upper = self.difficulty(item, uppers)
		p_lower = self.difficulty(item, lowers)
		return p_upper - p_lower
	
	def distractor(self, item):
		# Distractor analysis.
		uppers = self.upperquartile()
		lowers = self.lowerquartile()
		return self.distribution(item, uppers), self.distribution(item, lowers)

def getSheetNames(filename):
	book = xlrd.open_workbook(filename)
	return book.sheet_names()

def main():

	listenA = Exam()
	listenA.parseFromExcel("sample.xlsx", sheetname="Listening A", columnlist=range(2,22))
	listenB = Exam()
	listenB.parseFromExcel("sample.xlsx", sheetindex=1, columnlist=range(2,22))

	myExam = listenA + listenB
	
	# Display names of all students in the upper quartile
	for s in myExam.upperquartile():
		print(s.stdname)
	
	print(myExam.parse_choices())

if __name__ == '__main__':
	main()

