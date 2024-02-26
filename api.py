from flask import Flask
from flask import request
import json
import requests
import principal
import asyncio
import time
import nest_asyncio


app = Flask(__name__)

async def worked_ticket_response(ticket_id,priority,result):
    url = "https://soporte.teledata.com.uy/webservices/service-tickets.php"
    json_data = {
        'ticket_id':ticket_id,
        'priorty':priority,
        'attention_log':str(result)
    }
    json_data = json.dumps(json_data)
    data = {
        'operation':'automatic-sg-ticket',
        'authkey':'u73TkvWFFAKZnUcB9PAgjxhaf3m9ffJh',
        'json_data':json_data
    }

    return requests.post(url=url,data=data,verify=True).json()
    

@app.route("/set-ticket",methods=["POST","GET"])
async def prueba():
    nest_asyncio.apply()
    errors = {}
    print(request.form.get('form-data'))
    if request.form.get('api_key') != "T2Ed4pnvP5$Z5j87#T&m7RqV8qkA":
        errors["api_key"] = "WRONG API KEY"
    if not request.form.get("api_key"):
        errors['api_key'] = "API KEY REQUIRED"
    if not request.form.get("ticket_id"):
        errors['ticket_id'] = "TICKED ID REQUIRED"
    if not request.form.get("priority"):
        errors['priority'] = "ticket priority REQUIRED"
    if not request.form.get("logs"):
        errors['logs'] = "TICKET LOGS REQUIRED"
    
    print(request.method)
    
    if errors != {}:
        f = open('Errors.txt','a')
        log = "ERROR " + errors + "Time " + str(time.localtime()) + "\n"
        f.write(log)
        return errors
   
    
    apiKey = request.form.get("api_key")
    ticketId = request.form.get("ticket_id")
    priority = request.form.get("priority")
    logs = request.form.get("logs")
    
    
    result = await asyncio.gather(principal.manage_email(logs))
    foo = await worked_ticket_response(ticketId,priority,result)
    print(foo)
    print("AA")
    result = json.dumps(result)
    return result

if __name__ == '__main__':
    app.run(port=1111,debug=True,host="0.0.0.0")