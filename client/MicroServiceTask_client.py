import grpc
import MicroServiceTask_pb2
import MicroServiceTask_pb2_grpc


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
        return self.stub.hello(MicroServiceTask_pb2.NoType())

def run_client():
    try:
        while True:
            curr_client = ApiServiceClient()
            results_token = curr_client.post_username_password()
            if results_token.http_port == 403:
                print('[HTTP 403]: failure')
            else:
                print('[HTTP 200]: success')
                res = dict(token=results_token.token,\
                           http_port=results_token.http_port)
                curr_client.get_hello()
    except KeyboardInterrupt:
        print('Client Withdrawal')

if __name__ == "__main__":
        curr_client = ApiServiceClient()
        results_token = curr_client.post_username_password()
        print(type(results_token))
        print(results_token.http_port, results_token.token)
        print(results_token)

