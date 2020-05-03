#need to add in the record deletion option

import tkinter as tk
import sqlite3

class Mainclass(tk.Tk):
    
    def __init__(self, *args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        container = tk.Frame(self)
        #the container itself needs to packed on to the main window.
        container.pack()
        self.frames = {}
        
        #pack the dictionary of frames into the container
        #for F in (maindatabasegui):
        #in passing the container and the root as parent and controller, 
        #we create a new instance by the name frame.
        #for F in (maindatabasegui,editpage):
        frame = maindatabasegui(container, self)
            #makes maindatabasegui into a type and not class
            #this frame is then stored in the self.frames dictionary
        self.frames[maindatabasegui] = frame
        frame.grid(row = 0,column = 1,sticky = 'nsew')
        
        #calling upon another class(instatiating another object by calling this class)
        self.show_frame(maindatabasegui)
    
    def show_frame(self,page):
        frame = self.frames[page]
        frame.tkraise()
    
    #note that parent is the container here. As we are passing container in the name of 
    #parent to the maindatebasegui, we can only use this name as parent.
    def show_editpage(self,editpage,parent):
        editpageframe  = editpage(parent,self)
        self.frames[editpage] = editpageframe
        editpageframe.grid(row = 0, column = 1, sticky = 'nsew')
        editpageframe.tkraise()
        
        
    def get_frame(self,page):
        return self.frames[page]
        

class maindatabasegui(tk.Frame):
    #parent is the widget which acts as the parent of the current object.
    #common point of interaction for several pages of widgets. It is an attempt to decouple the pages. 
    #That is to say, each page doesn't need to know about the other pages. 
    #If it wants to interact with another page, such as causing it to be visible, 
    #it can ask the controller to make it visible.
    #parent is the container that we pass in and controller is the root (or the main class)
    def __init__(self, parent,controller):
        tk.Frame.__init__(self, parent)
        #self.geometry("500x500")
        self.controller = controller
        controller.title('Database Entry')
       
        #list of labels to be made
        self.labels = [('fnamelabel',2,'First Name'),('lnamelabel',4,'Last Name'), \
                       ('addresslabel',6,'Address'),('citylabel',8,'City'),\
                       ('joblabel',10,'Occupation')]
        #list of entry to be made
        self.entrys = [('fnamelabel',2),('lnamelabel',4), \
                       ('addresslabel',6),('citylabel',8),\
                       ('joblabel',10)]
        
        for group in self.labels:
            self.labelmaker(group[0],group[2],group[1])
        
        for group in self.entrys:
            self.entrymaker(group[0],group[1])
        
        #variable for dropdown menu
        self.selectedrecord = tk.StringVar()
        
        self.addbutton = tk.Button(self, padx = 10, pady = 10, width = 30, relief = 'raised', command = lambda: self.addrecord())
        self.addbutton.config(text = 'Add Record')
        self.addbutton.grid(row = 12, column = 1, columnspan = 2)
        
        self.viewbutton = tk.Button(self, padx = 10, pady = 10, width = 30, relief = 'raised',command = lambda:self.viewrecord())
        self.viewbutton.config(text = 'View Record')
        self.viewbutton.grid(row = 14, column = 1, columnspan = 2)
        
        self.deletebutton = tk.Button(self,padx = 10,  pady = 10, width = 30, relief = 'raised', command = lambda: self.deleterecord())
        self.deletebutton.config(text = 'Delete Record')
        self.deletebutton.grid(row = 16, column = 1, columnspan = 2)
        
        self.editbutton = tk.Button(self,padx = 10, pady = 10, width = 30, relief = 'raised', command = lambda: controller.show_editpage(editpage,parent))
        self.editbutton.config(text = 'Edit Existing Record')
        self.editbutton.grid(row = 18, column = 1, columnspan = 2)
        
        self.statuslabel = tk.Label(self,  padx = 10, pady = 10, width = 30, relief = 'raised')
        self.statuslabel.grid(row = 20, column = 1, columnspan = 2)
        
        #list is not specified initially(notice that you can just mention the variable, without the default and list of options)
        noticelabel = tk.Label(self,text = 'Select record to View, Delete or Update',padx = 10, pady = 10, width = 30)
        noticelabel.grid(row = 1, column = 3, padx = 10)
        
        self.addedrecords =  tk.OptionMenu(self, self.selectedrecord,self.selectedrecord.set('Select Record'),())
        self.addedrecords.grid(row = 2, column = 3, padx = 10)
        
        #message widget
        self.viewspace = tk.Message(self,text = 'Record Details',relief = 'sunken') 
        self.viewspace.grid(row = 4, column = 3, padx = 10)            
        #SQL Section
        self.conn = sqlite3.connect('addressbookdb.sqlite')
        self.curs = self.conn.cursor()
        
        self.curs.execute('''CREATE TABLE IF NOT EXISTS Addresses (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            first_name TEXT,
            last_name TEXT, 
            address TEXT,
            city TEXT, 
            job TEXT)''')
        
        rows = self.curs.execute('''SELECT first_name, last_name FROM Addresses''')
        if rows is not None:
            menu = self.addedrecords['menu']
            menu.delete(0,'end')
            for row in rows:
                #row is a tuple
                name = row[0] + ' ' + row[1]
                menu.add_command(label = name , command = lambda value = name: self.selectedrecord.set(value))
                
            
            
        self.conn.commit()
        self.conn.close()
           

     #instead of repeating the code, we created a list with tuples
     #and assigned the string attribute name with the object
     #these attributes still belong to the self object
    def labelmaker(self,labelname,textval, rowpos,*args):
        setattr(self,labelname,tk.Label(self, text = textval,anchor = 'w',width = 10))
        getattr(self,labelname).grid(row = rowpos, column = 1, pady = 10, padx = 10)
        
    def entrymaker(self,entryname,rowpos,*args):
        setattr(self, entryname,tk.Entry(self,width = 20, borderwidth = 5))
        getattr(self,entryname).grid(row = rowpos, column = 2, pady = 10, padx = 10)
        
    def addrecord(self):
        #gets all the fields from the entry boxes
        firstname = self.fnamelabel.get()
        lastname = self.lnamelabel.get()
        address = self.addresslabel.get()
        city = self.citylabel.get()
        job = self.joblabel.get()
        
        #creates a list of all the entries and checks if any are empty
        comparelist = [firstname, lastname, address, city, job]
        pos = [i for i, f in enumerate(comparelist) if len(f) < 1]
        
        #adds data if all fields are not empty
        #else tells user
        if len(pos) > 0 :
            self.statuslabel.grid_forget()
            self.statuslabel.config(text = 'Please fill in all the required fields')
            self.statuslabel.grid(row = 18, column = 1, columnspan = 2)
        else:
            #this is only used to collect the names to be added
            #name = str(firstname) + ' ' + str(lastname)
            
            #dynamically adding the records into the dropdown menu
            #menu = self.addedrecords['menu']
            #menu.add_command(label = name, command = lambda value = name: self.selectedrecord.set(value))
                
            #SQL section    
            self.conn = sqlite3.connect('addressbookdb.sqlite')
            self.curs = self.conn.cursor()
            
            self.curs.execute('''INSERT INTO Addresses 
                              (first_name, last_name, address,city,job) 
                              VALUES (?,?,?,?,?)''',(firstname,lastname,address,city,job))
            
            id = self.curs.execute('''SELECT id FROM Addresses ORDER BY id DESC LIMIT 1''')
            idval = id.fetchone()
            self.conn.commit()
            
            entry = str(idval[0]) + ' ' + str(firstname) + ' ' + str(lastname)
            menu = self.addedrecords['menu']
            menu.add_command(label = entry, command = lambda value = entry: self.selectedrecord.set(value))
            self.statuslabel.grid_forget()
            self.statuslabel.config(text = 'Record Loaded')
            self.statuslabel.grid(row = 20, column = 1, columnspan = 2)
           
            
            self.conn.commit()
            self.conn.close()
            
            
    def deleterecord(self):
                
        self.conn = sqlite3.connect('addressbookdb.sqlite')
        self.curs = self.conn.cursor()
        self.curs.execute('''DELETE FROM Addresses WHERE 
                              first_name = ? AND last_name = ?''',(self.selectedrecord.get().split()[0],self.selectedrecord.get().split()[1]))
       
        menu = self.addedrecords['menu']
        menu.delete(self.selectedrecord.get())
        self.selectedrecord.set('Select Record')
        
        self.statuslabel.grid_forget()
        self.statuslabel.config(text = 'Record Deleted')
        self.statuslabel.grid(row = 18, column = 1, columnspan = 2)
            
        self.conn.commit()
        self.conn.close()
        
        self.viewspace.config(text = 'Record Details')
        #clearing the view space after deleting
    
    def viewrecord(self):
        self.conn = sqlite3.connect('addressbookdb.sqlite')
        self.curs = self.conn.cursor()
        row = self.curs.execute('''SELECT * FROM Addresses WHERE first_name = ? AND last_name = ?''',(self.selectedrecord.get().split()[0],self.selectedrecord.get().split()[1]))
        
        element = row.fetchone()
        
        self.viewspace.config(text = 'Record Details: \n ID = {} \n First Name = {} \n Last Name = {} \n Address = {} \n City = {} \n Occupation = {}'.format(\
                              element[0],element[1],element[2],element[3],element[4],element[5]))
            
        self.conn.commit()
        self.conn.close()

class editpage(tk.Frame):
    
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        #INCLUDE THE SITUATION WHERE RECORD IS NOT AVAILABLE
        self.controller = controller
        #list of labels to be made
        
        #connects with the other frame (maindatabasegui) and obtains the selected record
        maindbpage = self.controller.get_frame(maindatabasegui)
        selectedrec = maindbpage.selectedrecord.get()
        
        self.labels = [('fnamelabel',2,'First Name'),('lnamelabel',4,'Last Name'), \
                       ('addresslabel',6,'Address'),('citylabel',8,'City'),\
                       ('joblabel',10,'Occupation')]
        #list of entry to be made
        self.entrys = [('fnamelabel',2),('lnamelabel',4), \
                       ('addresslabel',6),('citylabel',8),\
                       ('joblabel',10)]
        
        for group in self.labels:
            self.labelmaker(group[0],group[2],group[1])
        
        for group in self.entrys:
            self.entrymaker(group[0],group[1])
            
        self.returnbutton = tk.Button(self,text = 'Return to main page',relief = 'raised',anchor = 'e', command = lambda: controller.show_frame(maindatabasegui))
        self.returnbutton.grid(row = 2, column = 3, columnspan = 1)
        
        self.editpgviewspace =  tk.Message(self,relief = 'sunken') 
        self.editpgviewspace.grid(row = 4, column = 3, padx = 10) 
        
        self.statuslabel = tk.Label(self,relief = 'raised',width = 12)
        self.statuslabel.grid(row = 14, column = 1, columnspan = 2 )
        
        self.updatebutton = tk.Button(self, text = 'Update Record', relief = 'raised', command = lambda: self.updaterecord(selectedrec))
        self.updatebutton.grid(row = 12, column = 1, columnspan = 2)
        
        #accessing SQL database
        if selectedrec == 'Select Record':
            self.editpgviewspace.config(text = 'Please select a record to edit from the previous page')
        else:
            self.conn = sqlite3.connect('addressbookdb.sqlite')
            self.curs = self.conn.cursor()
            elementrow = self.curs.execute('''SELECT * From Addresses WHERE first_name = ? AND last_name = ?''',(selectedrec.split()[0],selectedrec.split()[1]))
            element = elementrow.fetchone()
            #should be displayed only when record exists
            self.editpgviewspace.config(text = 'Record Details: \n ID = {} \n First Name = {} \n Last Name = {} \n Address = {} \n City = {} \n Occupation = {}'.format(\
                              element[0],element[1],element[2],element[3],element[4],element[5]))
            self.conn.commit()
            self.conn.close()
            
    
    def labelmaker(self,attribname,disptext,rowpos):
        setattr(self,attribname,tk.Label(self,text = disptext,relief = 'raised',anchor = 'w',width = 10))
        getattr(self,attribname).grid(row = rowpos, column = 1, pady = 10, padx = 10)
        
    def entrymaker(self,attribname,rowpos):
        setattr(self, attribname,tk.Entry(self,width = 20, borderwidth = 5))
        getattr(self,attribname).grid(row = rowpos, column = 2, pady = 10, padx = 10)
        
    def updaterecord(self,selectedrec):
        
        firstname = self.fnamelabel.get()
        lastname = self.lnamelabel.get()
        address = self.addresslabel.get()
        city = self.citylabel.get()
        job = self.joblabel.get()
        
        comparelist = [firstname, lastname, address, city, job]
        pos = [i for i, f in enumerate(comparelist) if len(f) < 1]
        
        if len(pos) > 0 :
            self.statuslabel.grid_forget()
            self.statuslabel.config(text = 'Please fill in all the required fields')
            self.statuslabel.grid(row = 14, column = 1, columnspan = 2) 
        else:
            self.conn = sqlite3.connect('addressbookdb.sqlite')
            self.curs = self.conn.cursor()
            self.curs.execute('''UPDATE Addresses SET
                                         first_name = ?,
                                         last_name = ?,
                                         address = ?,
                                         city = ?,
                                         job = ? WHERE
                                         first_name = ? AND last_name = ?''',(firstname,lastname,address,city,job,selectedrec.split()[0],selectedrec.split()[1]))
            self.conn.commit()
            self.conn.close()
        
        return
    
        
        
        

        







root = Mainclass()
root.mainloop()