from core.FFxivPythonTrigger import PluginBase
from aiohttp import web
import asyncio

host = "127.0.0.1"
port = 2019
loop = asyncio.get_event_loop()


class NamazuServer(PluginBase):
    name = "Namazu Server"

    async def command(self, request):
        try:
            self.FPT.api.Magic.macro_command(await request.text())
        except Exception as e:
            return web.Response(body=str(e).encode('utf-8'))
        return web.Response(body="success".encode('utf-8'))

    def plugin_onload(self):
        self.app = web.Application(loop=loop)
        self.app.add_routes([web.post('/command', self.command)])
        runner = web.AppRunner(self.app)
        loop.run_until_complete(runner.setup())
        self.site = web.TCPSite(runner, host, port)

    def plugin_onunload(self):
        asyncio.run(self.app.shutdown())

    async def plugin_start(self):
        await self.site.start()
