from concurrent.futures.thread import ThreadPoolExecutor

from .utils.SetAdmin import check
from .utils.AttrContainer import AttrContainer
from .utils.Logger import log
import asyncio
import atexit
import inspect
import traceback
from functools import partial

from .utils.normalToAsync import normal_to_async

check()

loop = asyncio.get_event_loop()
loop.set_default_executor(ThreadPoolExecutor(max_workers=99))

class FFxivPythonTrigger(object):
    def __init__(self, plugins=None):
        self.plugins = dict()
        self.api = AttrContainer()
        self.plugin_tasks = list()
        self.events = dict()
        atexit.register(self.close)
        try:
            self.register_plugins(plugins if plugins is not None else [])
        except:
            log('error occurred during initialization')
            log(traceback.format_exc())
            self.close()
            raise Exception('error occurred during initialization')

    def register_plugins(self, plugins):
        for plugin in plugins:
            log("start register plugin: %s" % plugin.name)
            self.register_plugin(plugin)
            log("register plugin success: %s" % plugin.name)

    def register_plugin(self, plugin):
        temp_plugin = PluginContainer(self, plugin)
        if temp_plugin.name in self.plugins:
            raise Exception("Plugin %s was already registered" % temp_plugin.name)
        self.plugins[temp_plugin.name] = temp_plugin
        temp_plugin.init_plugin()

    def register_event(self, event_id, callback):
        if event_id not in self.events:
            self.events[event_id] = set()
        self.events[event_id].add(callback)

    def unregister_event(self, event_id, callback):
        self.events[event_id].remove(callback)

    def unload_plugin(self, plugin_name):
        self.plugins[plugin_name].plugin_unload()
        del self.plugins[plugin_name]

    def append_plugin_task(self, task):
        self.plugin_tasks.append(task)

    def process_event(self, event):
        if event.id in self.events:
            for callback in self.events[event.id].copy():
                self.add_task(callback,event)

    def close(self):
        for name in reversed(list(self.plugins.keys())):
            self.unload_plugin(name)

    def start(self):
        for plugin in self.plugins.values():
            plugin.start()
        log('FFxiv Python Trigger started')
        loop.run_until_complete(asyncio.wait(self.plugin_tasks))

    def add_task(self,call,*args,**kwargs):
        if inspect.iscoroutinefunction(call):
            self.append_plugin_task(loop.create_task(call(*args,**kwargs)))
        else:
            loop.create_task(normal_to_async(call,*args,**kwargs))

class PluginContainer(object):
    def __init__(self, fpt: FFxivPythonTrigger, plugin):
        self._fpt = fpt
        self.api = fpt.api
        self.process_event = fpt.process_event
        self.name = plugin.name
        self._plugin = plugin
        self.events = list()
        self.apis = list()
        self.plugin = None

    def init_plugin(self):
        self.plugin = self._plugin(self)
        self.plugin.plugin_onload()

    def start(self):
        self._fpt.append_plugin_task(loop.create_task(self.plugin.plugin_start()))

    def register_api(self, name, api_object):
        self.apis.append(name)
        self.api.register_attribute(name, api_object)

    def register_event(self, event_id, callback):
        self.events.append((event_id, callback))
        self._fpt.register_event(event_id, callback)

    def plugin_unload(self):
        for event_id, callback in self.events:
            self._fpt.unregister_event(event_id, callback)
        for name in self.apis:
            self.api.unregister_attribute(name)
        self.plugin.plugin_onunload()


class EventBase(object):
    id = 0
    name = "unnamed event"


class PluginBase(object):
    name = "unnamed_plugin"

    def __init__(self, FPT: PluginContainer):
        self.FPT = FPT

    def plugin_onload(self):
        pass

    def plugin_onunload(self):
        pass

    async def plugin_start(self):
        pass
