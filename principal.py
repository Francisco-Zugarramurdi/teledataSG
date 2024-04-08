# from google.oauth2.credentials import Credentials
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# from email.message import EmailMessage
import vt
# import os
import re 
# import quickstart
# import base64
# import email
# import time
import asyncio
import time


#Mail Teledata: sgteledata@gmail.com BORRAR     
#Contra mail teledata: !sttdt3l3d4t4*  BORRAR
#Me preocupa el hecho de en que formato me van a llegar los logs y como va a hacer el smart para identifcarlos...
fVariables = open("variables.json","r")
variables = eval(fVariables.read())
apiKey = variables['api_key']
#REGEXs:
regex = """http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"""
regex2 = """qname\s*(\S+)"""
regex3 = """Host Name\s*(\S+)"""
regexTrigger = "Very-Risky-Destination-Detection-By-Endpoint*"
regexTrigger2 = "Host-Detection-IOC-By-Endpoint*"
regexLogId = "Log ID\s*(\S+)"
regexSender = "\<(.*?)\>"
logRegex = r'\bDevice\b(?! Name)(?! ID)(?! Type)'
actionRegex = 'Action	\s*(\S+)'

def get_logs(allLogs):
    original = allLogs
    result = re.finditer(logRegex,allLogs)
    indices = [m.start(0) for m in result]
    logs = []
    print ("there are " + str(len(indices)) + "logs")
    if(len(indices) == 1):
        logs.append(original)
        return logs
    for i in range(0,len(indices),1):
        if(i!= 0):
            log = allLogs[indices[i-1]:indices[i]]
            logs.append(log)
        if(i == len(indices)):
            log = allLogs[indices[i]:len(allLogs)]
            logs.append(log)
    print("ALL LOGS")
    for x in logs:
        print("LOG")
        print(x)
        print("END LOG")
    return logs

def writeCurrentKey(key):
    apiFile=open('currentApiKey','w')
    apiFile.write(key)
def readCurrentKey():
    apiFile= open('currentApikey','r')
    return apiFile.readline()


def api_quota_exceeded(apikey):
    print("Apikey")
    print(apikey)
    if(apikey == variables['api_key']):
       writeCurrentKey(variables['api_key2'])
    else: 
        if(apikey == variables['api_key2']):
            writeCurrentKey(variables['api_key3'])
        else: 
            if (apikey == variables['apiKey3']):
                writeCurrentKey(variables['api_key4'])
            else:
                if(apikey == variables['apiKey4']):
                    writeCurrentKey(variables['api_key'])

def is_url_log(msg):
    result = re.findall(regexTrigger,msg)
    if (result == []):
        result += re.findall(regexTrigger2,msg)
    if (result == []):  
        return False
    return True

def trunk_duplicates(list):
    result = []
    for x in list:
        if x not in result:
            result.append(x)
    return result

def get_urls (txt):  
    print("Getting URL's from logs")
    print(txt)
    result = re.findall(regex,txt) 
    result += re.findall(regex2,txt)
    result += re.findall(regex3,txt)
    print("Log ID: ",re.findall(regexLogId,txt))
    i = 0
    for x in result:
        result[i] = x.replace("http://","")
        result[i] = result[i].replace("www.","")
        i = i+1
    print("Result")
    print(result)
    if(result):
        return(result[0])
    else: return "Null"

# def send_message(body,sender,reciver,subject):
#     SCOPES = ['https://www.googleapis.com/auth/gmail.modify'] 
#     creds = Credentials.from_authorized_user_file("token.json", SCOPES)
#     try:
#         service = build("gmail", "v1", credentials=creds)
#         message = EmailMessage()

#         message.set_content(body)
#         message["To"] = reciver
#         message["From"] = sender
#         message["Subject"] = "re: {}".format(subject)
        
#         encoded_msg = base64.urlsafe_b64encode(message.as_bytes()).decode()
#         create_msg = {"raw": encoded_msg}
        
#         service.users().messages().send(userId = "me",body=create_msg).execute()
#         print("Email Sent")
        
#     except HttpError as err:
#         print("An error occurred while trying to send the email",err)
                
# def get_unread_emails():
#     # Archivo de API Gooogle para Iniciar config en caso de que no este
#     SCOPES = ['https://www.googleapis.com/auth/gmail.modify'] 
#     creds = Credentials.from_authorized_user_file("token.json", SCOPES) 
#     try:
#         service = build("gmail", "v1", credentials=creds) 
        
#         print("Getting unread emails...")
        
#         results = service.users().messages().list(userId='me',labelIds=['INBOX'],q='is:unread',maxResults=20).execute() 
        
