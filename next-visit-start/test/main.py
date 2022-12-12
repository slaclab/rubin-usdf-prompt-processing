import httpx

import asyncio
import httpx
import time

import asyncio
import httpx
import time


start_time = time.time()


async def get_pokemon(client, url):
    resp = await client.get(url)
    pokemon = resp.json()

    return pokemon["name"]


async def main():

    while True:
        async with httpx.AsyncClient() as client:

            tasks = []
            for number in range(1, 151):
                url = f"https://pokeapi.co/api/v2/pokemon/{number}"
                tasks.append(asyncio.ensure_future(get_pokemon(client, url)))

            original_pokemon = await asyncio.gather(*tasks)
            for pokemon in original_pokemon:
                print(pokemon)


asyncio.run(main())
print("--- %s seconds ---" % (time.time() - start_time))
