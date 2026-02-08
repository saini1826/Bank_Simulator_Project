from tkinter import Tk,Label,Frame,Entry,Button,simpledialog,messagebox
from tkinter.ttk import Combobox
import time
import generator
import tables
import mailing
import sqlite3
from PIL import Image,ImageTk
tables.create_tables()

#it is used to update date & time every 1000 ms(1 sec)
def update_time():
    datetime=time.strftime("%d-%b-%Y ⏰ %r")
    dt_lbl.configure(text=datetime)
    dt_lbl.after(1000,update_time)

def forgot_screen():
    frm=Frame(root,highlightbackground='black',highlightthickness=2)
    frm.configure(bg="pink")
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.75)

    def back():
        frm.destroy()
        main_screen()

    def send_forgot_otp():
        acn=acn_entry.get()
        email=email_entry.get()

        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        query="select name,pass from accounts where acn=? and email=?"
        curobj.execute(query,(acn,email,))
        tup=curobj.fetchone()
        conobj.close()

        if tup!=None:
            otp=generator.forgot_otp()
            text=f"""Hello {tup[0]},
OTP to recover password is = {otp}
"""
            messagebox.showinfo("Forgot","OTP sent to registerd email")
            mailing.forgototp_mail(email,text)
            attempts=1
            while attempts<=3:
                attempts+=1
                uotp=simpledialog.askinteger("forgot","OTP")
                if otp==uotp:
                    messagebox.showinfo("password",tup[1])
                    break
                else:
                    messagebox.showerror("Forgot","Invalid OTP,try again")

        else:
            messagebox.showerror("Forgot","Invalid Details")

    back_btn=Button(frm,text="back",font=('arial',20,'bold'),
                       bg="powder blue",bd=5,command=back)
    
    back_btn.place(relx=0,rely=0)

    acn_lbl=Label(frm,text="ACN",font=('arial',20,'bold'),bg="pink")
    acn_lbl.place(relx=.3,rely=.2)

    acn_entry=Entry(frm,font=('arial',20,'bold'),bd=5)
    acn_entry.place(relx=.4,rely=.2)
    acn_entry.focus()

    email_lbl=Label(frm,text="Email",font=('arial',20,'bold'),bg="pink")
    email_lbl.place(relx=.3,rely=.3)

    email_entry=Entry(frm,font=('arial',20,'bold'),bd=5)
    email_entry.place(relx=.4,rely=.3)

    otp_btn=Button(frm,text="send otp",font=('arial',20,'bold'),
                       bg="powder blue",bd=5,command=send_forgot_otp)
    
    otp_btn.place(relx=.45,rely=.4)


