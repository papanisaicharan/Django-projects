from tkinter import *
from tkinter import filedialog
import tkinter as tk
import openpyxl as xl
from os import listdir
import pandas as pd
from os.path import isfile, join

no_of_file = 0
filepaths = []
column_names_all = []
card_names = []

def openfile(text):
	# filez = filedialog.askopenfilenames(parent=root,title='Choose a file')
	# print(root.tk.splitlist(filez))
	print("opening files")
	filez = filedialog.askopenfilenames(parent=root,title='Choose a file')
	print(root.tk.splitlist(filez))
	deselect_file(text)
	text.insert(tk.END,"\n".join(filez))
	global filepaths
	filez = sorted(filez,key=lambda x: int(x.split("/")[-1].split("_")[0].split("-")[-1]))
	for i in filez:
		filepaths.append(i.strip())
	for i in filepaths:
		card_names.append(i.split("/")[-1].split("_")[0])



def deselect_file(text):
	global no_of_file
	global filepaths
	global column_names_all
	column_names_all.clear()
	no_of_file = 0
	filepaths.clear()
	text.delete(1.0,END)

def getColumnNamesFromAll():
	# files = text.get("1.0",'end-1c').strip().split("\n")
	print("getColumnNamesFromAll")
	popup = tk.Tk()
	popup.wm_title("Column names")
	global column_names_all
	for i in filepaths:
		df = pd.read_excel(i)
		# lowering and stripping column list
		for j in list(df.columns):
			if j.lower().strip() not in column_names_all:
				column_names_all.append(j.lower().strip())
	if len(column_names_all) == 0:
		label = tk.Label(popup, text="NO FIlES ARE SELECTED")
	else:
		label = tk.Label(popup, text=" | ".join(column_names_all))
	label.pack(side="top", fill="x", pady=10 ,padx=10)
	B1 = tk.Button(popup, text="Okay", command = popup.destroy,bg="red",fg="white")
	B1.pack(side="top", fill="x", pady=10,padx=10)
	popup.mainloop()


def countWorkbooks(text):
	popup = tk.Tk()
	popup.wm_title("Number of workbooks selected")
	print("Paths of workbooks selected")
	if len(text.get("1.0").strip()) == 0:
		label = tk.Label(popup, text="Number of workbooks selected: " + str(0))
		label.pack(side="top", fill="x", pady=10 ,padx=10)
	else:
		length = len(text.get("1.0",'end-1c').strip().split("\n"))
		print(length)
		label = tk.Label(popup, text="Number of workbooks selected: " + str(length))
		label.pack(side="top", fill="x", pady=10 ,padx=10)
	B1 = tk.Button(popup, text="Okay", command = popup.destroy,bg="red",fg="white")
	B1.pack(side="top", fill="x", pady=10,padx=10)
	popup.mainloop()

def countSheets(text):
	popup = tk.Tk()
	popup.wm_title("No of sheets in workbook")
	files = text.get("1.0",'end-1c').strip().split("\n")
	if  len(text.get("1.0").strip()) == 0:
		label = tk.Label(popup, text="No files selected")
		label.pack(side="top", fill="x", pady=10 ,padx=10)
	else:
		for i in range(len(files)):
			wb = xl.load_workbook(files[i])
			label = tk.Label(popup, text="No of sheets in file : "+ files[i].split("/")[-1] +" = "+ str(len(wb.sheetnames)))
			label.pack(side="top", fill="x", pady=10 ,padx=10)
	B1 = tk.Button(popup, text="Okay", command = popup.destroy,bg="red",fg="white")
	B1.pack(side="top", fill="x", pady=10,padx=10)
	popup.mainloop()


def getFileNames(text):
	popup = tk.Tk()
	popup.wm_title("File names")
	print("File name")
	files = text.get("1.0",'end-1c').strip().split("\n")
	if  len(text.get("1.0").strip()) == 0:
		label = tk.Label(popup, text="No files selected")
		label.pack(side="top", fill="x", pady=10 ,padx=10)
	else:
		for i in files:
			label = tk.Label(popup, text=i.split("/")[-1] +" , with card number  :  "+ i.split("/")[-1].split("_")[0])
			label.pack(side="top", fill="x", pady=10 ,padx=10)
	
	B1 = tk.Button(popup, text="Okay", command = popup.destroy,bg="red",fg="white")
	B1.pack(side="top", fill="x", pady=10,padx=10)
	popup.mainloop()


# def removecolumns():


# def removersacolumns():


