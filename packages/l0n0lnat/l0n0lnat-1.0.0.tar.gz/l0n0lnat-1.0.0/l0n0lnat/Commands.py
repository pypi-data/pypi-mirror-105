import argparse
import asyncio
from l0n0lnat.ReverseServer import ReverseServer
from l0n0lnat.ReverseClient import ReverseClient


def run_reverse_server():
    parser = argparse.ArgumentParser(description="创建内网穿透服务器")
    parser.add_argument("listenhost", type=str, help="监听host")
    parser.add_argument("listenport", type=int, help="监听端口")
    args = parser.parse_args()

    async def main():
        server = ReverseServer(args.listenhost, args.listenport)
        await server.start()

    asyncio.get_event_loop().run_until_complete(main())
    asyncio.get_event_loop().run_forever()


def run_reverse_client():
    parser = argparse.ArgumentParser(description="创建内网穿透客户端")
    parser.add_argument("serverhost", type=str, help="监听host")
    parser.add_argument("serverport", type=int, help="监听端口")
    parser.add_argument("serverlistenport", type=int, help="服务器要监听端口")
    parser.add_argument("localhost", type=str, help="本地服务host")
    parser.add_argument("localport", type=int, help="本地服务端口")
    args = parser.parse_args()

    async def main():
        client = ReverseClient(args.serverhost,
                               args.serverport,
                               args.localhost,
                               args.localport,
                               args.serverlistenport)
        await client.start()

    asyncio.get_event_loop().run_until_complete(main())
    asyncio.get_event_loop().run_forever()
