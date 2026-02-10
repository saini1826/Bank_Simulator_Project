import gmail
email="xyz@gmail.com" # write your gmail id
pwd="xyz"             # write your app password

def openacn_mail(to,text):
    con = gmail.GMail(email,pwd)
    msg = gmail.Message(to=to,subject="Account opened in ABC Bank",text=text)
    con.send(msg)

    def closeotp_mail(to,text):
    con = gmail.GMail(email,pwd)
    msg = gmail.Message(to=to,subject="OTP to close account",text=text)
    con.send(msg)

def forgototp_mail(to,text):
    con = gmail.GMail(email,pwd)
    msg = gmail.Message(to=to,subject="OTP to recover password",text=text)
    con.send(msg)