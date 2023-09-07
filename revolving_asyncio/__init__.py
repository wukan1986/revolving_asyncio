import asyncio
import inspect
from functools import partial, wraps

from ._version import __version__


def to_async(f):
    """sync to async"""

    @wraps(f)
    async def decorated(*args, **kwargs):
        if inspect.iscoroutinefunction(f):
            # call directly
            return await f(*args, **kwargs)

        # no get_running_loop in python 3.6, have to copy that
        loop = asyncio._get_running_loop()
        if loop is None:
            raise RuntimeError('no running event loop')

        return await loop.run_in_executor(None, partial(f, *args, **kwargs))

    return decorated


def to_sync(f):
    """async to sync"""

    @wraps(f)
    def decorated(*args, **kwargs):
        if not inspect.iscoroutinefunction(f):
            # call directly
            return f(*args, **kwargs)

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            # RuntimeError: There is no current event loop in thread 'ThreadPoolExecutor-0_0'.
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # RuntimeError: This event loop is already running
        return loop.run_until_complete(f(*args, **kwargs))

    return decorated


def apply():
    # RuntimeError: This event loop is already running， so apply patch
    # 如果只使用`to_async`或`to_sync`不报错，那就直接使用，反之需要提前`apply`
    import nest_asyncio
    nest_asyncio.apply()
