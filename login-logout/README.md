# SignIn / SingOut MicroServices
The goal of this small project is to create a small microservice-based system, that is
composed of 3 services:
- ApiService
- AuthService
- HelloService

### Mircroservice Diagram

The system have the following:
- It can handle logins from multiple clients
- After a logout, a Uer must login before calling /hello, otherwise he will get an error
- The clients credentials stored in a sqlite database and a log of the logins logouts stored in the DB
- Each token returned by the AuthService should have an expiration time of 15
minutes
- The system designed in a way that is easy to change a component without affecting the others (low coupling, high cohesion)

# Architecture Overview
Each one of these is a standalone application that respects the SR principle.

## 1. ApiService 
Exposes a REST API and is the only services that is callable by the end-user. 
The ApiService verifies that the user is authenticated and forwards the call
to the correct microservice. It exposes the following REST operations:

  - /login : login to the server by validating the username and password and
  returns an authentication token
    - input:
    - username: string
    - password: string
    - returns: JSON message containing the authorization Token
  - /logout :  logout from the server
    - HTTP header:
    - Authorization: Basic TOKEN
    - /hello: Greats the user by returning the string: “hello [user]” where user is
  replaced by the username used when authenticating
    - input: None
    - returns: JSON
  - HTTP header:
  - Authorization: Basic TOKEN

## 2. AuthService
Handles authentication of end-user. It exposes the following GRPC operations:
  - authenticate (username, password) → token 
  - validate (token) validation result
  
## 3. HelloService 
Contains our “Business logic”, in our case only exposes one GRPC operation
  - hello (string name) → “hello [name]”
  
