from tkinter import *
from tkinter import messagebox
import time
from datetime import datetime
import random
import os
import sqlite3


def main_window():
    global window
    window = Tk()
    window.title('Main Window')
    window.config(bg='grey')
    Width = '1350'
    Height = '900'
    c = Canvas(window, height=Height, width=Width)
    c.pack()

    frame = Frame(window, bg='skyblue',relief=RAISED)
    frame.place(relx=0.05, rely=0.02, relwidth=0.9, relheight=0.85)

    conn = sqlite3.connect('pyzza.db')
    c = conn.cursor()
    #c.execute('''CREATE TABLE cashier(
    #            username text,
    #            passcode text)''')

    #c.execute('INSERT INTO cashier VALUES(:username, :passcode)',
    #            {
    #                'username': 'Aby',
    #                'passcode': 'aby'
    #            })


    #c.execute('''CREATE TABLE pizza(
    #            name text,
    #            price int)''')

    #c.execute('''CREATE TABLE drink(
    #            name text,
    #            price int)''')

    #c.execute('INSERT INTO pizza VALUES(:name, :price)',
    #            {
    #                'name': 'Kuku Tikka',
    #                'price': 150
    #            })

    #c.execute('INSERT INTO drink VALUES(:name, :price)',
    #            {
    #                'name': 'Vanilla',
    #                'price': 150
    #            })


    #c.execute('''CREATE TABLE sale(
    #            product_name text
    #            quantity int
                #cashier_id int
                #ForeignKey(cashier_id) Reference
    #            )''',

    conn.commit()
    conn.close()

    title_label = Label(frame, text='      DOT PYZZA MANAGEMENT SYSTEM    ', font=('COURIER', 40, 'bold'),bd=10, fg='cadet blue', bg='white',justify=CENTER, pady=30, padx=20)
    title_label.grid(row=0, columnspan=2)

    cashier_label = Label(frame, text=' CASHIER LOGIN ', font=('COURIER', 40, 'bold'),bd=10, fg='black', bg='skyblue', pady=30)
    cashier_label.grid(row=1, columnspan=2)


    cashier_id_label = Label(frame, text='Username', font=('COURIER', 30, 'bold'),bd=10,fg='black', bg='skyblue',justify=CENTER, pady=30, borderwidth=2)
    cashier_id_label.grid(row=2, column=0)

    #*******global*****************
    global cashier_id_entry
    global cashier_pass_entry
    global cashier_id_entry
    global cashier_pass_entry

    cashier_id_entry = Entry(frame, width=15, font=('ARIAL',25,'bold'),justify=LEFT, bd=8)
    cashier_id_entry.grid(row=2, column=1)

    cashier_pass_label = Label(frame, text=' PIN', font=('COURIER', 30, 'bold'),bd=10, fg='black', bg='skyblue', pady=30, padx=5)
    cashier_pass_label.grid(row=3, column=0)

    cashier_pass_entry = Entry(frame, width=15, font=('ARIAL',25,'bold'),justify=LEFT, bd=8)
    cashier_pass_entry.grid(row=3, column=1)
    cashier_pass_entry.config(show='*')

    cashier_login_button = Button(frame,text='Login',fg='cadet blue', bg='green', font=('COURIER', 20, 'bold'), pady=16, padx=16, bd=8, relief=RAISED, command=check_cashier_cred)
    cashier_login_button.grid(row=4, column=1)

    admin_login_button = Button(frame,text='Admin', bg='red', font=('COURIER', 20, 'bold'), pady=16, padx=16, bd=4, relief=RAISED, command=admin_window)
    admin_login_button.grid(row=4, column=0)


    window.mainloop()

def Cost():
    #*********PIZZA COST*************
    global rslt
    global rslt1
    conn = sqlite3.connect('pyzza.db')
    c = conn.cursor()
    c.execute('SELECT price FROM pizza')
    piz_prices = c.fetchall()
    qnt_list = []
    cost_list = []
    rslt = []
    for i in range(len(entry_list)):
        qnt_list.append(int(entry_list[i].get()))
        cost_list.append(piz_prices[i][0])
        rslt.append(qnt_list[i]* cost_list[i])

    cost_p = sum(rslt)
    eCostpizza.set(cost_p)

    conn.commit()
    conn.close()

    #*********DRINK COST*************
    conn = sqlite3.connect('pyzza.db')
    c = conn.cursor()
    c.execute('SELECT price FROM drink')
    drk_prices = c.fetchall()
    qnt_list1 = []
    cost_list1 = []
    rslt1 = []
    for i in range(len(entry_list1)):
        qnt_list1.append(int(entry_list1[i].get()))
        cost_list1.append(drk_prices[i][0])
        rslt1.append(qnt_list1[i]* cost_list1[i])

    cost_d = sum(rslt1)
    eCostdrinks.set(cost_d)

    conn.commit()
    conn.close()

    #*********VAT COST*************
    #vat=(cost_p+cost_d)*0.08
	#VAT='{0:.2f}'.format(vat)
	#eVat.set('0')

    #*********TOTAL COST*************
    total = cost_p + cost_d
    eTotal.set(total)

    #*********BALANCE*************
    try:
        paid=int(entryAmmount.get())
    except Exception as Error:
        pass
    try:
        balance=int(paid-total)
        eBalance.set(balance)
    except Exception as Error:
        pass

def Reset():
    eAmmount.set('')
    eTotal.set('')
    eVat.set('')
    eCostdrinks.set('')
    eCostpizza.set('')
    eBalance.set('')
    receipt.delete('1.0', END)

    for i in range(len(var_list)):
        var_list[i].set('0')
        textvar_list[i].set('0')
        entry_list[i].config(state=DISABLED)

    for j in range(len(var_list1)):
        var_list1[j].set('0')
        textvar_list1[j].set('0')
        entry_list1[j].config(state=DISABLED)

def check_btn():
    for i in range(len(var_list)):
        if var_list[i].get() == 1:
            entry_list[i].config(state=NORMAL)
        elif var_list[i].get() == 0:
            entry_list[i].config(state=DISABLED)
            textvar_list[i].set('0')

    for j in range(len(var_list1)):
        if var_list1[j].get() == 1:
            entry_list1[j].config(state=NORMAL)
        elif var_list1[j].get() == 0:
            entry_list1[j].config(state=DISABLED)
            textvar_list1[j].set('0')