def customer_screen(uacn):
    frm=Frame(root,highlightbackground='black',highlightthickness=2)
    frm.configure(bg="pink")
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.75)

    def logout():
        frm.destroy()
        main_screen()


    def show():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.6)

        title_lbl=Label(ifrm,text="This is Show Details Screen",
                        font=('arial',20,'bold'),bg="white",fg='purple')
        title_lbl.pack()

        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        query="select * from accounts where acn=?"
        curobj.execute(query,(uacn,))
        tup=curobj.fetchone()
        conobj.close()

        text=f"""
Account No = {tup[0]}

Acc Open Date = {tup[7]}

Acc Adhar = {tup[5]}

Acc Mob = {tup[4]}

Acc Bal = {tup[3]}

"""
        info_lbl=Label(ifrm,text=text,font=("arial",20),bg="white",fg="blue")
        info_lbl.place(relx=.2,rely=.1)
    def edit():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.6)

        def update():
            name=name_entry.get()
            pwd=pass_entry.get()
            mob=mob_entry.get()
            email=email_entry.get()

            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            query="update accounts set name=?,pass=?,mob=?,email=? where acn=?"
            curobj.execute(query,(name,pwd,mob,email,uacn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Update","Details Updated")

        title_lbl=Label(ifrm,text="This is Edit Details Screen",
                        font=('arial',20,'bold'),bg="white",fg='purple')
        title_lbl.pack()

        name_lbl=Label(ifrm,text="Name",font=('arial',15,'bold'),bg="white")
        name_lbl.place(relx=.1,rely=.1)

        name_entry=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        name_entry.place(relx=.1,rely=.17)
        name_entry.focus()

        email_lbl=Label(ifrm,text="Email",font=('arial',15,'bold'),bg="white")
        email_lbl.place(relx=.5,rely=.1)

        email_entry=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        email_entry.place(relx=.5,rely=.17)
        
        mob_lbl=Label(ifrm,text="Mob",font=('arial',15,'bold'),bg="white")
        mob_lbl.place(relx=.1,rely=.3)

        mob_entry=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        mob_entry.place(relx=.1,rely=.37)

        pass_lbl=Label(ifrm,text="Pass",font=('arial',15,'bold'),bg="white")
        pass_lbl.place(relx=.5,rely=.3)

        pass_entry=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        pass_entry.place(relx=.5,rely=.37)
        
        update_btn=Button(ifrm,text="Update & Save",font=('arial',20,'bold'),
                       bg="green",bd=5,fg="white",width=12,command=update)
    
        update_btn.place(relx=.4,rely=.6)

        name_entry.insert(0,tup[0])
        pass_entry.insert(0,tup[3])
        mob_entry.insert(0,tup[1])
        email_entry.insert(0,tup[2])

    def deposit():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.6)

        title_lbl=Label(ifrm,text="This is Deposit Details Screen",
                        font=('arial',20,'bold'),bg="white",fg='purple')
        title_lbl.pack()

        uamt=simpledialog.askfloat("Deposit","Amount")
    
        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        query="update accounts set bal=bal+? where acn=?"
        curobj.execute(query,(uamt,uacn))
        conobj.commit()
        conobj.close()
        messagebox.showinfo("Deposit",f"{uamt} deposited")

    def withdraw():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.6)

        title_lbl=Label(ifrm,text="This is Withdraw Screen",
                        font=('arial',20,'bold'),bg="white",fg='purple')
        title_lbl.pack()

        uamt=simpledialog.askfloat("Withdraw","Amount")
        if uamt==None:
            return
        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        query="select bal from accounts where acn=?"
        curobj.execute(query,(uacn,))
        bal=curobj.fetchone()[0]
        conobj.close()

        if bal>=uamt:
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            query="update accounts set bal=bal-? where acn=?"
            curobj.execute(query,(uamt,uacn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Withdarw",f"{uamt} withdrawn")
        else:
            messagebox.showerror("Withdraw","Insufficient bal")

    def transfer():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.6)

        title_lbl=Label(ifrm,text="This is Transfer Screen",
                        font=('arial',20,'bold'),bg="white",fg='purple')
        title_lbl.pack()

        toacn=simpledialog.askinteger("Transfer","To ACN")
        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        query="select * from accounts where acn=?"
        curobj.execute(query,(toacn,))
        tup=curobj.fetchone()
        conobj.close()
        if tup!=None:
            uamt=simpledialog.askfloat("Transfer","Amount")

            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            query="select bal from accounts where acn=?"
            curobj.execute(query,(uacn,))
            bal=curobj.fetchone()[0]
            conobj.close()

            if bal>=uamt:
                conobj=sqlite3.connect(database="bank.sqlite")
                curobj=conobj.cursor()
                query1="update accounts set bal=bal-? where acn=?"
                query2="update accounts set bal=bal+? where acn=?"

                curobj.execute(query1,(uamt,uacn))
                curobj.execute(query2,(uamt,toacn))
                
                conobj.commit()
                conobj.close()
                messagebox.showinfo("Transfer",f"{uamt} transfered to {toacn}")
            else:
                messagebox.showerror("Withdraw","Insufficient bal")

        else:
            messagebox.showerror("Transfer","Invalid TO ACN")

    conobj=sqlite3.connect(database="bank.sqlite")
    curobj=conobj.cursor()
    query="select name from accounts where acn=?"
    curobj.execute(query,(uacn,))
    name=curobj.fetchone()[0]
    conobj.close()

    wel_lbl=Label(frm,text=f"Welcome {name.capitalize()}",
                        font=('arial',20,'bold'),bg="pink",fg='purple')
    wel_lbl.place(relx=0,rely=0)
    

    logout_btn=Button(frm,text="logout",font=('arial',20,'bold'),
                       bg="powder blue",command=logout,bd=5)
    logout_btn.place(relx=.9,rely=0)



    show_btn=Button(frm,text="show details",font=('arial',20,'bold'),
                       bg="powder blue",bd=5,width=12,command=show)
    
    show_btn.place(relx=.001,rely=.1)

    edit_btn=Button(frm,text="edit details",font=('arial',20,'bold'),
                       bg="powder blue",bd=5,width=12,command=edit)
    
    edit_btn.place(relx=.001,rely=.25)

    deposit_btn=Button(frm,text="deposit",font=('arial',20,'bold'),
                       bd=5,width=12,bg="green",fg="white",command=deposit)
    
    deposit_btn.place(relx=.001,rely=.4)

    withdraw_btn=Button(frm,text="withdraw",font=('arial',20,'bold')
                      ,bd=5,width=12,bg="red",fg="white",command=withdraw)
    
    withdraw_btn.place(relx=.001,rely=.55)

    transfer_btn=Button(frm,text="transfer",font=('arial',20,'bold')
                       ,bd=5,width=12,bg="red",fg="white",command=transfer)
    
    transfer_btn.place(relx=.001,rely=.7)


def admin_screen():
    frm=Frame(root,highlightbackground='black',highlightthickness=2)
    frm.configure(bg="pink")
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.75)

    def logout():
        frm.destroy()
        main_screen()

    wel_lbl=Label(frm,text="Welcome Admin",
                        font=('arial',20,'bold'),bg="pink",fg='purple')
    wel_lbl.place(relx=0,rely=0)
    

    logout_btn=Button(frm,text="logout",font=('arial',20,'bold'),
                       bg="powder blue",command=logout,bd=5)
    logout_btn.place(relx=.9,rely=0)

    def new():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.1,rely=.2,relwidth=.8,relheight=.6)

        def open_acn():
            name=name_entry.get()
            email=email_entry.get()
            mob=mob_entry.get()
            adhar=adhar_entry.get()
            bal=0
            opendate=time.strftime("%d-%b-%Y %r")
            pwd=generator.password()

            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            query="insert into accounts values(null,?,?,?,?,?,?,?)"
            curobj.execute(query,(name,pwd,bal,mob,adhar,email,opendate))
            conobj.commit()
            conobj.close()

            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            query="select max(acn) from accounts"
            curobj.execute(query)
            acn=curobj.fetchone()[0]
            conobj.close()


            text=f"""Welcome {name},
We have successfully opened your account in ABC Bank
This is your Credentials
ACN={acn}
Pass={pwd}
"""
            mailing.openacn_mail(email,text)

            messagebox.showinfo("Account Open","We have opened your account and mailed credentials")

        title_lbl=Label(ifrm,text="This is New Account Screen",
                        font=('arial',20,'bold'),bg="white",fg='purple')
        title_lbl.pack()

        name_lbl=Label(ifrm,text="Name",font=('arial',15,'bold'),bg="white")
        name_lbl.place(relx=.1,rely=.1)

        name_entry=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        name_entry.place(relx=.1,rely=.17)
        name_entry.focus()

        email_lbl=Label(ifrm,text="Email",font=('arial',15,'bold'),bg="white")
        email_lbl.place(relx=.5,rely=.1)

        email_entry=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        email_entry.place(relx=.5,rely=.17)
        
        mob_lbl=Label(ifrm,text="Mob",font=('arial',15,'bold'),bg="white")
        mob_lbl.place(relx=.1,rely=.3)

        mob_entry=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        mob_entry.place(relx=.1,rely=.37)

        adhar_lbl=Label(ifrm,text="Adhar",font=('arial',15,'bold'),bg="white")
        adhar_lbl.place(relx=.5,rely=.3)

        adhar_entry=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        adhar_entry.place(relx=.5,rely=.37)
        
        open_btn=Button(ifrm,text="Open Account",font=('arial',20,'bold'),
                       bg="green",bd=5,fg="white",width=12,command=open_acn)
    
        open_btn.place(relx=.4,rely=.6)

    def view():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.1,rely=.2,relwidth=.8,relheight=.6)

        title_lbl=Label(ifrm,text="This is View Account Screen",
                        font=('arial',20,'bold'),bg="white",fg='purple')
        title_lbl.pack()

        uacn=simpledialog.askinteger("View Account","Enter ACN")

        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        query="select * from accounts where acn=?"
        curobj.execute(query,(uacn,))
        tup=curobj.fetchone()
        conobj.close()
        if tup!=None:
            messagebox.showinfo("Details",tup)
        else:
            messagebox.showerror("Details","Acccount does not exist")

    def close():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.1,rely=.2,relwidth=.8,relheight=.6)

        title_lbl=Label(ifrm,text="This is Close Account Screen",
                        font=('arial',20,'bold'),bg="white",fg='purple')
        title_lbl.pack()

        uacn=simpledialog.askinteger("Close Account","Enter ACN")
        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        query="select name,email from accounts where acn=?"
        curobj.execute(query,(uacn,))
        tup=curobj.fetchone()
        conobj.close()
        if tup!=None:
            otp=generator.close_otp()
            text=f"Hello {tup[0]}\nOTP to close you account :{otp}"
            mailing.closeotp_mail(tup[1],text)
            messagebox.showinfo("Close","We have sent otp to close account")
            uotp=simpledialog.askinteger("Close OTP","OTP")
            if otp==uotp:
                conobj=sqlite3.connect(database="bank.sqlite")
                curobj=conobj.cursor()
                query="delete from accounts where acn=?"
                curobj.execute(query,(uacn,))
                conobj.commit()
                conobj.close()
                messagebox.showinfo("Close","Account closed")
            else:
                messagebox.showerror("Close Account","Invalid OTP")
        else:
            messagebox.showerror("Close","Acccount does not exist")

    newacn_btn=Button(frm,text="New Account",font=('arial',20,'bold'),
                       bg="green",bd=5,fg="white",width=12,command=new)
    
    newacn_btn.place(relx=.1,rely=.05)

    viewacn_btn=Button(frm,text="View Account",font=('arial',20,'bold'),
                       bg="powder blue",bd=5,width=12,command=view)
    
    viewacn_btn.place(relx=.4,rely=.05)

    closeacn_btn=Button(frm,text="Close Account",font=('arial',20,'bold'),
                       bd=5,bg="red",fg="white",width=12,command=close)
    
    closeacn_btn.place(relx=.7,rely=.05)


