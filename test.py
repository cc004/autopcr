import asyncio
from autopcr.modulebase import ModuleManager
from autopcr.modules import register_all
register_all()

mgr = ModuleManager('test.json')
print(asyncio.run(mgr.do_task()))