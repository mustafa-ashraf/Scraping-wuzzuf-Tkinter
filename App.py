####################################################### S T A R T  ####################################################
# Most important
import pandas as pd
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
# other
import os
import requests
import warnings
warnings.filterwarnings("ignore")
#!pip install bs4
from bs4 import BeautifulSoup
import time
import math
import re
# selenium 
import time
from PIL import Image
from selenium import webdriver
import selenium.webdriver.common.keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from chromedriver_py import binary_path


##########################################################################################################







#############################################################################################################################
# enter job and get the url
def get_url(job):
    url= "https://wuzzuf.net/search/jobs/?q="+str(job)
    return url
#############################################################################################################################
# get the number of pages 
def get_pages_no(url):
    request = requests.get(url)
    data = request.text
    soup = BeautifulSoup(data)
    n = soup.find("li", {"class":"css-8neukt"}).text
    n = n.split(" ")
    number_of_pages = int(n[-1])/int(n[3])
    number_of_pages = math.ceil(number_of_pages)
    return number_of_pages
#############################################################################################################################
def all_scrap_function(job_name):
        titles = []
        Requirments = []
        Experince = []
        links = []
        Company_name = []
        country = []
        city = []
        address = []
        job_since = []
        company_link = []
        full_part = []

        base_url = get_url(job_name)
        pages = get_pages_no(base_url)
        for i in range(0,pages+1):
                url = base_url+"&start="+str(i)
                request = requests.get(url)
                data = request.text
                soup = BeautifulSoup(data)
                
                x = soup.findAll("h2",{"class":"css-m604qf"})
                for i in x:
                        titles.append(i.text.split("-")[0].strip())

                x = soup.findAll("div",{"class":"css-y4udm8"})
                for i in x:
                    Requirments.append(",".join(i.text.split("·")[2:]))
                
                x = soup.findAll("div",{"class":"css-y4udm8"})
                for i in x:
                    Experince.append(i.text.split("·")[1])

                x = soup.findAll("h2",{"class":"css-m604qf"})
                for i in x:
                    links.append(("https://wuzzuf.net"+i.find("a")["href"]))

                x = soup.findAll("div",{"class":"css-d7j1kk"})
                for i in x:
                    Company_name.append(i.find("a").text.replace("-","").strip())

                x = soup.findAll("span",{"class":"css-5wys0k"})
                for i in x:
                    country.append(i.text.split(",")[-1])


                x = soup.findAll("span",{"class":"css-5wys0k"})
                for i in x:
                    city.append(i.text.split(",")[-2])


                x = soup.findAll("span",{"class":"css-5wys0k"})
                for i in x:
                    address.append(i.text.split(",")[0])


                x = soup.findAll("div",{"class":"css-4c4ojb"})
                x=x+soup.findAll("div",{"class":"css-do6t5g"})
                for i in x:            
                    job_since.append(i.text.split(",")[0])
                    
                x = soup.findAll("div",{"class":"css-d7j1kk"})
                for i in x:
                    if(i.find("a").text =="Confidential -" ):
                        company_link.append("Confidential")
                    else:
                        company_link.append(i.find("a")["href"])
                  
                
                x = soup.findAll("div",{"class":"css-1lh32fc"})
                for i in x:
                    full_part.append(i.text)
                    
                    
        
        JOB_DESCRIPTION = []
        JOB_REQUIRMENT = []
        jobs_skills =[]
        # Connection
        DRIVER_PATH = "chromedriver.exe"
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1200")
        driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
        # collecting data
        for i in links:
                jobaya_skils = []
                url = i
                driver.get(url)
                job_description_and_job_requirement = driver.find_elements(By.CLASS_NAME,"css-ghicub")
                if(len(job_description_and_job_requirement)>1):
                        JOB_DESCRIPTION.append(job_description_and_job_requirement[0].text)
                        JOB_REQUIRMENT.append(job_description_and_job_requirement[1].text)
                elif (len(job_description_and_job_requirement)==1):
                        JOB_DESCRIPTION.append(job_description_and_job_requirement[0].text)
                        JOB_REQUIRMENT.append("No")
                job_skills = driver.find_elements(By.CLASS_NAME,"css-158icaa")
        
                jobaya_skils = []
                for i in job_skills:

                    jobaya_skils.append(i.text)
                jobs_skills.append(jobaya_skils)
        
        length = len(company_link)
        company_logo = []
        for i in range(0,length):
            if(Company_name[i]=="Confidential"):
                company_logo.append("Confidential")
            else:
                url = company_link[i]
                request = requests.get(url)
                data = request.text
                soup = BeautifulSoup(data)
                company_logo.append(soup.find("img")["src"])
        
        # converting lists to a data frame 
        df = pd.DataFrame(titles,columns=["titles"])
        df["Requirments"] = Requirments
        df["Experince"] = Experince
        df["links"] = links
        df["Company_name"] = Company_name
        df["country"] = country
        df["city"] = city
        df["address"] = address
        df["job_since"] = job_since
        df["company_link"] = company_link
        df["full_part"] = full_part
        df["job_description"] = JOB_DESCRIPTION
        df["job_requirement"] = JOB_REQUIRMENT
        df["jobs_skills"] = jobs_skills
        df["company_logo"] = company_logo
        return df
