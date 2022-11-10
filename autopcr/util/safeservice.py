from typing import Callable
from hoshino import Service
from asyncio import get_event_loop, run_coroutine_threadsafe

class SafeService(Service):

    def __init__(self, *args, **kwargs):
        if 'loop' in kwargs:
            self.invokeloop = kwargs['loop']
            kwargs.pop('loop')
        else:
            self.invokeloop = get_event_loop()
            
        super().__init__(*args, **kwargs)

    @staticmethod
    async def invoketo(cor, loop):
        return await get_event_loop().run_in_executor(None, lambda: run_coroutine_threadsafe(cor, loop).result())

    def decoWrapper(self, func) -> Callable:
        async def wrapper(*args, **kwargs):
            if get_event_loop() != self.invokeloop:
                return await SafeService.invoketo(func(*args, **kwargs), self.invokeloop)
            else:
                return await func(*args, **kwargs)
        return wrapper
    
    
    def on_message(self, *args, **kwargs) -> Callable:
        wrapper = super().on_message(*args, **kwargs)
        return lambda func: wrapper(self.decoWrapper(func))
    
    def on_fullmatch(self, *args, **kwargs) -> Callable:
        wrapper = super().on_fullmatch(*args, **kwargs)
        return lambda func: wrapper(self.decoWrapper(func))
    
    def on_suffix(self, *args, **kwargs) -> Callable:
        wrapper = super().on_suffix(*args, **kwargs)
        return lambda func: wrapper(self.decoWrapper(func))
    
    def on_keyword(self, *args, **kwargs) -> Callable:
        wrapper = super().on_keyword(*args, **kwargs)
        return lambda func: wrapper(self.decoWrapper(func))
    
    def on_rex(self, *args, **kwargs) -> Callable:
        wrapper = super().on_rex(*args, **kwargs)
        return lambda func: wrapper(self.decoWrapper(func))
    
    def on_command(self, *args, **kwargs) -> Callable:
        wrapper = super().on_command(*args, **kwargs)
        return lambda func: wrapper(self.decoWrapper(func))
    
    def on_natural_language(self, *args, **kwargs) -> Callable:
        wrapper = super().on_natural_language(*args, **kwargs)
        return lambda func: wrapper(self.decoWrapper(func))
    
    def scheduled_job(self, *args, **kwargs) -> Callable:
        wrapper = super().scheduled_job(*args, **kwargs)
        return lambda func: wrapper(self.decoWrapper(func))
    
    def on_request(self, *args, **kwargs) -> Callable:
        wrapper = super().on_request(*args, **kwargs)
        return lambda func: wrapper(self.decoWrapper(func))
    
    def on_notice(self, *args, **kwargs) -> Callable:
        wrapper = super().on_notice(*args, **kwargs)
        return lambda func: wrapper(self.decoWrapper(func))
