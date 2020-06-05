# Microservice-Based Systems

## Examples
1. [Login Logout Services](https://github.com/Fayssal404/Microservices/tree/master/login-logout)


### G-RPC
- Let clients get information about features on their route
- Create summary of clients route
- Exchange on between server & clients
- Compiling generate either :
	- Base class for service, writing business specific-code
	- Client class to use for reliable access to the service
- Messages are much smaller than HTTP-based (RESTFul Service)
- Protocol Buffers is the interface definition language (IDL) used in __G-RPC__

<!---
[//]:(generating server skeleton & client stub)
[//]:(implementing a service business logic)
[//]:(running grpc server with the implemented service)
[//]:(invoking the service through the GRPC client Application)
--->

### G-RPC Service Interface
- Allow *Clients* to call remotely, methods parameters & message formats to use, when invoking methods
- Service definitions are recorded as *protocol buffers*
- Identify the business capabilities of the service

Consists of :
- Methods __G-RPC__ service makes available
- Data structure of the parameters & methods returned values

For each service in the .proto, three elements are generated:
- Stub : used by the client to connect to __G-RPC__
- Servicer : used by server to implement a __G-RPC__ service
- Registration Function : user to register a servicer with grpc.Server object 

## G-RPC Messages
- Each Message has a position in the service & scalar type (i.e data type)

### G-RPC File Structure
- Proto File : 
	- Contains all the service definitions for the current package
	- Allow to specify the interface of the server
	- Must be compliant with Google's Protocol Buffers specifications (a.k.a ProtoBuf)
- gCPR Server : used for servicing incoming requests
- gCPR Client : This is distributed out to other people so that they can access our server using it


## HTTP Methods
- Web applications use different HTTP methods when accessing URLs
- Two HTTP methods we will use:
	- GET : used to retrieve information from the given server using a given URL
	- POST : used to send data to the server using HTML forms
- "route" only anwser for 'GET' requests