#############################################################################################################################
def outer_scrap_function(job_name):
        titles = []
        Requirments = []
        Experince = []
        links = []
        Company_name = []
        country = []
        city = []
        address = []
        job_since = []
        company_link = []
        full_part = []

        base_url = get_url(job_name)
        pages = get_pages_no(base_url)
        for i in range(0,pages+1):
                url = base_url+"&start="+str(i)
                request = requests.get(url)
                data = request.text
                soup = BeautifulSoup(data)
                
                x = soup.findAll("h2",{"class":"css-m604qf"})
                for i in x:
                        titles.append(i.text.split("-")[0].strip())

                x = soup.findAll("div",{"class":"css-y4udm8"})
                for i in x:
                    Requirments.append(",".join(i.text.split("·")[2:]))
                
                x = soup.findAll("div",{"class":"css-y4udm8"})
                for i in x:
                    Experince.append(i.text.split("·")[1])

                x = soup.findAll("h2",{"class":"css-m604qf"})
                for i in x:
                    links.append(("https://wuzzuf.net"+i.find("a")["href"]))

                x = soup.findAll("div",{"class":"css-d7j1kk"})
                for i in x:
                    Company_name.append(i.find("a").text.replace("-","").strip())

                x = soup.findAll("span",{"class":"css-5wys0k"})
                for i in x:
                    country.append(i.text.split(",")[-1])


                x = soup.findAll("span",{"class":"css-5wys0k"})
                for i in x:
                    city.append(i.text.split(",")[-2])


                x = soup.findAll("span",{"class":"css-5wys0k"})
                for i in x:
                    address.append(i.text.split(",")[0])


                x = soup.findAll("div",{"class":"css-4c4ojb"})
                x=x+soup.findAll("div",{"class":"css-do6t5g"})
                for i in x:            
                    job_since.append(i.text.split(",")[0])
                    
                x = soup.findAll("div",{"class":"css-d7j1kk"})
                for i in x:
                    if(i.find("a").text =="Confidential -" ):
                        company_link.append("Confidential")
                    else:
                        company_link.append(i.find("a")["href"])
                  
                
                x = soup.findAll("div",{"class":"css-1lh32fc"})
                for i in x:
                    full_part.append(i.text)
                    
        df = pd.DataFrame(titles,columns=["titles"])
        df["Requirments"] = Requirments
        df["Experince"] = Experince
        df["links"] = links
        df["Company_name"] = Company_name
        df["country"] = country
        df["city"] = city
        df["address"] = address
        df["job_since"] = job_since
        df["company_link"] = company_link
        df["full_part"] = full_part
        return df
        print("Done")

def determine(entry_1_var,var):
    #Loading = Label(root, text="Loading...",width=30,font=("bold", 12)).place(x=120,y=600)
    if(var==1):
            x = outer_scrap_function(entry_1_var)
            file_name = entry_1_var+".csv"
            x.to_csv(file_name) 
    elif(var==2):
            x = all_scrap_function(entry_1_var)
            file_name = entry_1_var+".csv"
            x.to_csv(file_name)
    Successfuly = Label(root, text="Successfuly Done",width=30,font=("bold", 30)).place(x=40,y=700)
    
  
