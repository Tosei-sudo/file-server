
from decsvr import DecServer
import router

server = DecServer.DecServer(8000, True)

server.incude_router(router.router)

server.start()