def receipt_order():
    dateOfOrder=StringVar()
    dateOfOrder.set(datetime.today())
    receiptRef=StringVar()
    rcpt=random.randint(1000,9999)
    receiptRef.set(rcpt)
    receipt.delete('1.0',END)
    rcpt_ref = receiptRef.get()
    date = dateOfOrder.get()
    receipt.insert(END,'Receipt Ref:{} \t\t {}\n\n'.format(rcpt_ref,date))
    receipt.insert(END,'Items \t\t Quantity \t\t Cost\n\n')
    conn = sqlite3.connect('pyzza.db')
    c = conn.cursor()
    for i in range(len(rslt)):
        qnt = int(entry_list[i].get())
        if qnt > 0:
            c.execute('SELECT * FROM pizza WHERE oid=:oid',
                        {'oid': i+1})
            rcs = c.fetchall()
            p_name = rcs[0][0]
            p_price = rcs[0][1]
            cost = qnt * p_price
            receipt.insert(END,'{} \t\t  {}x{} \t\t  {}\n'.format(p_name,qnt,p_price,cost))
        else:
            pass

    for i in range(len(rslt1)):
        qnt1 = int(entry_list1[i].get())
        if qnt1 > 0:
            c.execute('SELECT * FROM drink WHERE oid=:oid',
                        {'oid': i+1})
            rcs1 = c.fetchall()
            d_name = rcs1[0][0]
            d_price = rcs1[0][1]
            cost1 = qnt1 * d_price
            receipt.insert(END,'{} \t\t  {}x{} \t\t  {}\n'.format(d_name,qnt1,d_price,cost1))

    vt = eVat.get()
    tt = eTotal.get()
    amt = eAmmount.get()
    blc = eBalance.get()

    receipt.insert(END,'\nTotal KSHS. \t\t {}\n'.format(tt))
    receipt.insert(END,'Ammount Paid KSHS. \t\t\t {} \n'.format(amt))
    receipt.insert(END,'Balance KSHS. \t\t\t {} \n'.format(blc))
    receipt.insert(END,'VAT(8%) KSHS. \t\t{} \n'.format(vt))
	#receipt.insert(END,'**********WE ARE GLAD TO HAVE YOU**********')
    #

    conn.commit()
    conn.close()

def prod_menu():
    #global root

    top = Toplevel()
    top.title('Pizza Management System')
    top.geometry('1350x750+0+0')
    top.config(bg='black')

    #***********************FRAMES****************************
    tf = Frame(top,width='1350',height='50',border=10,relief=RAISED)
    tf.pack(side=TOP)

    lf = Frame(top,width='900',height='700',border=8,relief=RAISED)
    lf.pack(side=LEFT)

    rf = Frame(top,width='450',height='700',border=8,relief=RAISED)
    rf.pack(side=RIGHT)

    tlf = Frame(lf,width='900',height='500',border=8,relief=RAISED)
    tlf.pack(side=TOP)

    blf = Frame(lf,width='900',height='250',border=6,relief=RAISED)
    blf.pack(side=BOTTOM)

    trf = Frame(rf,width='450',height='450',border=12,relief=RAISED)
    trf.pack(side=TOP)

    brf = Frame(rf,width='450',height='250',border=16,relief=RAISED)
    brf.pack(side=BOTTOM)

    pizza_frame1 = Frame(tlf,width='450',height='500',border=16,relief=RAISED)
    pizza_frame1.pack(side=LEFT)

    drink__frame1 = Frame(tlf,width='450',height='500',border=16,relief=RAISED)
    drink__frame1.pack(side=RIGHT)

    cost_frame1 = Frame(blf,width='450',height='250',bd=14,relief=RAISED)
    cost_frame1.pack(side=LEFT)

    ammount_frame1 = Frame(blf,width='450',height='250',bd=14,relief=RAISED)
    ammount_frame1.pack(side=RIGHT)


    tf.config(bg='black')
    lf.config(bg='black')
    rf.config(bg='black')


    #******************* LABELS******************************

    Label(tf,text='    DOT PYZZA MANAGEMENT SYSTEM      ', font=('COURIER', 50, 'bold'),bd=10, fg="cadet blue", bg="white").grid(row=0,column=0)

    Label(cost_frame1,text='COST OF PIZZA \t\t', font=('COURIER', 18, 'bold'), bd=8, anchor=W).grid(row=0,column=0,sticky=W, padx=10)

    Label(cost_frame1,text='COST OF DRINKS', font=('COURIER', 18, 'bold'), bd=8, anchor=W).grid(row=1,column=0,sticky=W, padx=10)

    Label(cost_frame1,text='VAT (8%)\t', font=('COURIER', 18, 'bold'), bd=8, anchor=W).grid(row=2,column=0,sticky=W, padx=10)

    Label(ammount_frame1,text='TOTAL\t\t', font=('COURIER', 18, 'bold'), bd=8, anchor=W).grid(row=0,column=0,sticky=W, padx=10)

    Label(ammount_frame1,text='AMMOUNT PAID   \t', font=('COURIER', 18, 'bold'), bd=8, anchor=W).grid(row=1,column=0,sticky=W, padx=10)

    Label(ammount_frame1,text='BALANCE\t', font=('COURIER', 18, 'bold'), bd=8, anchor=W).grid(row=2,column=0,sticky=W)

    Label(trf,text='Receipt', font=('COURIER', 12, 'bold'),bd=2,anchor="w").grid(row=0,column=0,sticky=W)

    #global var
    global var_list
    #global textvar
    global textvar_list
    #global entry
    global entry_list
    #global var1
    global var_list1
    #global entry1
    global entry_list1
    #global textvar1
    global textvar_list1

    conn = sqlite3.connect('pyzza.db')
    c = conn.cursor()
    c.execute('SELECT *, oid FROM pizza')
    pizza_records = c.fetchall()
    i = 0
    var_list = []
    entry_list = []
    textvar_list = []
    for pr in pizza_records:
        var_id = str(pr[2])
        #check_btn = 'checkPbtn' + var_id
        var = IntVar()
        entry = 'entryP' + var_id
        textvar = StringVar()
        #*****************PIZZA CHECK BUTTONS*************************
        check_btnP = Checkbutton(pizza_frame1,text=pr[0] + '      \t',font=('COURIER', 18, 'bold'),command=check_btn,variable=var,onvalue=1,offvalue=0)
        check_btnP.grid(row=i, sticky=W)
        var_list.append(var)
        #*****************PIZZA ENTRY**************************
        entry = Entry(pizza_frame1,width=6,font=('ARIAL',12,'bold'),justify=LEFT, bd=8,state=DISABLED,textvariable=textvar)
        entry.grid(row=i,column=1)
        entry_list.append(entry)
        textvar_list.append(textvar)
        textvar.set('0')
        i += 1


    c.execute('SELECT *, oid FROM drink')
    drink_records = c.fetchall()
    i = 0
    var_list1 = []
    entry_list1 = []
    textvar_list1 = []
    for dr in drink_records:
        var1_id = str(dr[2])
        var1 = IntVar()
        entry1 = 'entryD' + var1_id
        textvar1 = StringVar()
        textvar1.set('0')
        #*****************DRINKS CHECK BUTTONS**************************
        check_btnD = Checkbutton(drink__frame1,text=dr[0] + '       \t',font=('COURIER', 18, 'bold'),command=check_btn,variable=var1,onvalue=1,offvalue=0)
        check_btnD.grid(row=i, sticky=W)
        var_list1.append(var1)
        #*****************DRINKS ENTRY**************************
        entry1 = Entry(drink__frame1,width=6,font=('ARIAL',12,'bold'),justify=LEFT, bd=8,state=DISABLED,textvariable=textvar1)
        entry1.grid(row=i,column=1)
        entry_list1.append(entry1)
        textvar_list1.append(textvar1)
        i += 1

    conn.commit()
    conn.close()



    #*****************TOTAL ENTRY**************************
    global eCostpizza
    global eCostdrinks
    global eVat
    global eTotal
    global eAmmount
    global eBalance
    global receipt
    global entryAmmount

    eCostpizza=StringVar()
    eCostdrinks=StringVar()
    eVat=StringVar()
    eTotal=StringVar()
    eAmmount=StringVar()
    eBalance=StringVar()

    entryCostpizza = Entry(cost_frame1,width=8,font=('ARIAL', 18),justify=LEFT, bd=8,state=NORMAL,textvariable=eCostpizza)
    entryCostpizza.grid(row=0,column=1)

    entrycostdrinks = Entry(cost_frame1,width=8,font=('ARIAL', 18),justify=LEFT, bd=8,state=NORMAL,textvariable=eCostdrinks)
    entrycostdrinks.grid(row=1,column=1)

    entryVat = Entry(cost_frame1,width=8,font=('ARIAL', 18),justify=LEFT, bd=8,state=NORMAL,textvariable=eVat)
    entryVat.grid(row=2,column=1)

    entryTotal = Entry(ammount_frame1,width=8,font=('ARIAL', 18),justify=LEFT, bd=8,state=NORMAL,textvariable=eTotal)
    entryTotal.grid(row=0,column=1)

    entryAmmount = Entry(ammount_frame1,width=8,font=('ARIAL', 18),justify=LEFT, bd=8,state=NORMAL,textvariable=eAmmount)
    entryAmmount.grid(row=1,column=1)

    entryBalance = Entry(ammount_frame1,width=8,font=('ARIAL', 18),justify=LEFT, bd=8,state=NORMAL,textvariable=eBalance)
    entryBalance.grid(row=2,column=1)

    #******************RECEIPT************************************

    receipt = Text(trf,width='45',height='25',bg='white',bd=8,font=('ARIAL', 11, 'bold'))
    receipt.grid(row=1, column=0)


    #***************BUTTONS**************************

    btnTotal = Button(brf,text='TOTAL',bd=4,bg='green', font=('COURIER', 12, 'bold'),padx=16,pady=1,command=Cost)
    btnTotal.grid(row=0,column=0)

    btnReceipt = Button(brf,text='RECEIPT',fg='black',bg='white', font=('COURIER', 12, 'bold'),bd=4,padx=5,pady=1,command=receipt_order)
    btnReceipt.grid(row=0,column=1)

    btnReset = Button(brf,text='RESET',fg='black',bg='grey', font=('COURIER', 12, 'bold'),bd=4,padx=5,pady=1,command=Reset)
    btnReset.grid(row=0,column=2)

    btnExit = Button(brf,text='EXIT',fg='black',bg='red', font=('COURIER', 12, 'bold'),bd=4,padx=5,pady=1,command=top.destroy)
    btnExit.grid(row=0,column=3)


    top.mainloop()

