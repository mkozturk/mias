# mias
Meral's Item Analysis Software

A simple Python program with a Qt GUI to analyze multiple-choice exams and generate a report. Requires Python 3, PyQt4 and xlrd.

The exam results are read from an Excel file. A student's responses are listed on a single row. The first row must contain the solution key. There is no limit to the number of questions or to the number of students. Responses should be A,B,C,D,T,F or blank. The sheet may contain other columns such as name or ID; the user can specify which columns should be chosen for processing. Response columns should be contiguous.

The main program is MIAS_main.py. First choose the input Excel file. The sheets in the file are parsed and displayed as a tickbox list.

The "Generate Report" button analyzes the test and displays a report in another window. The report displays a table of the difficulty index and the discrimination index of each question (item). It also displays the distribution of responses for each item, for the upper quartile, lower quartile, and all students in that particular sheet.

The file may contain several sheets of related exams. The example file sample.xlsx has two exam forms, Reading and Listening, and four booklets of each. For example, "Listening A" to "Listening D" comprise the same questions in the same order, but choices are shuffled in each question. The report correctly evaluates the difficulty and discrimination index for several booklets of the same type (Listening or Reading), but it does not evaluate the distribution of responses as this is meaningless with shuffled choices. Also, combining different types of exams (e.g., Listening and Reading) gives meaningless results.

The report can be sent to a printer, or saved as a PDF file.
 
