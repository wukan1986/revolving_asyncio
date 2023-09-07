import asyncio
import time

from revolving_asyncio import to_async, to_sync

if __name__ == '__main__':
    @to_async
    def do_sync_work(name: str):
        time.sleep(5)
        print(f"sync function, to async by decorator, {name}")


    async def do_async_work(name: str):
        await asyncio.sleep(5)
        print(f"async function, to sync by wrapper, {name}")


    async def async_main():
        # Method 1
        await do_sync_work(name="Method 1")


    def sync_main():
        # Method 2
        to_sync(do_async_work)(name="Method 2")


    asyncio.run(async_main())
    sync_main()


    async def async_main():
        await asyncio.gather(do_sync_work('gather 1'),
                             do_async_work('gather 2'))


    asyncio.run(async_main())