def main_screen():
    def refresh():
        global gen_cap
        gen_cap=generator.captcha()
        cap_lbl.configure(text=gen_cap)


    def forgot():
        frm.destroy()
        forgot_screen()


    def login():
        utype=user_combo.get()
        uacn=acn_entry.get()
        upass=pass_entry.get()
        ucap=cap_entry.get()

        if len(uacn)==0:
            messagebox.showerror("Login","please enter acn")
            return
        if len(upass)==0:
            messagebox.showerror("Login","please enter password")
            return
        if len(ucap)==0:
            messagebox.showerror("Login","please enter captcha")
            return
        

        global gen_cap
        gen_cap=gen_cap.replace(" ","")
        if ucap!=gen_cap:
            messagebox.showerror("Login","Invalid captch")
            return

        if utype=="Admin":
            if uacn=="0" and upass=="admin":
                frm.destroy()
                admin_screen()
            else:
                messagebox.showerror("Login","Invalid Credentials")
        elif utype=="Customer":
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            query="select * from accounts where acn=? and pass=?"
            curobj.execute(query,(uacn,upass))
            tup=curobj.fetchone()
            if tup!=None:
                frm.destroy()
                customer_screen(uacn)
            else:
                messagebox.showerror("Login","Invalid Credentials")
        else:
            messagebox.showerror("Login","Please select user type")

    def reset():
        user_combo.current(0)
        acn_entry.delete(0,"end")
        pass_entry.delete(0,"end")
        cap_entry.delete(0,"end")

        user_combo.focus()

    frm=Frame(root,highlightbackground='black',highlightthickness=2)
    frm.configure(bg="pink")
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.75)

    user_lbl=Label(frm,text="User",font=('arial',20,'bold'),bg="pink")
    user_lbl.place(relx=.3,rely=.1)

    user_combo=Combobox(frm,values=['---Select---','Admin','Customer'],font=('arial',20,'bold'))
    user_combo.place(relx=.4,rely=.1)
    user_combo.current(0)

    acn_lbl=Label(frm,text="ACN",font=('arial',20,'bold'),bg="pink")
    acn_lbl.place(relx=.3,rely=.2)

    acn_entry=Entry(frm,font=('arial',20,'bold'),bd=5)
    acn_entry.place(relx=.4,rely=.2)
    acn_entry.focus()

    pass_lbl=Label(frm,text="PASS",font=('arial',20,'bold'),bg="pink")
    pass_lbl.place(relx=.3,rely=.3)

    pass_entry=Entry(frm,font=('arial',20,'bold'),bd=5,show="*")
    pass_entry.place(relx=.4,rely=.3)
    global gen_cap
    gen_cap=generator.captcha()
    cap_lbl=Label(frm,text=gen_cap,font=('Comic Sans MS',20,'bold'),width=10)
    cap_lbl.place(relx=.45,rely=.4)

    refersh_btn=Button(frm,text="🔄",font=('Comic Sans MS',10,'bold'),
                       bg="powder blue",command=refresh,bd=5)
    refersh_btn.place(relx=.6,rely=.4)

    cap_entry=Entry(frm,font=('arial',20,'bold'),bd=5)
    cap_entry.place(relx=.4,rely=.5)

    login_btn=Button(frm,text="login",font=('arial',20,'bold'),
                       bg="powder blue",bd=5,command=login)
    
    login_btn.place(relx=.43,rely=.6)

    reset_btn=Button(frm,text="reset",font=('arial',20,'bold'),
                       bg="powder blue",bd=5,command=reset)
    
    reset_btn.place(relx=.52,rely=.6)

    forgot_btn=Button(frm,text="forgot password",font=('arial',20,'bold'),
                       bg="powder blue",bd=5,width=17,command=forgot)
    
    forgot_btn.place(relx=.4,rely=.7)

root=Tk()
root.state("zoomed")
root.configure(bg="powder blue")

title_lbl=Label(root,text="Banking Simulator",font=('arial',50,'bold','underline'),
                bg="powder blue")
title_lbl.pack()

datetime=time.strftime("%d-%b-%Y %r")

dt_lbl=Label(root,text=datetime,font=('arial',20,'bold'),bg="powder blue",fg="blue")
dt_lbl.pack()
update_time()

img=Image.open("logo.jpg").resize((200,150))
tkimg=ImageTk.PhotoImage(img,master=root)

logo_lbl=Label(root,image=tkimg)
logo_lbl.place(relx=0,rely=0)

footer_lbl=Label(root,text="Sonu Kumar\n 📱:9999999999",font=('arial',20,'bold'),
                bg="powder blue")
footer_lbl.pack(side='bottom',pady=10)

main_screen()
root.mainloop()