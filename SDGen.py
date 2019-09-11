import csv
from tkinter import *
from tkinter import messagebox
from random import sample

def mode(x):
	e1.delete(0, END)
	if x == "List of Donors":
		e1.insert(END, 'D1,D2,D3,D4,D5,D6,D7,D8')
	if x == "Number of Donors":
		e1.insert(END,'8')
	if x == "Desired number of Superdonors":
		e1.insert(END,'32')

#function choosePiece samples one bottle of the set of bottles with the
#maximum number of pieces, and takes one piece. The input takes a set of
#bootles L or R, and a subset of bottles to exclude from the sampling.
#The output is the piece label and the bottle index in the set of botles

def choosePiece(B, e):
	np = [len(x) if B.index(x) not in e else 0 for x in B];
	b = sample([i for i, j in enumerate(np) if j == max(np)],1)[0]
	p = B[b][0]
	return p, b

#the choosePiece function is used in a chain process to 
#sample always a different bottle (from different donors)

def superDonor(L, R):
	pl1, d1 = choosePiece(L, [])
	pl2, d2 = choosePiece(L, [d1])
	pr1, d3 = choosePiece(R, [d1,d2])
	pr2, d4 = choosePiece(R, [d1,d2,d3])
	L[d1].pop(0)
	L[d2].pop(0)
	R[d3].pop(0)
	R[d4].pop(0)	
	return [pl1,pl2,pr1,pr2]
	
def Run():
	#Number of pieces
	
	NP = int(e2.get())

	#Donors
	
	if variable.get() == "List of Donors":
		DONORS = e1.get().split(',')
		
	if variable.get() == "Number of Donors":
		ND = int(e1.get())
		DONORS = ['D'+str(i) for i in range(1,ND+1)]

	if variable.get() == "Desired number of Superdonors":
		NSD = int(e1.get())
		ND = int((NSD*4/(2*NP)))
		DONORS = ['D'+str(i) for i in range(1,ND+1)]
	
	#Because sometimes, although rarely, it happens that the sampling of 
	#pieces does not lead to a perfect mixture an IndexError may occur at 
	#the end. For that reason, the cern of the code will repeat whenever an 
	#Indexerror occurs.

	while True:

		#Left and right pad piece labels

		L = [[x]*NP for x in DONORS]
		R = [[x]*NP for x in DONORS]

		SD = []
		
		try:
			while sum([len(x) for x in L]) != 0:
				SD += [superDonor(L, R)]			

			break
		except IndexError:
			continue

	#Generate output file

	output = open(e3.get()+'.csv', mode='w')
	fieldnames = ['', 'L1', 'L2', 'R1','R2']
	writer = csv.DictWriter(output, fieldnames=fieldnames)
	writer.writeheader()  
	for i in range(0,len(SD)):
		writer = csv.DictWriter(output, fieldnames=fieldnames)
		writer.writerow({'': 'SD'+str(i+1), 'L1': SD[i][0], 'L2': SD[i][1], 'R1': SD[i][2], 'R2': SD[i][3]})

	messagebox.showinfo("SDGen", "The output file " + e3.get()+'.csv ' + "was generated at the SDGen script directory!")

#Dialog

master = Tk()
master.title("SDGen")

variable = StringVar(master)
variable.set(" Select input type")
w = OptionMenu(master, variable, "List of Donors", "Number of Donors", "Desired number of Superdonors", command=mode).grid(row=0, padx = 3, sticky="ew")

Label(master, text="Number of pieces to cut each pad into ").grid(row=1, padx = 3)
Label(master, text="Output file name ").grid(row=2, padx = 3)

e1 = Entry(master)
e2 = Entry(master)
e2.insert(END, '8')
e3 = Entry(master)
e3.insert(END, 'SD')

e1.grid(row=0, column=1, padx = 3, pady = 3)
e2.grid(row=1, column=1, padx = 3, pady = 3)
e3.grid(row=2, column=1, padx = 3, pady = 3)

Button(master, text='Quit', command=master.destroy).grid(row=4, column=0, pady = 8)
Button(master, text='Run', command=Run).grid(row=4, column=1, pady = 8)

mainloop()
