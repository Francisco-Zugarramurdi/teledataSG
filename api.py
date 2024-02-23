from flask import Flask
from flask import request
import json
import requests
import principal
import asyncio
import time
import nest_asyncio

app = Flask(__name__)

def worked_ticket_response(ticket_id,priority,result):
    url = "https://soporte.teledata.com.uy/webservices/service-tickets.php?operation=automatic-sg-ticket/"
    data = {
        "authkey":"u73TkvWFFAKZnUcB9PAgjxhaf3m9ffJh",
        "ticket_id":ticket_id,
        "priorty":priority,
        "attention_log":result
    }
    requests.post(url,data)
    

@app.route("/set-ticket",methods=["POST","GET"])
async def prueba():
    nest_asyncio.apply()
    errors = {}
    
    if request.args.get('api_key') != "T2Ed4pnvP5$Z5j87#T&m7RqV8qkA":
        errors["api_key"] = "WRONG API KEY"
    if not request.args.get("api_key"):
        errors['api_key'] = "API KEY REQUIRED"
    if not request.args.get("ticket_id"):
        errors['ticket_id'] = "TICKED ID REQUIRED"
    if not request.args.get("priority"):
        errors['priority'] = "ticket priority REQUIRED"
    if not request.args.get("logs"):
        errors['logs'] = "TICKET LOGS REQUIRED"
    
        
    
    if errors != {}:
        return errors
   
    
    apiKey = request.args.get("api_key")
    ticketId = request.args.get("ticket_id")
    priority = request.args.get("priority")
    logs = request.args.get("logs")
    data = {
        "api_key":apiKey,
        "ticket_id":ticketId,
        "priority":priority,
        "logs":logs
    }
    result = await asyncio.gather(principal.manage_email(logs))

    worked_ticket_response(ticketId,priority,result)
    result = json.dumps(result)
    return result

if __name__ == '__main__':
    app.run(port=1111,debug=True,host="0.0.0.0")