#*********LOGIN BTN(main_window)*************
def check_cashier_cred():
    entered_username = cashier_id_entry.get()
    entered_pass = cashier_pass_entry.get()
    conn = sqlite3.connect('pyzza.db')
    c = conn.cursor()
    c.execute('SELECT username, passcode FROM cashier')
    cashier_records = c.fetchall()
    record_dict = {}
    for cr in cashier_records:
        record_dict[cr[0]] = cr[1] #PDO::FETCH_KEY_PAIR()
    if entered_username in record_dict.keys() and entered_pass in record_dict.values():
        cashier_id_entry.delete(0, END)
        cashier_pass_entry.delete(0, END)
        #window.destroy()
        prod_menu()
    else:
        messagebox.showerror(title='Invalid credentials', message='Wrong Username or Password')
        cashier_id_entry.delete(0, END)
        cashier_pass_entry.delete(0, END)
#*******************************************ADMIN*************************
#************CASHIER TABLE********************
def addCashier():
    usname = addusname_entry.get()
    pasw = addpass_entry.get()
    conn = sqlite3.connect('pyzza.db')
    c = conn.cursor()
    c.execute('INSERT INTO cashier VALUES(:username, :password)',
                {
                    'username':usname,
                    'password':pasw
                })

    conn.commit()
    conn.close()
    addusname_entry.delete(0, END)
    addpass_entry.delete(0, END)
    top1.destroy()
    messagebox.showinfo(title='Success', message='Cashier Added Successfully')
    return admin_view()

def cashier_delete():
    pk = id_entry.get()
    conn = sqlite3.connect('pyzza.db')
    c = conn.cursor()
    c.execute('DELETE FROM cashier WHERE oid={}'.format(pk))
    conn.commit()
    conn.close()

    id_entry.delete(0, END)
    top3.destroy()
    messagebox.showinfo(title='Success', message='Cashier Deleted')
    return update_cashier()

def cashier_edit():
    conn = sqlite3.connect('pyzza.db')
    c = conn.cursor()
    c.execute('SELECT * FROM cashier WHERE oid=' + id_entry.get())
    records = c.fetchall()
    for rcd in records:
        usname_entry.insert(0, rcd[0])
        pass_entry.insert(0, rcd[1])


    conn.commit()
    conn.close()

