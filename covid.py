import time
from bs4 import BeautifulSoup
import requests
import win10toast
from win10toast import ToastNotifier
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys

def covid():
    r=requests.get("https://covid19.saglik.gov.tr/")
    soup=BeautifulSoup(r.content)
    s = soup.findAll('script')
    cdata_list=s[-1].string.split()
    text=cdata_list[4]
    list_rakamlar=list(text[2:].split(","))
    sets=dict()
    for i in list_rakamlar:
        temp=i.split(':')
        if(temp[0].__contains__('tarih')):
            sets["tarih"]=temp[1].strip("\"")
        elif(temp[0].__contains__('gunluk_test')):
            sets["test"]=temp[1].strip("\"")
        elif(temp[0].__contains__('gunluk_vaka')):
            sets["vaka"]=temp[1].strip("\"")
        elif(temp[0].__contains__('gunluk_hasta')):
            sets["hasta"]=temp[1].strip("\"")
        elif(temp[0].__contains__('gunluk_vefat')):
            sets["vefat"]=temp[1].strip("\"")
        elif(temp[0].__contains__('gunluk_iyilesen')):
            sets["iyilesen"]=temp[1].strip("\"")
    return sets

def sendmail():
    mail = smtplib.SMTP("smtp.gmail.com",587)
    mail.ehlo()
    mail.starttls()
    mail.login("example@gmail.com", 'your_gmail_password')
    mesaj = MIMEMultipart()
    mesaj["From"] = "edaersu1@gmail.com" # Gönderen
    mesaj["Subject"] = "Günlük Corona İstatistikleri-Python"# Konu
    mesaj["To"] = "person@gmail.com" # Gönderilen
    txt=(f"\n\nTarih: {sets['tarih']}\nTest Sayısı: {sets['test']}\nVaka Sayısı: {sets['vaka']}\nHasta Sayısı: {sets['hasta']}\nVefat Sayısı: {sets['vefat']}\nİyileşen Sayısı: {sets['iyilesen']}")
    body_text = MIMEText(txt, "plain")
    mesaj.attach(body_text)
    mail.sendmail(mesaj["From"], mesaj["To"], mesaj.as_string())
    print("Mail başarılı bir şekilde gönderildi.")
    mail.close()


control=0
while(True):
    time.sleep(5)
    today=datetime.today().strftime('%d.%m.%Y')
    sets=covid()
    if(today==sets["tarih"]):
            sendmail()
            toaster = ToastNotifier()
            toaster.show_toast(f"Tarih: {sets['tarih']}\nTest Sayısı: {sets['test']}\nVaka Sayısı: {sets['vaka']}\nHasta Sayısı: {sets['hasta']}\nVefat Sayısı: {sets['vefat']}\nİyileşen Sayısı: {sets['iyilesen']}")
            break
    else:
        control=control+1
        s=(f" log {str(control)}")
        print("log  ",s)
        if(control==2) | (control==5) | (control==100):
            print("sayac = ",control)
            toaster = ToastNotifier()
            toaster.show_toast(s)
            
