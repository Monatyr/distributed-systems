from http import server
from re import S
from telnetlib import SE
from server.server import Server


if __name__ == "__main__":
    server = Server()
    server.run()