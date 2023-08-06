# animality-py
Python Wrapper for https://animal-api.nitcord.repl.co/api<br>
Discord Server: https://discord.gg/ESPMP7BEeJ<br>
Made for burber. (Hamburger#0001)<br>
## Installation
```bash
$ pip install animality-py
```

## Simple Usage
```py
import animality
from asyncio import get_event_loop

async def run():
    animal = await animality.get_animal("dog")
    print(animal.name, animal.image, animal.fact)
    random = await animality.random()
    print(random.name, random.image, random.fact)

    await animality.close()

get_event_loop().run_until_complete(run())
```

## Using an existing aiohttp client session
```py
import animality
import aiohttp

my_session = aiohttp.ClientSession(...)
animality.set_session(my_session)
```

## Downloading an image response from the API
```py
import animality
from asyncio import get_event_loop

async def run():
    animal = await animality.random()

    img = await animal.download_image()
    with open(f"{animal.name}.png", "wb" as f:
        f.write(img)
        f.close()

    await animality.close()

get_event_loop().run_until_complete(run())
```
