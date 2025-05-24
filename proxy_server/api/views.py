from django.shortcuts import render
import json
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .store import store,idToContainerId
from .store import PORT
import os
import docker
# Create your views here.

def update_nginx_config(config_file, base_url, conditions):
    data = [
        "events {",
        "    worker_connections 1024;",
        "}",
        "",
        "http {",
        "    map_hash_bucket_size 128; # Adjust as needed",
        "    map $subdomain $upstream {"
    ]
    
    # Add entries for each subdomain in the store
    for subdomain, port in store.items():
        data.append(f'        {subdomain} "{base_url}:{port}";')
    
    # Add the default case
    data.append("    }")
    
    data.extend([
        "",
        "    server {",
        "        listen 80;",
        "        server_name ~^(?<subdomain>[^.]+)\\.localhost$;",
        "",
        "        location / {",
        '            if ($upstream = "") {',
        '                return 404 "No such subdomain";',
        "            }",
        "            proxy_pass $upstream;",
        "            proxy_set_header Host $host;",
        "            proxy_set_header X-Real-IP $remote_addr;",
        "            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;",
        "        }",
        "    }",
        "}"
    ])
    
    with open(config_file, "w") as file:
        file.write("\n".join(data))
    
@csrf_exempt
def webhook(request):
    global PORT
    if(request.method=='POST'):
        print("Webhook called")
        data = json.loads(request.body)
        print(data)
        #data have id and image_name and image_port
        #create a new container
        client = docker.from_env()
        if(data['work']=='redeploy'):
            #make db call to get the port of the container in database
            container_id=idToContainerId[data['id']]
            port=store[data['id']]
            print("ContainerId",container_id)
            print("Port",port)
            #stop the container
            client.containers.get(container_id).stop()
            #remove the container
            client.containers.get(container_id).remove()
            #rerun the container
            c=client.containers.run(data['image_name'],detach=True,ports={data['image_port']:port})
            #update the store and idToContainer
            store[data['id']] = port
            idToContainerId[data['id']]=c.id
            return JsonResponse({"status": "redeployed"})
            
        con=client.containers.run(data['image_name'],detach=True,ports={data['image_port']:PORT})
        #update the store and idToContainer
        store[data['id']] = PORT
        idToContainerId[data['id']]=con.id
        print("store",store)
        print("idToContainerId",idToContainerId)
        PORT+=1
        #update the nginx configuration
         #check nginx file exist or not. if not create the file
        if not os.path.exists("/etc/nginx/nginx.conf"):
            os.system("sudo touch /etc/nginx/nginx.conf")
        if not os.path.exists("./test"):
            os.system("sudo touch ./test")
        update_nginx_config("/etc/nginx/nginx.conf","http://127.0.0.1",store)
        update_nginx_config("./test","http://127.0.0.1",store)
        
        os.system("sudo systemctl restart nginx")#for locally
        #os.system("docker exec nginx_proxy nginx -s reload")#for docker
        return JsonResponse({"status": "deployed"})

@csrf_exempt
def stop_container(request):
    if(request.method=='POST'):
        data = json.loads(request.body)
        client = docker.from_env()
        id=data['id']
        container_id=idToContainerId[id]
        if(container_id==None):
            return JsonResponse({"status": "Some issue in Id as no container is running"})
        #stop the container
        client.containers.get(container_id).stop()
        #remove the container
        client.containers.get(container_id).remove()
        #remove the entry from the store
        del store[id]
        container_id[id]=None
        #update the nginx configuration
        update_nginx_config("/etc/nginx/nginx.conf","http://127.0.0.1",store)
        return JsonResponse({"status": "Container stopped"})

@csrf_exempt
def start_container(request):
    if(request.method=='POST'):
        data = json.loads(request.body)
        client = docker.from_env()
        id=data['id']
        PORT=store[id]
        #create a new container
        #From id get the Image-port and image_name From database
        #currentlly take as input
        con=client.containers.run(data['image_name'],detach=True,ports={data['image_port']:PORT})
        print(con)
        if(con==None):
            return JsonResponse({"status": "Some issue in Id as no container is running"})
        #update the store and idToContainer
        store[data['id']] = PORT
        idToContainerId[data['id']]=con.id
        #update the nginx configuration
        update_nginx_config("/etc/nginx/nginx.conf","http://127.0.0.1",store)
        return JsonResponse({"status": "Container Started"})

