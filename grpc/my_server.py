import items_pb2_grpc
import items_pb2
from concurrent import futures
import grpc
import asyncio

class MyServicer(items_pb2_grpc.MessageServiceServicer):
    
    def UnaryGetMessage(self, request, context):
        response_message = request.message + " RESPONSE"
        return items_pb2.MessageResponse(message=response_message)

    def StreamGetMessage(self, request_iterator, context):
        messages = []
        for message in request_iterator:
            messages.append(message.message)
        for num in range(1, 10):
            yield items_pb2.MessageResponse(message=",".join(messages) + f" {str(num)} RESPONSE")

    def ClientStreamGetMessage(self, request_iterator, context):
        messages = []
        for message in request_iterator:
            messages.append(message.message)
        return items_pb2.MessageResponse(message=",".join(messages) + " RESPONSE")

    def ServerStreamGetMessage(self, request, context):
        for num in range(1,10):
            yield items_pb2.MessageResponse(message = f"{request.message} {str(num)} RESPONSE")
    
async def serve(timeout=300):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    items_pb2_grpc.add_MessageServiceServicer_to_server(
        MyServicer(), server)
    server.add_insecure_port('[::]:50051')
    
    print("About to start the server...")
    server.start()
    server.wait_for_termination(timeout=timeout)
    print("Timeout: about to stop the server...")
    server.stop(grace=None)
  

if __name__ == "__main__":
    asyncio.run(serve())
    