def cashier_save():
    conn = sqlite3.connect('pyzza.db')
    c = conn.cursor()
    record_id = id_entry.get()
    c.execute('''UPDATE cashier SET
            username = :name,
            passcode = :pass

            WHERE oid = :id''',
            {
                'name':usname_entry.get(),
                'pass':pass_entry.get(),
                'id':record_id
            })


    conn.commit()
    conn.close()
    usname_entry.delete(0, END)
    pass_entry.delete(0, END)
    id_entry.delete(0, END)
    top3.destroy()
    messagebox.showinfo(title='Success', message='Updated Successfully')
    return update_cashier()

def exit_cashier():
    top3.destroy()
    top1.destroy()
    admin_view()
    
def update_cashier():
    global top3

    top3 = Toplevel()
    top3.title('Update Cashiers')
    top3.config(bg='grey')
    #top3.geometry("1350x750+0+0")

    Width = '1350'
    Height = '900'
    c = Canvas(top3, height=Height, width=Width,bg='skyblue')
    c.pack()

    top_frame4 = Frame(top3, bg='skyblue',border=10,relief=RAISED)
    top_frame4.place(relx=0.03, rely=0.01, relwidth=0.9, relheight=0.1)

    left_frame4 = Frame(top3, bg='black',border=6,relief=RAISED)
    left_frame4.place(relx=0.03, rely=0.12, relwidth=0.45, relheight=0.75)

    right_frame4 = Frame(top3,width='650',height='800', bg='black',border=6,relief=RAISED)
    right_frame4.place(relx=0.5, rely=0.12, relwidth=0.45, relheight=0.75)

    title_label4 = Label(top_frame4, text='    \t\t Cashier Records  \t  ', font=('COURIER', 30, 'bold'),justify=CENTER, fg='black',bg='skyblue', padx=10)
    title_label4.grid(row=0)

    #***********global vars*************
    global id_entry
    global usname_entry
    global pass_entry

    id_label = Label(left_frame4, text='Cashier Id  ', font=('COURIER', 20, 'bold'),bd=10, fg='cadet blue', bg='black', pady=10, padx=40)
    id_label.grid(row=0, column=0, sticky=W)

    cashier_label = Label(left_frame4, text='Username ', font=('COURIER', 20, 'bold'),bd=10, fg='cadet blue', bg='black', pady=10, padx=40)
    cashier_label.grid(row=0, column=1, sticky=W)

    conn = sqlite3.connect('pyzza.db')
    c = conn.cursor()
    c.execute('SELECT oid, * FROM cashier')
    records = c.fetchall()
    i = 1
    j = 1
    for rcd in records:
        c_id = str(rcd[0])
        c_name =str(rcd[1])
        id_label = Label(left_frame4, text='\t{}'.format(c_id), font=('COURIER', 15, 'bold'),bd=10, anchor=W, fg='white', bg='black', pady=5, padx=5)
        id_label.grid(row=i, column=0,sticky=W)
        name_label = Label(left_frame4, text='\t{}'.format(c_name), font=('COURIER', 15, 'bold'),bd=10, anchor=W, fg='white', bg='black', pady=5, padx=5)
        name_label.grid(row=i, column=j,sticky=W)
        #name_label = Label(bottom_frame4, text=c_name, font=('COURIER', 15, 'bold'),bd=10, anchor=W, fg='cadet blue', bg='grey', pady=5, padx=5)
        #name_label.grid(row=i, column=1,sticky=W)
        i +=1

    conn.commit()
    conn.close()

    cashier_label = Label(right_frame4, text='Enter Cashier ID ', font=('COURIER', 20, 'bold'),bd=10,  fg='cadet blue', bg='black', pady=20, padx=20)
    cashier_label.grid(row=0, column=0)

    id_entry = Entry(right_frame4, width=10, font=('ARIAL',25,'bold'),justify=LEFT, bd=8)
    id_entry.grid(row=0, column=1)

    del_btn = Button(right_frame4,text='Delete',fg='cadet blue', bg='red', font=('COURIER', 15, 'bold'), pady=15, padx=40, bd=8, relief=RAISED, command=cashier_delete)
    del_btn.grid(row=1, column=0)

    edit_btn = Button(right_frame4,text='Edit',fg='cadet blue', bg='green', font=('COURIER', 15, 'bold'), pady=15, padx=40, bd=8, relief=RAISED, command=cashier_edit)
    edit_btn.grid(row=1, column=1)

    usname_label = Label(right_frame4, text='Username', font=('COURIER', 20, 'bold'),bd=10, fg='cadet blue', anchor=W, bg='black', pady=20, padx=15)
    usname_label.grid(row=2, column=0, sticky=W)

    usname_entry = Entry(right_frame4, width=13, font=('ARIAL',25,'bold'),justify=LEFT, bd=8)
    usname_entry.grid(row=2, column=1, sticky=W)

    pass_label = Label(right_frame4, text='Password',  font=('COURIER', 20, 'bold'),bd=10, fg='cadet blue', anchor=W, bg='black', pady=20, padx=15)
    pass_label.grid(row=3, column=0, sticky=W)

    pass_entry = Entry(right_frame4, width=13, font=('ARIAL',25,'bold'),justify=LEFT, bd=8, show='*')
    pass_entry.grid(row=3, column=1, sticky=W)

    save_btn = Button(right_frame4,text='Save',fg='cadet blue', bg='green', font=('COURIER', 15, 'bold'), pady=15, padx=40, bd=8, relief=RAISED, command=cashier_save)
    save_btn.grid(row=4, column=1)

    refr_btn = Button(right_frame4,text='Refresh',fg='cadet blue', bg='green', font=('COURIER', 15, 'bold'), pady=15, padx=40, bd=8, relief=RAISED, command=update_cashier)
    refr_btn.grid(row=5, column=0)

    exit_btn = Button(right_frame4,text=' Exit ',fg='cadet blue', bg='red', font=('COURIER', 15, 'bold'), pady=15, padx=40, bd=8, relief=RAISED, command=exit_cashier)
    exit_btn.grid(row=5, column=1)


    top3.mainloop()

#************PIZZA TABLE********************
def addPizza():
    pname = addname_entry.get()
    price = int(addprice_entry.get())
    conn = sqlite3.connect('pyzza.db')
    c = conn.cursor()
    c.execute('INSERT INTO pizza VALUES(:name, :price)',
                {
                    'name':pname,
                    'price':price
                })


    conn.commit()
    conn.close()
    addname_entry.delete(0, END)
    addprice_entry.delete(0, END)
    top1.destroy()
    messagebox.showinfo(title='Success', message='Pizza Added Successfully')
    return admin_view()

