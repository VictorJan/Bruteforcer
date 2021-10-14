import asyncio
import sys

async def run(path):
    from application import product
    return await product.open(path)

if __name__=='__main__':

    if len(sys.argv)!=2: raise IndexError('In order to run this, please provide an argument of a path to crack.')
    path=sys.argv[1]
    loop=asyncio.get_event_loop()
    outcome=loop.run_until_complete(run(path))
    print(f'{path} outcome:\n{"".join(outcome)}')
    for task in asyncio.all_tasks(loop):
        task.cancel()
