
import time
import grpc
import concurrent

from concurrent import futures


import MicroServiceTask_pb2
import MicroServiceTask_pb2_grpc

from models import User


class ApiServiceServicer(MicroServiceTask_pb2_grpc.ApiServiceServicer):
    def __init__(self, *args, **kwargs):
        self.server_port = 46001
        self.results = None

    def login(self, request, context):
        print("[Info]:=================== [ AUTHENTICATION SERVICE: CONNECTED ] ===================")
        authservice = AuthServiceServicer()
        print("[Info]:=================== [ CLIENT: INFORMATION ] ===================")
        print(f"Username {request.username}\nPassword {request.password}")
        self.results = authservice.authenticate(request,context)
        return MicroServiceTask_pb2.LoginResponse(**dict(http_port = self.results.http_port,\
                                                         token = self.results.token))

    def hello(self, request, context):
        """
        Server Sending Greeting Request for authentication & hello service
        """
        print("[Info]:===================[ AUTHENTICATION SERVICE: CONNECTED ]===================")
        authservice = AuthServiceServicer()
        try:
            validation = authservice.validate(request = self.results, context = context)
        except:
            print("[Info]:===================[ CLIENT NOT AUTHENTICATED ]===================")
            return MicroServiceTask_pb2.GreetingResponse(greet="CLIENT NOT AUTHENTICATED")
        else:
            # New Hello Service API Instance
            print("[Info]:===================[ CONNECT TO HELLO SERVICE: CONNECTED ]===================")
            helloservice = HelloServiceServicer()
            return helloservice.SayHello(request = validation, context = context)

    def logout(self, request, context):
        authservice = AuthServiceServicer()
        request = self.results
        try:
            validation = authservice.validate(self.results, context)
            print(validation, type(validation))
        except:
            print("[Info]:===================[ LOGGING OUT ]===================")
            return MicroServiceTask_pb2.LogoutResponse(logginout="GOOD BYE!")
        else:
            if validation:
                self.results = None
                print("[Info]:===================[ LOGGING OUT ]===================")
                return MicroServiceTask_pb2.LogoutResponse(logginout="GOOD BYE!")
class AuthServiceServicer(MicroServiceTask_pb2_grpc.AuthServiceServicer):
    def __init__(self, *args, **kwargs):
        self.server_port = 46001

    def authenticate(self, request, context):
        # print(f"Username {request.username}\nPassword {request.password}")
        user = self.checkUserPass(request.username, request.password)
        if user:
            # If User Exists Return AuthorizationToken
            result = dict(token=user.get_reset_token(), http_port=200)
        else:
            result = dict(token="", http_port=403)
        return MicroServiceTask_pb2.AuthenticationToken(**result)

    def validate(self, request, context):
        user = self.validate_token(request.token)
        print("CLIENT", user.username)
        return MicroServiceTask_pb2.VerifiedUser(**dict(verifuser=user.username))

    def validate_token(self, token):
        return User.verify_reset_token(token)

    def checkUserPass(self, usr, pwd):

        return User.query.filter_by(**dict(username=usr, password=pwd)).first()

class HelloServiceServicer(MicroServiceTask_pb2_grpc.HelloServiceServicer):

    def __init__(self, *args, **kwargs):
        self.server_port = 46001

    def SayHello(self, request, context):
        """
        Send Greeting Back To Client 
        """
        print("HELLO", request.verifuser)
        return MicroServiceTask_pb2.GreetingResponse(greet = f"Hello {request.verifuser}, We are getting near the end. ")

def run_server():
    """
    Method starts the gRPC server, and preps
    it for serving incoming connections
    """
    # declare a server object with desired number
    # of thread pool workers.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # This line can be ignored
    MicroServiceTask_pb2_grpc.add_ApiServiceServicer_to_server(
        ApiServiceServicer(), server)
    MicroServiceTask_pb2_grpc.add_AuthServiceServicer_to_server(
        AuthServiceServicer(), server)
    MicroServiceTask_pb2_grpc.add_HelloServiceServicer_to_server(
        HelloServiceServicer(), server)
    # bind the server to the port defined above
    server.add_insecure_port('[::]:{}'.format(
        ApiServiceServicer().server_port))
    server.add_insecure_port('[::]:{}'.format(
        AuthServiceServicer().server_port))
    server.add_insecure_port('[::]:{}'.format(
        HelloServiceServicer().server_port))
    # start the server
    server.start()
    print("[Info]:===================[ STARTING SERVER ]===================")
    try:
        # need an infinite loop since the above
        # code is non blocking, and if I don't do this
        # the program will exit
        while True:
            time.sleep(60 * 60 * 60)
    except KeyboardInterrupt:
        server.stop(0)
        print('Server Stopped ...')


if __name__ == "__main__":
    run_server()