def consolidate(column_names):
	column_names1 = []
	if column_names.get().strip() != "":
		column_names1 = list(column_names.get().strip().split(","))
	print(column_names1)
	popup = tk.Tk()
	popup.wm_title("Output")
	if len(filepaths) == 0 or len(column_names1) == 0:
		label = tk.Label(popup, text="No files selected or no input in input columns entry.")
		label.pack(side="top", fill="x", pady=10 ,padx=10)
		B1 = tk.Button(popup, text="Okay", command = popup.destroy,bg="red",fg="white")
		B1.pack(side="top", fill="x", pady=10,padx=10)
	else:
		dfs = []
		for i in filepaths:
			df = pd.read_excel(i)
			columns_list = [j.lower().strip() for j in list(df.columns) ]
			index_remove = [columns_list.index(j) for j in column_names1 if j in columns_list]
			df.drop(list(df.columns[index_remove]),axis = 1,inplace=True)
			dfs.append(df)

		try:
			with pd.ExcelWriter('output.xlsx', engine='xlsxwriter') as writer:
				for i in range(len(dfs)):
					print(card_names[i])
					dfs[i].to_excel(writer, sheet_name=card_names[i],index =False,startrow=1, header=False,engine='xlsxwriter')
					# Get the xlsxwriter workbook and worksheet objects.
					workbook  = writer.book
					worksheet = writer.sheets[card_names[i]]

					# Add a header format.
					header_format = workbook.add_format({
					    'bold': True,
					    'text_wrap': True,
					    'valign': 'top',
					    'fg_color': '#fabf8f',
					    'border': 1})

					# Write the column headers with the defined format.
					for col_num, value in enumerate(dfs[i].columns.values):
					    worksheet.write(0, col_num , value, header_format)

			# Close the Pandas Excel writer and output the Excel file.
			writer.save()
			label = tk.Label(popup, text="CONSOLIDATION SUCCESSFULLY,FILE CREATE WITH NAME : output.xlsx")
			label.pack(side="top", fill="x", pady=10 ,padx=10)
			B1 = tk.Button(popup, text="Okay", command = popup.destroy,bg="red",fg="white")
			B1.pack(side="top", fill="x", pady=10,padx=10)
		except:
			label = tk.Label(popup, text="output.xlsx is open or other error occurred, so please follow the steps:close it!")
			label.pack(side="top", fill="x", pady=10 ,padx=10)
			B1 = tk.Button(popup, text="Okay", command = popup.destroy,bg="red",fg="white")
			B1.pack(side="top", fill="x", pady=10,padx=10)
	popup.mainloop()


def rsaconsolidate():
	popup = tk.Tk()
	popup.wm_title("Output")
	dfs = []
	for i in filepaths:

		df = pd.read_excel(i) 
		columns_list = [j.lower().strip() for j in list(df.columns) ]
		#getting the index of link to requirements
		indexOf_link_to_requiremnts = -1
		if "link to requirements" in columns_list:
			indexOf_link_to_requiremnts = columns_list.index("link to requirements")
		# print(indexOf_link_to_requiremnts)
		list_columns_removal = []
		if len(columns_list) > indexOf_link_to_requiremnts:
			list_columns_removal = [j for j in range(indexOf_link_to_requiremnts+1,len(columns_list))]
		# print("*************************************************")
		# print("columns : ",columns_list)
		# print("columns to be removed : ",list_columns_removal)
		# print(list(df.columns[list_columns_removal]))
		#removing columns
		df.drop(list(df.columns[list_columns_removal]),axis = 1,inplace=True)
		# print(df.head(2))
		dfs.append(df)
		#print(df.columns)
		# print("*************************************************** ")

	if len(filepaths) == 0:
		label = tk.Label(popup, text="No files selected")
		label.pack(side="top", fill="x", pady=10 ,padx=10)
		B1 = tk.Button(popup, text="Okay", command = popup.destroy,bg="red",fg="white")
		B1.pack(side="top", fill="x", pady=10,padx=10)
	else:
		# https://xlsxwriter.readthedocs.io/example_pandas_header_format.html
		# https://xlsxwriter.readthedocs.io/example_pandas_header_format.html
		try:
			with pd.ExcelWriter('output.xlsx', engine='xlsxwriter') as writer:
				for i in range(len(dfs)):
					print(card_names[i])
					dfs[i].to_excel(writer, sheet_name=card_names[i],index =False,startrow=1, header=False,engine='xlsxwriter')
					# Get the xlsxwriter workbook and worksheet objects.
					workbook  = writer.book
					worksheet = writer.sheets[card_names[i]]

					# Add a header format.
					header_format = workbook.add_format({
					    'bold': True,
					    'text_wrap': True,
					    'valign': 'top',
					    'fg_color': '#fabf8f',
					    'border': 1})

					# Write the column headers with the defined format.
					for col_num, value in enumerate(dfs[i].columns.values):
					    worksheet.write(0, col_num , value, header_format)

			# Close the Pandas Excel writer and output the Excel file.
			writer.save()
			label = tk.Label(popup, text="CONSOLIDATION SUCCESSFULLY,FILE CREATE WITH NAME : output.xlsx")
			label.pack(side="top", fill="x", pady=10 ,padx=10)
			B1 = tk.Button(popup, text="Okay", command = popup.destroy,bg="red",fg="white")
			B1.pack(side="top", fill="x", pady=10,padx=10)
		except:
			label = tk.Label(popup, text="output.xlsx is open or other error occurred, so please follow the steps:close it!")
			label.pack(side="top", fill="x", pady=10 ,padx=10)
			B1 = tk.Button(popup, text="Okay", command = popup.destroy,bg="red",fg="white")
			B1.pack(side="top", fill="x", pady=10,padx=10)
	popup.mainloop()
	# print("***************** CONSOLIDATION SUCCESSFULLY,FILE CREATE WITH NAME "+filename+"*********************")