def pizza_delete():
    pk = id_entry5.get()
    conn = sqlite3.connect('pyzza.db')
    c = conn.cursor()
    c.execute('DELETE FROM pizza WHERE oid={}'.format(pk))
    conn.commit()
    conn.close()

    id_entry5.delete(0, END)
    top4.destroy()
    messagebox.showinfo(title='Success', message='Pizza Deleted')
    return update_pizza()

def pizza_edit():
    conn = sqlite3.connect('pyzza.db')
    c = conn.cursor()
    c.execute('SELECT * FROM pizza WHERE oid= {}'.format(id_entry5.get()))
    records = c.fetchall()
    for rcd in records:
        pname_entry5.insert(0, rcd[0])
        price_entry5.insert(0, rcd[1])


    conn.commit()
    conn.close()

def pizza_save():
    conn = sqlite3.connect('pyzza.db')
    c = conn.cursor()
    record_id = id_entry5.get()
    c.execute('''UPDATE pizza SET
            name = :name,
            price = :price

            WHERE oid = :id''',
            {
                'name':pname_entry5.get(),
                'price':price_entry5.get(),
                'id':record_id
            })

    conn.commit()
    conn.close()
    pname_entry5.delete(0, END)
    price_entry5.delete(0, END)
    id_entry5.delete(0, END)
    top4.destroy()
    messagebox.showinfo(title='Success', message='Updated Successfully')
    return update_pizza()

def exit_pizza():
    top4.destroy()
    top1.destroy()
    admin_view()

def update_pizza():
    global top4

    top4 = Toplevel()
    top4.title('Update Pizza')
    top4.config(bg='grey')
    #top4.geometry("1350x750+0+0")

    Width = '1350'
    Height = '1200'
    c = Canvas(top4, height=Height, width=Width,bg='skyblue')
    c.pack()

    top_frame5 = Frame(top4, bg='skyblue',border=10,relief=RAISED)
    top_frame5.place(relx=0.03, rely=0.01, relwidth=0.9, relheight=0.1)

    left_frame5 = Frame(top4, bg='black',border=6,relief=RAISED)
    left_frame5.place(relx=0.03, rely=0.12, relwidth=0.45, relheight=1.1)

    right_frame5 = Frame(top4,width='650',height='800', bg='black',border=6,relief=RAISED)
    right_frame5.place(relx=0.5, rely=0.12, relwidth=0.45, relheight=1.1)

    title_label5 = Label(top_frame5, text='    \t\t Pizza Records  \t  ', font=('COURIER', 30, 'bold'),justify=CENTER, fg='black',bg='skyblue', padx=10)
    title_label5.grid(row=0, column=0)

    #***********global vars*************
    global id_entry5
    global pname_entry5
    global price_entry5

    id_label = Label(left_frame5, text='Pizza Id', font=('COURIER', 20, 'bold'),bd=10, fg='cadet blue', bg='black', pady=10, padx=10)
    id_label.grid(row=0, column=0, sticky=W)

    name_label5 = Label(left_frame5, text='Pizza Name', font=('COURIER', 20, 'bold'),bd=10, fg='cadet blue', bg='black', pady=10, padx=10)
    name_label5.grid(row=0, column=1, sticky=W)

    price_label5 = Label(left_frame5, text='Pizza Price', font=('COURIER', 20, 'bold'),bd=10, fg='cadet blue', bg='black', pady=10, padx=10)
    price_label5.grid(row=0, column=2, sticky=W)

    conn = sqlite3.connect('pyzza.db')
    c = conn.cursor()
    c.execute('SELECT oid, * FROM pizza')
    records = c.fetchall()
    i = 1
    for rcd in records:
        p_id = str(rcd[0])
        p_name =str(rcd[1])
        p_price =str(rcd[2])

        id_label = Label(left_frame5, text='{}\t'.format(p_id), font=('COURIER', 15, 'bold'),bd=10, anchor=W, fg='white', bg='black', pady=5, padx=20)
        id_label.grid(row=i, column=0,sticky=W)
        name_label = Label(left_frame5, text=p_name, font=('COURIER', 15, 'bold'),bd=10, anchor=W, fg='white', bg='black', pady=5, padx=20)
        name_label.grid(row=i, column=1,sticky=W)
        price_label = Label(left_frame5, text=p_price, font=('COURIER', 15, 'bold'),bd=10, anchor=W, fg='white', bg='black', pady=5, padx=20)
        price_label.grid(row=i, column=2,sticky=W)
        i +=1



    conn.commit()
    conn.close()

    id_label5 = Label(right_frame5, text='Enter Pizza ID ', font=('COURIER', 20, 'bold'),bd=10,  fg='cadet blue', bg='black', pady=20, padx=20)
    id_label5.grid(row=0, column=0)

    id_entry5 = Entry(right_frame5, width=10, font=('ARIAL',25,'bold'),justify=LEFT, bd=8)
    id_entry5.grid(row=0, column=1)

    del_btn5 = Button(right_frame5,text='Delete',fg='cadet blue', bg='red', font=('COURIER', 15, 'bold'), pady=15, padx=30, bd=8, relief=RAISED, command=pizza_delete)
    del_btn5.grid(row=1, column=0)

    edit_btn5 = Button(right_frame5,text='Edit',fg='cadet blue', bg='green', font=('COURIER', 15, 'bold'), pady=15, padx=30, bd=8, relief=RAISED, command=pizza_edit)
    edit_btn5.grid(row=1, column=1)

    pname_label5 = Label(right_frame5, text='Name', font=('COURIER', 20, 'bold'),bd=10, fg='cadet blue', anchor=W, bg='black', pady=20, padx=30)
    pname_label5.grid(row=2, column=0, sticky=W)

    pname_entry5 = Entry(right_frame5, width=15, font=('ARIAL',25,'bold'),justify=LEFT, bd=8)
    pname_entry5.grid(row=2, column=1, sticky=W)

    price_label5 = Label(right_frame5, text='Price',  font=('COURIER', 20, 'bold'),bd=10, fg='cadet blue', anchor=W, bg='black', pady=20, padx=30)
    price_label5.grid(row=3, column=0, sticky=W)

    price_entry5 = Entry(right_frame5, width=15, font=('ARIAL',25,'bold'),justify=LEFT, bd=8)
    price_entry5.grid(row=3, column=1, sticky=W)

    save_btn5 = Button(right_frame5,text='Save',fg='cadet blue', bg='green', font=('COURIER', 15, 'bold'), pady=15, padx=40, bd=8, relief=RAISED, command=pizza_save)
    save_btn5.grid(row=4, column=1)

    refr_btn5 = Button(right_frame5,text='Refresh',fg='cadet blue', bg='green', font=('COURIER', 15, 'bold'), pady=15, padx=40, bd=8, relief=RAISED, command=update_pizza)
    refr_btn5.grid(row=5, column=0)

    exit_btn5 = Button(right_frame5,text=' Exit ',fg='cadet blue', bg='red', font=('COURIER', 15, 'bold'), pady=15, padx=40, bd=8, relief=RAISED, command=exit_pizza)
    exit_btn5.grid(row=5, column=1)

    top4.mainloop()