#         mails = [] 
#         if results['resultSizeEstimate'] != 0:
        
#             for msg in results['messages']: 
                
#                 service.users().messages().modify(userId= 'me',id=msg['id'],body={'removeLabelIds':['UNREAD']}).execute()
#                 mail = service.users().messages().get(userId='me',id=msg['id'],format='raw').execute() 
#                 metadata = service.users().messages().get(userId='me',id=msg['id']).execute()
                
#                 headers = metadata['payload']['headers']
                
#                 for h in headers:
#                     if h['name'] == 'From':
#                         sender = re.findall(regexSender,h['value'])[0]
#                     if h['name'] == 'Subject':
#                         subject = h['value']
                

#                 msg_str = base64.urlsafe_b64decode(mail['raw'].encode("utf-8")).decode("utf-8") 
#                 mime_msg = email.message_from_string(msg_str) 
                
#                 if(mime_msg.is_multipart()): # Si es multipart hay que recorrer todo el msg    
#                     for x in mime_msg.get_payload():
#                         if(is_url_log(x.get_payload())): ## Verificamos que sea un msg del tipo para analizar
#                             mails.append([x.get_payload(),sender,subject]) 
#                             break
#                 else:
#                     if(is_url_log(mime_msg.get_payload())):
#                         mails.append([mime_msg.get_payload(),sender,subject]) 
#             return mails 
#         else:
#             print("There are not unread emails")
#             return []
#     except HttpError as err:
#         print(err) 



async def api_vt(x,action):  
    apiKey=readCurrentKey()
    print(apiKey)
    client = vt.Client(apiKey) 
    
    print("Analyzing urls")
    result = "" 
    print(x)
    url_id = vt.url_id(x)
    try:
        url = client.get_object("/urls/{}",url_id) 
        if(url.last_analysis_stats.get("malicious") >= 1):
            result += "action:"
            result += action
            result += "-" + x
            result += "-<b>Maliciosa</b>"
            result += url.categories[list(url.categories.keys())[0]]
            result += '<br>'
        else:
            result += "action:"
            result += action
            result += "-" + x
            result += "-No maliciosa"
            result += "<br>"
    except Exception as e: # Si da error el 99% de los casos significa que simplente la URL no esta catalogada por VT
        try:
            a , b = e.args 
            if(a!="QuotaExceededError"):
                result += "action:"
                result += action
                result += "-" + x
                result += " -Sin catalogar"  
                result += "<br>"
            else:
                result += "action:"
                result += action
                result += "-" + x
                result += "-<b> API Quota Exceeded-</b>"
                result += "<br>"
                api_quota_exceeded(apiKey)
                if(apiKey!=variables['api_key4']):
                    return await api_vt(x,action)
                
        except:
            print("")
        print("action:"+ action +"url" + x)
                    
            

            
        
         
    client.close()  
    f = open('Resultados.txt','a')
    log = "Result " + result + "Time " + str(time.localtime()) + "\n"
    f.write(log)
    return result

async def manage_email(email):
    # return "MALA"
    if(is_url_log(email)):
        logs = get_logs(email)
        result = list()
        for log in logs:
            if(is_url_log(log)):
                urls = get_urls(log)
                action = re.findall(actionRegex,log)
                if(urls != "Null" and action):
                    result.append(await asyncio.gather(api_vt(urls,action[0])))
                    
     
        return result
    # send_message(result,"seguridadgestionadatd@gmail.com",email[1],email[2])
    return("not able to analyze ticket")

#Potencialmente se puede usar la API de shodan para tambien Gestionar los tickets de login (Pero me parece que hay que finiquitar esto bien antes)
#Potencialmente se puede agregar un workaround que utilice varias API_KEYS de VT en caso que no se pueda pagar la API Premiumn (No se ni proponer esto)
#Potencialmente se puede agregar un analisis mayor de los logs action, ip de origen etc (No se que tan util seria la vdd)
#La verdad no se que mucho mas hacer el programa no se puede hacer mucho mas robusto hasta que sepa como llegan los emails y como le convienen recibirlos al WS...

#Agregar los regex para que sirva para muuuchos logs
#Agregar el cambio de prioridad 

# def main():
#     if not (os.path.exists("token.json")):
#         quickstart.main()
#         print("Token json does not exist, running quickstart.py")
#     while 1 != 2:
#         print("Getting emails...")
#         # mails = get_unread_emails()
#         if (mails != []):
#             print("Analyze URLs from emails")
#             for x in mails:
#                 manage_email(x)
    
#         time.sleep(2)
#     os.system("pause")
          
# main()

