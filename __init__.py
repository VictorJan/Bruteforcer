import asyncio

async def run(path):
    from application import product
    return await product.open(path)

if __name__=='__main__':

    path=r'D:\Uni\7s\SoftwareSecurity\Labs\lab2\data\sample_1_2.zip'

    loop=asyncio.get_event_loop()
    outcome=loop.run_until_complete(run(path))
    loop.close()
    print(print(f'{path} outcome:\n{"".join(outcome)}'))

