import random

def captcha():
    nums = list(range(10))
    lettes = list("abcdefghijklmnopqrstuvwxyz")
    cap = random.choices(nums+nums+nums+lettes,k=4)
    s = ""
    for i in cap:
        s += str(i)
        s += " "
    return s

def password():
    nums = list(range(10))
    lettes = list("abcdefghijklmnopqrstuvwxyz")
    pwd = random.choices(nums+nums+nums+lettes,k=4)
    s = ""
    for i in pwd:
        s += str(i)
    return s


def close_otp():
    otp = random.randint(1000,9999)
    return otp


def forgot_otp():
    otp = random.randint(1000,9999)
    return otp