#************DRINK TABLE********************

def addDrink():
    dname = addDname_entry.get()
    price = int(addDprice_entry.get())
    conn = sqlite3.connect('pyzza.db')
    c = conn.cursor()
    c.execute('INSERT INTO drink VALUES(:name, :price)',
                {
                    'name':dname,
                    'price':price
                })


    conn.commit()
    conn.close()
    addDname_entry.delete(0, END)
    addDprice_entry.delete(0, END)
    top1.destroy()
    messagebox.showinfo(title='Success', message='Drink Added Successfully')
    return admin_view()

def drink_delete():
    pk = id_entry6.get()
    conn = sqlite3.connect('pyzza.db')
    c = conn.cursor()
    c.execute('DELETE FROM drink WHERE oid={}'.format(pk))
    conn.commit()
    conn.close()

    id_entry6.delete(0, END)

    messagebox.showinfo(title='Success', message='Drink Deleted')
    return update_drink()

def drink_edit():
    conn = sqlite3.connect('pyzza.db')
    c = conn.cursor()
    c.execute('SELECT * FROM drink WHERE oid=' + id_entry6.get())
    records = c.fetchall()
    for rcd in records:
        dname_entry6.insert(0, rcd[0])
        price_entry6.insert(0, rcd[1])


    conn.commit()
    conn.close()

def drink_save():
    conn = sqlite3.connect('pyzza.db')
    c = conn.cursor()
    record_id = id_entry6.get()
    c.execute('''UPDATE drink SET
            name = :name,
            price = :price

            WHERE oid = :id''',
            {
                'name':dname_entry6.get(),
                'price':price_entry6.get(),
                'id':record_id
            })


    conn.commit()
    conn.close()
    dname_entry6.delete(0, END)
    price_entry6.delete(0, END)
    id_entry6.delete(0, END)
    top5.destroy()
    messagebox.showinfo(title='Success', message='Drink updated Successfully')
    return update_drink()

def exit_drink():
    top5.destroy()
    top1.destroy()
    admin_view()

def update_drink():
    global top5

    top5 = Toplevel()
    top5.title('Update Drink')
    top5.config(bg='grey')
    #top5.geometry("1350x750+0+0")

    Width = '1350'
    Height = '1200'
    c = Canvas(top5, height=Height, width=Width,bg='skyblue')
    c.pack()

    top_frame6 = Frame(top5, bg='skyblue',border=10,relief=RAISED)
    top_frame6.place(relx=0.03, rely=0.01, relwidth=0.9, relheight=0.1)

    left_frame6 = Frame(top5, bg='black',border=6,relief=RAISED)
    left_frame6.place(relx=0.03, rely=0.12, relwidth=0.45, relheight=1.1)

    right_frame6 = Frame(top5,width='650',height='800', bg='black',border=6,relief=RAISED)
    right_frame6.place(relx=0.5, rely=0.12, relwidth=0.45, relheight=1.1)

    title_label6 = Label(top_frame6, text='    \t\t Drink Records  \t  ', font=('COURIER', 30, 'bold'),justify=CENTER, fg='black',bg='skyblue', padx=10)
    title_label6.grid(row=0, column=0)

    #***********global vars*************
    global id_entry6
    global dname_entry6
    global price_entry6

    id_label = Label(left_frame6, text='Drink Id', font=('COURIER', 20, 'bold'),bd=10, fg='cadet blue', bg='black', pady=10, padx=10)
    id_label.grid(row=0, column=0, sticky=W)

    name_label6 = Label(left_frame6, text='Drink Name', font=('COURIER', 20, 'bold'),bd=10, fg='cadet blue', bg='black', pady=10, padx=10)
    name_label6.grid(row=0, column=1, sticky=W)

    price_label6 = Label(left_frame6, text='Drink Price', font=('COURIER', 20, 'bold'),bd=10, fg='cadet blue', bg='black', pady=10, padx=10)
    price_label6.grid(row=0, column=2, sticky=W)

    conn = sqlite3.connect('pyzza.db')
    c = conn.cursor()
    c.execute('SELECT oid, * FROM drink')
    records = c.fetchall()
    i = 2
    for rcd in records:
        d_id = str(rcd[0])
        d_name =str(rcd[1])
        d_price =str(rcd[2])

        id_label = Label(left_frame6, text='{}\t'.format(d_id), font=('COURIER', 15, 'bold'),bd=10, anchor=W, fg='white', bg='black', pady=5, padx=20)
        id_label.grid(row=i, column=0,sticky=W)
        name_label = Label(left_frame6, text=d_name, font=('COURIER', 15, 'bold'),bd=10, anchor=W, fg='white', bg='black', pady=5, padx=20)
        name_label.grid(row=i, column=1,sticky=W)
        price_label = Label(left_frame6, text=d_price, font=('COURIER', 15, 'bold'),bd=10, anchor=W, fg='white', bg='black', pady=5, padx=20)
        price_label.grid(row=i, column=2,sticky=W)
        i +=1

    conn.commit()
    conn.close()

    id_label6 = Label(right_frame6, text='Enter Drink ID ', font=('COURIER', 20, 'bold'),bd=10,  fg='cadet blue', bg='black', pady=20, padx=20)
    id_label6.grid(row=0, column=0)

    id_entry6= Entry(right_frame6, width=10, font=('ARIAL',25,'bold'),justify=LEFT, bd=8)
    id_entry6.grid(row=0, column=1)

    del_btn6 = Button(right_frame6,text='Delete',fg='cadet blue', bg='red', font=('COURIER', 15, 'bold'), pady=15, padx=30, bd=8, relief=RAISED, command=drink_delete)
    del_btn6.grid(row=1, column=0)

    edit_btn6 = Button(right_frame6,text='Edit',fg='cadet blue', bg='green', font=('COURIER', 15, 'bold'), pady=15, padx=30, bd=8, relief=RAISED, command=drink_edit)
    edit_btn6.grid(row=1, column=1)

    dname_label6 = Label(right_frame6, text='Name', font=('COURIER', 20, 'bold'),bd=10, fg='cadet blue', anchor=W, bg='black', pady=20, padx=30)
    dname_label6.grid(row=2, column=0, sticky=W)

    dname_entry6 = Entry(right_frame6, width=15, font=('ARIAL',25,'bold'),justify=LEFT, bd=8)
    dname_entry6.grid(row=2, column=1, sticky=W)

    price_label6 = Label(right_frame6, text='Price',  font=('COURIER', 20, 'bold'),bd=10, fg='cadet blue', anchor=W, bg='black', pady=20, padx=30)
    price_label6.grid(row=3, column=0, sticky=W)

    price_entry6 = Entry(right_frame6, width=15, font=('ARIAL',25,'bold'),justify=LEFT, bd=8)
    price_entry6.grid(row=3, column=1, sticky=W)

    save_btn6 = Button(right_frame6,text='Save',fg='cadet blue', bg='green', font=('COURIER', 15, 'bold'), pady=15, padx=40, bd=8, relief=RAISED, command=drink_save)
    save_btn6.grid(row=4, column=1)

    refr_btn6 = Button(right_frame6,text='Refresh',fg='cadet blue', bg='green', font=('COURIER', 15, 'bold'), pady=15, padx=40, bd=8, relief=RAISED, command=update_drink)
    refr_btn6.grid(row=5, column=0)

    exit_btn6 = Button(right_frame6,text=' Exit ',fg='cadet blue', bg='red', font=('COURIER', 15, 'bold'), pady=15, padx=40, bd=8, relief=RAISED, command=exit_drink)
    exit_btn6.grid(row=5, column=1)

    top5.mainloop()


