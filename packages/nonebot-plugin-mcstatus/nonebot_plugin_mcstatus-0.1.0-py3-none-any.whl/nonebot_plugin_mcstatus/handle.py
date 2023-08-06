import time
from argparse import Namespace
from mcstatus import MinecraftServer

from nonebot_plugin_mcstatus.data import ServerList

class Handle:

    @classmethod
    async def check(cls,args: Namespace) -> str:
        try:
            ping = await MinecraftServer.lookup(args.address).async_ping()
            status = True
        except:
            status = False

        return (
                f"Address: {args.address}\n"
                f"Status: {'On' if status else 'Off'}\n"
                f"Ping: {ping}" if status else "" 
            )

    @classmethod
    async def add(cls,args: Namespace) -> str:
        try:
            ping = await MinecraftServer.lookup(args.address).async_ping()
            status = True
        except:
            status = False
        ServerList().add_server({args.server:{"address":args.address,"status":status}},args.user_id,args.group_id)

        return "添加服务器成功！"

    @classmethod
    async def remove(cls,args: Namespace) -> str:
        ServerList().remove_server(args.server,args.user_id,args.group_id)

        return "移除服务器成功！"