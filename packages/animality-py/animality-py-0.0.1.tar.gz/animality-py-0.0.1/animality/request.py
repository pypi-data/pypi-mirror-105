from aiohttp import ClientSession
from .errors import RequestError
from json import loads
from gc import collect
from .response import Animal
from random import choice
from asyncio import sleep
from time import time

# apologize for the bad code. this was written in mobile.
# - null#8626, May 14th, 2021

# main aiohttp client session
main_session = None

# base URL
base_url = "https://animal-api.nitcord.repl.co"

# all animals
animals = ("cat", "dog", "bird", "panda", "redpanda", "koala", "fox", "whale", "kangaroo", "bunny")

# makes it case insensitive and remove all spaces and underscores
clean_str = lambda s: str(s).lower().replace("_", "").replace(" ", "")

# timeout cache
timeouts = {}

def _get_session(session=None):
    if isinstance(session, ClientSession) and (not session.closed):
        return session

    global main_session
    if main_session and (not main_session.closed):
        return main_session

    main_session = ClientSession()
    return main_session

def _validate_array(var):
    if isinstance(var, str) or not var or not hasattr(var, "__iter__"):
        return
    res = []
    for i in var:
        if not hasattr(i, "__str__"):
            return
        s = clean_str(i)
        if (s in animals) and (s not in res):
            res.append(s)
    return (res or None)

async def _delay(path):
    global timeouts
    current_time = time()
    cached = timeouts.get(path)
    if (not cached) or (cached < current_time):
        timeouts[path] = current_time + 2
        return
    await sleep(cached - current_time)

async def _get_request(path="/", session=None):
    json = None
    await _delay(path.lower().replace("/", ""))
    response = await _get_session(session).get(base_url + path)
    try:
        json = loads(await response.text())
    except:
        raise RequestError(message="Cannot parse JSON response. The API may be down. Please try again later.", response=response)
    if response.status >= 400:
        raise RequestError(response=response)
    return json

async def _animal_request(animal, session=None):
    image = await _get_request(f"/api/img/{animal}", session=session)
    fact = await _get_request(f"/api/fact/{animal}", session=session)
    return Animal(
        name=animal,
        image=image.get("link"),
        fact=fact.get("fact"),
        session=main_session
    )

# main functions

async def get(animal, session=None):
    """ retrieves an animal from the API. input can be a str or a list[str]. """

    arr = _validate_array(animal)
    if not arr:
        s = clean_str(animal)
        assert s in animals, f"'{s}' is not a valid animal name."
        return await _animal_request(s, session=session)

    results = []
    for elem in arr:
        results.append(await _animal_request(elem, session=session))

    return results

async def random(session=None):
    """ retrieves an info about a random animal from the API. """

    return await _animal_request(choice(animals), session=session)

def set_session(session):
    """ Sets the aiohttp client session to be used by the client. """

    if (not session) or (not isinstance(session, ClientSession)):
        raise TypeError("Not a valid aiohttp client session.")
    elif session.closed:
        raise TypeError("Session is closed. Cannot use.")

    global main_session
    main_session = session

async def close():
    """ Closes the used session and clears out the cache. """

    global main_session
    if main_session and (not main_session.closed):
        await main_session.close()

    global timeouts
    timeouts = {}
    collect()