#*****************ADMIN BUTTON(main_window)************
def exit_admin():
    top2.destroy()
    top1.destroy()
    admin_window()

def admin_view():
    global top1
    top1 = Toplevel()
    top1.title('Admin View')
    top1.config(bg='grey')
    #top1.geometry('1350x900+0+0')

    Width = '1350'
    Height = '900'
    c = Canvas(top1, height=Height, width=Width,bg='skyblue')
    c.pack()

    top_frame3 = Frame(top1, bg='skyblue',border=14,relief=RAISED)
    top_frame3.place(relx=0.03, rely=0.01, relwidth=0.9, relheight=0.1)

    left_frame3 = Frame(top1, bg='black',border=6,relief=RAISED)
    left_frame3.place(relx=0.03, rely=0.12, relwidth=0.45, relheight=0.75)

    right_frame3 = Frame(top1,width='650',height='800', bg='black',border=6,relief=RAISED)
    right_frame3.place(relx=0.5, rely=0.12, relwidth=0.45, relheight=0.75)

    cashier__frame = Frame(left_frame3, bg='black',width='650',height='400',relief=RAISED)
    cashier__frame.pack(side=TOP)

    drink__frame = Frame(left_frame3, bg='black',width='650',height='400',relief=RAISED)
    drink__frame.pack(side=BOTTOM)

    pizza__frame = Frame(right_frame3,bg='black',width='650',height='400',relief=RAISED)
    pizza__frame.pack(side=TOP)

    btn__frame = Frame(right_frame3, bg='black',width='650',height='400',relief=RAISED)
    btn__frame.pack(side=BOTTOM)

    title_label = Label(top_frame3, text='   \t \t\t ADMIN MODE  \t\t  ', font=('COURIER', 25, 'bold'),justify=CENTER, fg='black',bg='skyblue', padx=30)
    title_label.grid(row=0)

    #***************************Add Cashier Frame******************
    #********global*********
    global addusname_entry
    global addpass_entry
    global addname_entry
    global addprice_entry
    global addDname_entry
    global addDprice_entry

    addcashier_label = Label(cashier__frame, text='\t\t   Add Cashier   \t\t', font=('COURIER', 15, 'bold'),justify=CENTER,bd=10, fg='cadet blue', bg='white', pady=5, padx=10)
    addcashier_label.grid(row=0, columnspan=2)

    addusname_label = Label(cashier__frame, text='Username\t', font=('COURIER', 20, 'bold'),bd=10, fg='cadet blue', bg='black', pady=20, padx=20, borderwidth=2)
    addusname_label.grid(row=1, column=0, sticky=W)

    addusname_entry = Entry(cashier__frame, width=15, font=('ARIAL',20,'bold'),justify=LEFT, bd=8)
    addusname_entry.grid(row=1, column=1, sticky=W)

    addpass_label = Label(cashier__frame, text='Password\t', font=('COURIER', 20, 'bold'),bd=10, fg='cadet blue', bg='black',pady=20, padx=20, borderwidth=2)
    addpass_label.grid(row=2, column=0, sticky=W)

    addpass_entry = Entry(cashier__frame, width=15, font=('ARIAL',20,'bold'),justify=LEFT, bd=8, show='*')
    addpass_entry.grid(row=2, column=1, sticky=W)

    addcashier_btn = Button(cashier__frame, text='Add Cashier',bd=2, fg='cadet blue', bg='green', font=('COURIER', 15, 'bold'),padx=5,pady=10, command=addCashier)
    addcashier_btn.grid(row=3, column=1)

    updatecashier_btn = Button(cashier__frame, text='Update Cashier Records',bd=2, fg='white', bg='grey', font=('COURIER', 15, 'bold'),padx=10,pady=10, command=update_cashier)
    updatecashier_btn.grid(row=3, column=0, sticky=W)

    #*************Add Pizza Frame*************************
    addpizza_label = Label(pizza__frame, text='\t\t    Add Pizza    \t\t', font=('COURIER', 15, 'bold'),justify=CENTER,bd=10, fg='cadet blue', bg='white', pady=10, padx=20)
    addpizza_label.grid(row=0, columnspan=2)

    addname_label = Label(pizza__frame, text='Pizza Name \t', font=('COURIER', 20, 'bold'),bd=10, fg='cadet blue', bg='black', pady=20, borderwidth=2)
    addname_label.grid(row=1, column=0, sticky=W)

    addname_entry = Entry(pizza__frame, width=15, font=('ARIAL',20,'bold'),justify=LEFT, bd=8)
    addname_entry.grid(row=1, column=1, sticky=W)

    addprice_label = Label(pizza__frame, text='Price \t', font=('COURIER', 20, 'bold'),bd=10, fg='cadet blue', bg='black',  pady=20, borderwidth=2)
    addprice_label.grid(row=2, column=0, sticky=W)

    addprice_entry = Entry(pizza__frame, width=12, font=('ARIAL',20,'bold'),justify=LEFT, bd=8)
    addprice_entry.grid(row=2, column=1, sticky=W)

    addpizza_btn = Button(pizza__frame, text='Add Pizza',bd=4, fg='cadet blue', bg='green', font=('COURIER', 15, 'bold'),padx=10,pady=10, command=addPizza)
    addpizza_btn.grid(row=3, column=1)

    updatepizza_btn = Button(pizza__frame, text='Update Pizza Records',bd=2, fg='white', bg='grey', font=('COURIER', 15, 'bold'),padx=10,pady=10, command=update_pizza)
    updatepizza_btn.grid(row=3, column=0, sticky=W)

    #*************Add Drink Frame*************************
    adddrink_label = Label(drink__frame, text='\t\t    Add Drink    \t\t', font=('COURIER', 15, 'bold'),bd=10, fg="cadet blue", bg='white', pady=10, padx=20)
    adddrink_label.grid(row=0, columnspan=2, sticky=W)

    addDname_label = Label(drink__frame, text='Drink Name \t', font=('COURIER', 20, 'bold'),bd=10, fg='cadet blue', bg='black',  pady=20, borderwidth=2)
    addDname_label.grid(row=1, column=0, sticky=W)

    addDname_entry = Entry(drink__frame, width=15,font=('ARIAL',20,'bold'),justify=LEFT, bd=8)
    addDname_entry.grid(row=1, column=1, sticky=W)

    addDprice_label = Label(drink__frame, text='Price \t', font=('COURIER', 20, 'bold'),bd=10, fg='cadet blue', bg='black',  pady=20, borderwidth=2)
    addDprice_label.grid(row=2, column=0, sticky=W)

    addDprice_entry = Entry(drink__frame, width=12, font=('ARIAL',20,'bold'),justify=LEFT, bd=8)
    addDprice_entry.grid(row=2, column=1, sticky=W)

    addD_btn = Button(drink__frame, text='Add Drink',bd=4, fg='cadet blue', bg='green', font=('COURIER', 15, 'bold'),padx=10,pady=10, command=addDrink)
    addD_btn.grid(row=3, column=1)

    updateD_btn = Button(drink__frame, text='Update Drinks Records',bd=2, fg='white', bg='grey', font=('COURIER', 15, 'bold'),padx=10,pady=10,command=update_drink)
    updateD_btn.grid(row=3, column=0, sticky=W)


    #*************btn Frame***********************
    view_sales_button = Button(btn__frame,text='View Sales',fg='cadet blue', bg='green', font=('COURIER', 20, 'bold'), pady=32, padx=12, bd=8, relief=RAISED)
    view_sales_button.grid(row=0, column=0)

    #settings_button = Button(btn__frame,text='View Sales',fg='cadet blue', bg='green', font=("COURIER", 20, "bold"), pady=13, padx=12, bd=8, relief=RAISED)
    #settings_button.grid(row=1, column=0)

    exit_button = Button(btn__frame,text='   Exit   ',fg='cadet blue', bg='red', font=('COURIER', 20, 'bold'), pady=32, padx=12, bd=8, relief=RAISED, command=exit_admin)
    exit_button.grid(row=2, column=0)


    top1.mainloop()

