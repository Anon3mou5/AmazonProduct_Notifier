from datetime import datetime
import time
import os
import clx.xms
import requests
import smtplib 
import re as regularexpression
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
from apscheduler.schedulers.background import BackgroundScheduler


from selenium import webdriver
from selenium.webdriver.chrome.options import Options

   
fromaddr = "RECIEVER MAIL ID"
toaddr = "SENDER MAIL ID"

   


msg = MIMEMultipart()  
# storing the senders email address   
msg['From'] = fromaddr   
# storing the receivers email address  
msg['To'] = toaddr   
# storing the subject  
msg['Subject'] = "YOUR PRODUCt IS BACK IN STORE"
# string to store the body of the mail 
body = "THIS IS THE LINK" 
# attach the body with the msg instance 
msg.attach(MIMEText(body, 'plain'))   


client = clx.xms.Client(service_plan_id='###PLANID', token='###TOKEN')
create = clx.xms.api.MtBatchTextSmsCreate()
create.sender = '#SENDER NUMBER'
create.recipients = {'#RECIEVERNUMBER'}
      
# terminating the session 
import urllib.request as rq
from bs4 import BeautifulSoup

key="span"
val="priceblock_ourprice"
clss="a-size-medium a-color-price priceBlockBuyingPriceString"
websitelist = []
def tick():
    
 for m in websitelist:

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    }
    res = requests.get(m, headers=headers,proxies={'http':'','https':''})
#    
    soup = BeautifulSoup(res.content, 'html5lib')
    productname = soup.find("span",attrs={"id":"productTitle","class":"a-size-large product-title-word-break"})
    priceTablerow = soup.find(key,attrs={"id":val,"class":clss})
    priceTablerow2 = soup.find(key,attrs={"id":"priceblock_saleprice","class":"a-size-medium a-color-price priceBlockSalePriceString"})


    if(priceTablerow):
           pass
    else:
       priceTablerow=priceTablerow2
    if(priceTablerow ):
       pricebytes=priceTablerow.text.strip()
       productnm=productname.text.strip()
       pricey= str((pricebytes).encode('utf8'))
       pricey=pricey.split(',')
       pu=pricey[1:]
       price=""

       for i in range(1,len(pricey)):
            if(i==len(pricey)-1):
              price=price+pricey[i][:-1]
            else:
              price=price+pricey[i]+","
       price=pricey[0][-2:]+","+price

       
       print("Product name :" + productnm)
       print("Product price : "+ price)
    ######################   Sending the email
       
       msg = MIMEMultipart()  
# storing the senders email address   
       msg['From'] = fromaddr   
# storing the receivers email address  
       msg['To'] = toaddr   
# storing the subject  
       msg['Subject'] = str(productnm)+"  is back on Store for RS " + str(price)
# string to store the body of the mail 
       body = str(productnm)+"  is back on Store, here is the link : " + m 
# attach the body with the msg instance 
       msg.attach(MIMEText(body, 'plain'))   
# Converts the Multipart msg into a string     
       text = msg.as_string() 
       
       s = smtplib.SMTP('smtp.gmail.com', 587) 
  
# start TLS for security 
       s.starttls() 
  
# Authentication 
       s.login(fromaddr, "SENDER_MAIL_PASSWORD") 
  
       s.sendmail(fromaddr, toaddr, text) 

       s.quit() 

    #####################    Sending to mobile phone
       try:
        create.body = str(productnm)+"  is back on Store, here is the link : " + m 
        batch = client.create_batch(create)  
       except (requests.exceptions.RequestException,clx.xms.exceptions.ApiException) as ex:
        print('Failed to communicate with XMS: %s' % str(ex))

    else:
        print("\nProduct link \n"+ m + "\n Out of stock\n")


if __name__ == '__main__':   
    scheduler = BackgroundScheduler()
    scheduler.add_job(tick, 'interval', seconds=30)
    scheduler.start()
    while(1):
        n=int(input("1 to add the website OR 2 to exit:\n"))
        if(n==1):
         websitelist.append(str(input("Enter the link:\n"))) 
        else:
         break

    