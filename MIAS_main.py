#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os, xlrd
from Exam import Exam
from PyQt4 import QtGui
from MIAS_UI import Ui_Dialog
from detailrep import Ui_DetailReportWindow

class Main(QtGui.QMainWindow):

	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)
		
		self.ui.btnOpen.clicked.connect(self.openfile)
		self.ui.btnQuit.clicked.connect(self.close)
		self.ui.btnFullReport.clicked.connect(self.full_report)
			
	def selectedsheets(self):
		sheets = []
		for s in self.checkboxes:
			if s[1].isChecked():
				sheets.append(s[0])
		return sheets
	
	def hyphen_range(self,s):
		""" Takes a range in form of "a-b" and generate a list of numbers between a and b inclusive.
		Also accepts comma separated ranges like "a-b,c-d,f" will build a list which will include
		Numbers from a to b, c to d and f"""
		s="".join(s.split())#removes white space
		r=set()
		for x in s.split(','):
			t=x.split('-')
			if len(t) not in [1,2]:
				raise SyntaxError("hash_range given as "+s+" incorrectly formatted.")
			r.add(int(t[0])) if len(t)==1 else r.update(set(range(int(t[0]),int(t[1])+1)))
		l=list(r)
		l.sort()
		return l

	def getparameters(self):
		# Get selected sheets
		sels = self.selectedsheets()
		
		# Verify that all selected sheets have the same
		# number of columns.
		temp = self.sheetdata[sels[0]][1] # number of cols on first sheet
		for c in sels[1:]:
			if self.sheetdata[c][1] != temp:
				raise ValueError
				return
		
		# Which columns contain the data?
		if self.ui.radColAll.isChecked():
			firstcol = 0
			lastcol = self.sheetdata[sels[0]][1]-1
		elif self.ui.radColRange.isChecked():
			firstcol = self.ui.spinColFrom.value()-1
			lastcol = self.ui.spinColTo.value()-1
		
		# Select the items to process
		if self.ui.radItemAll.isChecked():
			items = list(range(lastcol-firstcol))
		elif self.ui.radItemSingle.isChecked():
			items = [self.ui.spinItemSingle.value() - 1 ] # convert to 0-based from 1-based
		elif self.ui.radItemRange.isChecked():
			items = self.hyphen_range( self.ui.editItemRange.text() )
			items = [i-1 for i in items] # convert to 0-based from 1-based
		
		return sels, items,firstcol, lastcol

	def full_report(self):		
		# Get the selected parameters
		try:
			sels, items, firstcol, lastcol = self.getparameters()
		except ValueError:
			msgbox = QtGui.QMessageBox.warning(self, "Size mismatch",
				"Selected sheets do not have the same number of columns. Please check the input file.\n")
			return
		# Parse the grades from the Excel file
		# If more than one sheet selected, combine into one exam.
		myExam = Exam()
		myExam.parseFromExcel(self.ui.filename.text(), sheetname = sels[0], columnlist = [i+firstcol for i in items])
		for s in sels[1:]:
			e = Exam()
			e.parseFromExcel(self.ui.filename.text(), sheetname = s, columnlist = [i+firstcol for i in items])
			myExam += e
		# Generate the output HTML

		# Title
		output = "<h1>Item Analysis Report</h1>"
		output +='<h1>%s</h1>' % myExam.name
		
		# Display a table of items, their difficulty, and the discrimination index
		output += "<h2>Difficulty and discrimination indices</h2>"
		output += "<p>Note: Results are meaningless if you combine unrelated exam booklets (e.g., Listening and Reading).</p>"
		output += "<p>Difficulty index: % of correct answers.</p>"
		output += "<p>Discrimination index: (% correct by upper quartile students) - (% correct by lower quartile students).</p>"
		output += """<p><table border="1">
						<tr>
							<th></th>
							<th colspan="3">Difficulty index</th>
							<th rowspan="2">Discrimination index</th>
						</tr>
						<tr>
							<th>item #</th>
							<th>upper qt</th>
							<th>lower qt</th>
							<th>All</th>
						</tr>
					"""		
		uq = myExam.upperquartile()
		lq = myExam.lowerquartile()
		for i in items:
			diff = myExam.difficulty(i)
			diffuq = myExam.difficulty(i, uq)
			difflq = myExam.difficulty(i, lq)
			disc = myExam.discrimination(i)
			output += """<tr>
							<td>%d</td>
							<td>%.3f</td>
							<td>%.3f</td>
							<td>%.3f</td>
							<td>%.3f</td>
						</tr>""" % (i+1, diffuq, difflq, diff, disc)
		output += "</table></p>"
		
		# Display distribution of responses for upper quartile,
		# lower quartile, and all students.
		# Not applicable with more than one sheet (booklet).
		output += "<h2>Distribution of responses</h2>"
		if len(sels) == 1:
			responses = "_ABCDTF"
			soln = myExam.papers[0].keyslist
			output += "<p>Correct responses in boldface.</p>"
			output += """<p><table border="1">
							<tr>
								<th>item #</th>
								<th>  </th>"""
			for r in responses:
				if r == "_":
					output += "<th>Blank</th>"
				elif r == "T":
					output += "<th>True</th>"
				elif r == "F":
					output += "<th>False</th>"
				else:
					output += "<th>%s</th>" % r
			output += "</tr>"
			
			for i in items:
				d = myExam.distribution(i)
				du, dl = myExam.distractor(i)
				output += "<tr>"
				output += """<td>
								<table>
									<tr>
										<td></td>
									</tr>
									<tr>
										<td>%d</td>
									</tr>
									<tr>
										<td></td>
									</tr>
								</table>
							</td>""" % (i+1)
				output += """<td>
								<table>
									<tr>
										<td>upper qt</td>
									</tr>
									<tr>
										<td>lower qt</td>
									</tr>
									<tr>
										<td>all</td>
									</tr>
								</table>
							</td>"""
				for c in responses:
					if soln[i] == c: # correct solution in boldface
						output += """<td>
										<table>
											<tr>
												<td><b>%.3f</b></td>
											</tr>
											<tr>
												<td><b>%.3f</b></td>
											</tr>
											<tr>
												<td><b>%.3f</b></td>
											</tr>
										</table>
									</td>""" % (du.get(c,0.0), dl.get(c,0.0), d.get(c,0.0))
					else:
						output += """<td>
										<table>
											<tr>
												<td>%.3f</td>
											</tr>
											<tr>
												<td>%.3f</td>
											</tr>
											<tr>
												<td>%.3f</td>
											</tr>
										</table>
									</td>""" % (du.get(c,0.0), dl.get(c,0.0), d.get(c,0.0))
				output += "</tr>"
			output += "</table></p>"
		else:
			output += "<p>Not applicable when more than one booklet is selected.</p>"
		# Display the report on window
		self.repfull = DetailReportWindow()
		self.repfull.show()
		self.repfull.ui.textEdit.setHtml(output)
	
	def openfile(self):
		filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', os.getenv('.'), "Excel files (*.xlsx)")
		self.ui.filename.setText(filename)
		
		# get basic data about the sheets
		book = xlrd.open_workbook(filename)
		self.sheetdata = {} # keys: sheet name, values: (no. of rows, no. of columns)
		for n in book.sheet_names():
			self.sheetdata[n] = (book.sheet_by_name(n).nrows, book.sheet_by_name(n).ncols)
		
		self.ui.grpSheets.setEnabled(True)
		
		self.checkboxes = []
		for s in book.sheet_names():
			self.checkboxes.append( (s, QtGui.QCheckBox(s)) )
			self.ui.verticalLayout_3.addWidget(self.checkboxes[-1][1])

class DetailReportWindow(Main):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.ui = Ui_DetailReportWindow()
		self.ui.setupUi(self)
		self.ui.actionPrint.triggered.connect(self.sendtoprinter)	
	def sendtoprinter(self):
		dialog = QtGui.QPrintDialog()
		if dialog.exec_() == QtGui.QDialog.Accepted:
			self.ui.textEdit.document().print_(dialog.printer())

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