if __name__ == '__main__':
    root = tk.Tk()
    # heading
    w = tk.Label(root, text="Consolidation",fg = "red",font = "Times")
    w.pack(side=tk.TOP,expand=tk.YES,fill=tk.X,padx=5,pady=5)

    # filter
    row2 = tk.Frame(root)
    w = tk.Label(row2, text="Input the column names separated by commas  :",fg = "gray50",font = "Times")
    w.pack(side=tk.LEFT,fill=tk.X,padx=5,pady=5)
    column_names = tk.Entry(row2)
    column_names.pack(side=tk.RIGHT,expand=tk.YES,fill=tk.X,padx=5,pady=5)
    row2.pack(side=tk.TOP,expand=tk.YES,fill=tk.X,padx=5,pady=5)
    # row 3
    row3 = tk.Frame(root)
    # sidnav
    row1 = tk.Frame(row3)

    lab1 = tk.Button(row1,text="Click to open files",bg="gray50",fg="white",command= lambda:openfile(text1))
    lab2 = tk.Button(row1,text="deselect the files",bg="gray50",fg="white",command= lambda:deselect_file(text1))
    # add a vertical scroll bar to the text area
    lab1.pack(side=tk.TOP,fill='x', padx=5, pady=5)
    lab2.pack(side=tk.TOP,fill='x', padx=5, pady=5)
    # row last,frame last.
    b1 = tk.Button(row1, text='custum consolidate',bg="gray50",fg="white",
           command= lambda:consolidate(column_names))
    b1.pack(side=tk.TOP,fill='x',expand=tk.YES, padx=5, pady=5)
    b2 = tk.Button(row1, text='RSA_consolidate',bg="gray50",fg="white",
           command= lambda:rsaconsolidate())
    b2.pack(side=tk.TOP,fill='x',expand=tk.YES, padx=5, pady=5)

    b3 = tk.Button(row1,width="30",text='Quit',bg="gray50",fg="white", command=root.quit)
    b3.pack(side=tk.TOP,fill='x',expand=tk.YES,padx=5, pady=5)
    row1.pack(side=tk.LEFT,expand=tk.YES,fill=tk.X,padx=5,pady=5)

    text1 = Text(row3,height="20")
    scroll=Scrollbar(row3)
    text1.configure(yscrollcommand=scroll.set)
    #pack everything

    text1.pack(side=tk.LEFT,expand=tk.YES)
    scroll.pack(side=tk.RIGHT,fill=Y,expand=tk.YES)
    text1.pack(side=tk.RIGHT,expand=tk.YES)
    row3.pack(side=tk.TOP,expand=tk.YES,fill=tk.X,padx=5,pady=5)

    lastsecond = tk.Frame(root)
    count_workbooks = tk.Button(lastsecond,width="15",text='count_workbooks',bg="gray50",fg="white", command= lambda:countWorkbooks(text1))
    count_workbooks.pack(side=tk.LEFT,fill='x',expand=tk.YES,padx=5, pady=5)
    file_names = tk.Button(lastsecond,width="15",text='get file names',bg="gray50",fg="white", command= lambda:getFileNames(text1))
    file_names.pack(side=tk.LEFT,fill='x',expand=tk.YES,padx=5, pady=5)
    count_sheets = tk.Button(lastsecond,width="15",text='count_sheets',bg="gray50",fg="white", command= lambda:countSheets(text1))
    count_sheets.pack(side=tk.LEFT,fill='x',expand=tk.YES,padx=5, pady=5)
    columnNames = tk.Button(lastsecond,width="15",text='columnNames',bg="gray50",fg="white", command= lambda:getColumnNamesFromAll())
    columnNames.pack(side=tk.LEFT,fill='x',expand=tk.YES,padx=5, pady=5)
    lastsecond.pack(side=tk.TOP,expand=tk.YES,fill=tk.X,padx=5,pady=5)

    rowlast = tk.Frame(root)
    instr = tk.Label(rowlast, text="***Instructions***\n1.When using custom consolidate it is required to input in input section.\n2.When pressing quit,all the popups must be closed.\n3.If input xlsx file is not proper then sheet will be created with the name but no content will be loaded in it while consolidating.",fg = "red",font = "Times")
    instr.pack(side=tk.TOP,expand=tk.YES,fill=tk.X,padx=5,pady=5)
    rowlast.pack(side=tk.TOP,expand=tk.YES,fill=tk.X,padx=5,pady=5)
    
    root.mainloop()