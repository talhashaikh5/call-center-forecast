# Installation

 - Install [docker](https://docs.docker.com/engine/install/)
 - Build image: `sudo docker build --tag forecast_api` .
 - Run container: `sudo docker run -d -p 3001:3001 forecast_api`
Now you should have a service running at <server_public_ip>:3001. To test the service you can try 
`curl http://<server_public_ip>:3001/test` . 

# Api Documentation (Postman share link)

https://www.getpostman.com/collections/f4544ff1c6b1a89450e9