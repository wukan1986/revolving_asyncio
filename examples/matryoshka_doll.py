import asyncio
import time

from revolving_asyncio import to_async, to_sync

if __name__ == '__main__':

    def do_sync_work(name: str):
        time.sleep(2)
        print(f"sync function, {name}")


    async def do_async_work(name: str):
        await asyncio.sleep(2)
        print(f"async function, {name}")


    async def async_main():
        # Matryoshka Doll
        await to_async(to_sync(to_async(do_sync_work)))(name="revolving")


    def sync_main():
        # Matryoshka Doll
        to_sync(to_async(to_sync(do_async_work)))(name="revolving")


    asyncio.run(async_main())
    sync_main()


    async def async_gather():
        await asyncio.gather(async_main(),
                             to_async(sync_main)())


    asyncio.run(async_gather())