# Define a function to return the Input data

###################################################################################################################



from tkinter import*
root = Tk()

root.geometry('800x800')
root.title("Scrapping")

label_0 = Label(root, text="Scrapping From Wuzzuf", width=20,font=("bold", 40))
label_0.place(x=90,y=53)

label_1 = Label(root, text="Enter Job Title:",width=20,font=("bold", 20))
label_1.place(x=50,y=200)

entry_1_var = StringVar()
entry_1 = Entry(root,width = 25,font=("bold", 20))
#entry_1 = Entry(root,text=" ",font=('calibre',18, 'bold'),textvariable=entry_1_var)
entry_1.place(x=350,y=205)

# Choosing between fast and slow scrapping ways
label_3 = Label(root, text="Way of collecting the data:",width=20,font=("bold", 20))
label_3.place(x=120,y=300)
var = IntVar()
Radiobutton(root, text="Fast",padx = 5, variable=var, value=1,font=("bold", 20)).place(x=120,y=360)
Radiobutton(root, text="slow",padx = 20, variable=var, value=2,font=("bold", 20)).place(x=105,y=430)



label_5 = Label(root, text="It collect some of job features not all",width=30,font=("bold", 12)).place(x=280,y=370)

label_6 = Label(root, text="It collect all of job features",width=30,font=("bold", 12)).place(x=250,y=440)

label_7 = Label(root, text="It may take few minutes",width=20,font=("bold", 8)).place(x=295,y=460)

#print(str(entry_1_var.get()))
#print(type(var))
#x = entry_1_var.get()
#y = var.get()
def get_data():
    e = entry_1.get()
    a = var.get()
    determine(e,a)

Button(root, text='Download CSV File',width=20,command=get_data,bg='red',fg='white',font=("bold", 15)).place(x=100,y=550)



root.mainloop()










#Loading = Label(root, text="Loading...",width=30,font=("bold", 12)).place(x=120,y=600)
#Successfuly = Label(root, text="Successfuly Done",width=30,font=("bold", 30)).place(x=40,y=700)
#Successfuly = Label(root, text="Successfuly Done",width=30,font=("bold", 30)).place(x=40,y=650)
#Download Csv Button
#Loading = Label(root, text="Loading...",width=30,font=("bold", 12)).place(x=120,y=600)
#Button(root, text='Slow',width=20,bg='red',fg='white',font=("bold", 15)).place(x=400,y=550)
#Button(root, text='Fast',width=20,bg='red',command=outer_scrap_function("deep learning"),fg='white',font=("bold", 15)).place(x=100,y=550)
#Button(root, text='Slow',width=20,bg='red',command=all_scrap_function("deep learning"),fg='white',font=("bold", 15)).place(x=400,y=550)
#Successfuly = Label(root, text="Successfuly Done",width=30,font=("bold", 30)).place(x=40,y=650)
#Successfuly = Label(root, text="Successfuly Done",width=30,font=("bold", 30)).place(x=40,y=650)
#Data1 = Button(root, text='Fast',width=20,bg='red',command=outer_scrap_function(entry_1_var),fg='white',font=("bold", 15)).place(x=100,y=550)
#Data2 = Button(root, text='Slow',width=20,bg='red',command=all_scrap_function(entry_1_var),fg='white',font=("bold", 15)).place(x=400,y=550)
#print(entry_1_var)
# command = detrmine
# command=outer_scrap_function(entry_1_var),
# # it is use for display the registration form on the window
# ,command=outer_scrap_function(entry_1_var)
#command=all_scrap_function(entry_1_var),
#Download Csv Button
#Loading = Label(root, text="Loading...",width=30,font=("bold", 12)).place(x=120,y=600)
#Data1 = Button(root, text='Load Data',width=20,bg='red',fg='white',font=("bold", 15)).place(x=100,y=550)
#Data2 = Button(root, text='Download CSV',width=20,bg='red',fg='white',font=("bold", 15)).place(x=400,y=550)
#Successfuly = Label(root, text="Successfuly Done",width=30,font=("bold", 30)).place(x=40,y=650)            

############################################################## THE END #######################################################