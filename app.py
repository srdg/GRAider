from tkinter import *
from tkinter import font
import shutil
import os, sys
import urllib.request
import requests

class downloadGradeCard():

	def __init__(self,master):
		'''
		initializes and sets up UI requires the user to mention 
		sem [SEM1 by default] and stream [CSE by default]
		'''
		master.geometry("400x300")
		master.title("GrAider")

		Label(master,text="\n\n").grid(row=1, column=2,sticky=W)

		Label(master,text="Choose stream : ").grid(row=1, column=3,sticky=E)
		self.stream = StringVar()
		STREAMS = ["CSE","ECE","IT","ME","CE","EE"]
		self.stream.set(STREAMS[0])
		OptionMenu(master, self.stream, *STREAMS).grid(row = 1,column = 4,sticky=E)

		Label(master,text="\n\nChoose semester : ").grid(row=2, column=3,sticky=E)
		self.sem = StringVar()
		SEMS = ["SEM1","SEM2","SEM3","SEM4","SEM5","SEM6", "SEM7", "SEM8"]
		self.sem.set(SEMS[0])
		OptionMenu(master, self.sem, *SEMS).grid(row = 2, column=4, sticky=E)

		Label(master,text="\n\nAdmission Year : ").grid(row=3, column=3,sticky=E)
		self.year = StringVar()
		YEARS = ["2013","2014","2015","2016","2017","2018"]
		self.year.set(YEARS[2])
		OptionMenu(master, self.year, *YEARS).grid(row = 3, column=4, sticky=E)

		Label(master,text="\n\nType of admission : ").grid(row=4, column=3,sticky=E)
		self.typeofstudent  = IntVar()
		Radiobutton(master, text="Regular", variable = self.typeofstudent, value=0).grid(row = 5, column = 3, sticky = E)
		Radiobutton(master, text="Lateral", variable = self.typeofstudent, value=1).grid(row = 5, column = 4, sticky = E)
		
		Label(master,text="\n\n\n").grid(row=6, column=3,sticky=W)

		download = Button(master, text="Start Now", command = self.startDownload)
		font_obj = font.Font(download,download.cget("font"))
		font_obj.configure(underline = True)
		download.configure(font=font_obj)
		download.grid(row = 6, column = 4, sticky = E)

	def startDownload(self):
		'''
		Generates the url by parsing arguments entered as inputs
		Retrieves the file using urlretrieve() [might be deprecated]
		Saves and stores the retrieved file to a local system folder
		'''
		endset = {'CSE': '40', 'ECE': '60', 'IT': '50', 'CE':'10','EE':'20','ME':'30'}
		_url = "http://jgec.ac.in/php/coe/results/"+self.sem.get()[3]+"/"+self.stream.get()+"_"+self.sem.get()+"_"
		preset = self.year.get()[-2:]
		roll = str(int(preset) -1*(self.typeofstudent.get()))+"10110"+endset[self.stream.get()]
		# create custom directory if not available
		if not os.path.exists(self.stream.get()+"_"+self.sem.get()+"_Results Stored Here"):
			os.makedirs(self.stream.get()+"_"+self.sem.get()+"_Results Stored Here")

		start,stop = 1,100
		for offset in range(start,stop):
			complete_url = _url+roll+"0"*(offset<10)+str(offset)+".pdf"
			print("Generating custom URL ... done.")
			response = requests.get(complete_url)
			with open(complete_url[36:], 'wb') as fw:
				fw.write(response.content)
			fw.close()
			shutil.move(complete_url[36:], os.getcwd()+"/"+self.stream.get()+"_"+self.sem.get()+"_Results Stored Here")
			print("Saving file "+complete_url[36:]+" .... done.")

			if offset==70:
				if self.typeofstudent.get()==1:
					roll = preset+"10110"+endset[self.stream.get()]
				else:
					roll = str(int(preset)+1)+"10110"+endset[self.stream.get()]
		
def main():
	root = Tk()
	downloaderObject = downloadGradeCard(root)
	root.mainloop()

if __name__=="__main__":
	main()