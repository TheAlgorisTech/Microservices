
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

    def login(self, request, context):
        print(context)
        print(f"Username {request.username}\nPassword {request.password}")
        authservice = AuthenticationServicer()
        self.results = authservice.authenticate(request,context)
        print(self.results)
        return MicroServiceTask_pb2.LoginResponse(**dict(http_port = self.results.http_port,\
                                                         token = self.results.token))

    def hello(self, request, context):
        """
        Server Sending Greeting Request for authentication & hello service
        """
        print(request.token)
        print(AuthenticationServicer().validate(request, context))

class AuthenticationServicer(MicroServiceTask_pb2_grpc.AuthServiceServicer):
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
        return MicroServiceTask_pb2.VerifiedUser(**{'verifuser': user})

    def validate_token(self, token):
        return User.verify_reset_token(token)

    def checkUserPass(self, usr, pwd):

        return User.query.filter_by(**dict(username=usr, password=pwd)).first()


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
        AuthenticationServicer(), server)
    # bind the server to the port defined above
    server.add_insecure_port('[::]:{}'.format(
        ApiServiceServicer().server_port))
    server.add_insecure_port('[::]:{}'.format(
        ApiServiceServicer().server_port))

    # start the server
    server.start()
    print ('Server running ...')

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
