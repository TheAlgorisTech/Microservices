import grpc
import MicroServiceTask_pb2
import MicroServiceTask_pb2_grpc
import time


class ApiServiceClient(object):
    """
    Client for accessing the gRPC login functionality
    """

    def __init__(self):
        # configure the host and the
        # the port to which the client should connect
        # to.
        self.host = 'localhost'
        self.server_port = 46001

        # instantiate a communication channel
        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.server_port))

        # bind the client to the server channel
        self.stub = MicroServiceTask_pb2_grpc.ApiServiceStub(self.channel)

    def post_username_password(self):
        """
        Client function to call the rpc for login
        """

        user = input("Enter Username : ")
        pass_ = input("Enter Password : ")

        username_password_message = MicroServiceTask_pb2.LoginRequest(
            **dict(username=user, password=pass_))
        return self.stub.login(username_password_message)

    def get_hello(self):
        """
        Client function to call the rpc for hello
        """
        print("====================== [ HELLO REQUEST: 'GET'] ===================")
        return self.stub.hello(MicroServiceTask_pb2.NoType())

    def get_logout(self, token_):
        """
        Client function to call the rpc for hello
        """
        print("====================== [ LOGOUT REQUEST: 'GET'] ===================")
        return self.stub.logout(MicroServiceTask_pb2.AuthenticationToken(**dict(http_port = 200, token = token_)))

def run_client():
    try:
        while True:
            print("[ CLIENT LOGIN : 15 MIN ]")
            start_time = time.time()
            curr_client = ApiServiceClient()
            results_token = curr_client.post_username_password()
            if results_token.http_port == 403:
                print('[HTTP 403]: failure')
            else:
                print('[HTTP 200]: success')
                print( curr_client.get_hello())

                while True:
                    end_time = time.time()
                    if round(end_time - start_time) == 15:
                        print("[ TIME OUT : LOGOUT]")
                        print(curr_client.get_logout(results_token.token))
                        break
                break
    except KeyboardInterrupt:
        print('Client Withdrawal')


if __name__ == "__main__":
    run_client()