def check_admin_cred():
    entered_id = int(admin_id_entry.get())
    entered_pass = admin_pass_entry.get()
    conn = sqlite3.connect('pyzza.db')
    c = conn.cursor()
    c.execute('SELECT oid,* FROM cashier') #FETCH_KEY_PAIR
    admin_id = c.fetchall()
    if entered_id == admin_id[0][0] and entered_pass == admin_id[0][2]:
        admin_id_entry.delete(0, END)
        admin_pass_entry.delete(0, END)
        admin_view()
    else:
        messagebox.showerror(title='Invalid credentials', message='Wrong Username or Pin')
        top2.destroy()
        return admin_window()

    conn.commit()
    conn.close()


def admin_window():
    global top2
    top2 = Toplevel()
    top2.title('Admin window')
    top2.config(bg='grey')
    #top2.geometry("1350x750+0+0")

    Width = '1350'
    Height = '900'
    c = Canvas(top2, height=Height, width=Width)
    c.pack()

    frame2 = Frame(top2, bg='skyblue',relief=RAISED)
    frame2.place(relx=0.05, rely=0.02, relwidth=0.9, relheight=0.85)

    title_label2 = Label(frame2, text='      DOT PYZZA MANAGEMENT SYSTEM    ', font=('COURIER', 40, 'bold'),bd=10, fg='cadet blue', bg='white',justify=CENTER, pady=30, padx=10)
    title_label2.grid(row=0, columnspan=2)

    admin_label = Label(frame2, text=' ADMIN LOGIN ', font=('COURIER', 40, 'bold'),bd=10, fg='black', bg='skyblue',justify=CENTER, pady=30)
    admin_label.grid(row=1, columnspan=2)

    admin_id_label = Label(frame2, text='ID', font=('COURIER', 30, 'bold'),bd=10, justify=CENTER, fg='black', bg='skyblue', pady=30, borderwidth=2)
    admin_id_label.grid(row=2, column=0)

    #************global variables*************************
    global admin_id_entry
    global admin_pass_entry

    admin_id_entry = Entry(frame2, width=15, font=('ARIAL',25,'bold'),justify=LEFT, bd=8)
    admin_id_entry.grid(row=2, column=1)

    admin_pass_label = Label(frame2, text='PIN', font=('COURIER', 30, 'bold'),bd=10, fg='black', bg='skyblue', pady=30, padx=5)
    admin_pass_label.grid(row=3, column=0)

    admin_pass_entry = Entry(frame2, width=15, font=('ARIAL',25,'bold'),justify=LEFT, bd=8)
    admin_pass_entry.grid(row=3, column=1)
    admin_pass_entry.config(show='*')

    admin_login_button = Button(frame2,text='Login',fg='cadet blue', bg='green', font=('COURIER', 20, 'bold'), pady=16, padx=16, bd=8, relief=RAISED, command=check_admin_cred)
    admin_login_button.grid(row=4, column=1)

    main_window_button = Button(frame2,text='Main Window', bg='grey', font=('COURIER', 20, 'bold'), pady=16, padx=16, bd=8, relief=RAISED, command=top2.destroy)#, command=check_admin_cred)
    main_window_button.grid(row=4, column=0)


    top2.mainloop()


main_window()
