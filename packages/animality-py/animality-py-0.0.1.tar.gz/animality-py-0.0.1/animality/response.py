from .errors import RequestError                           
class Animal:
    def __init__(self, name, image, fact, session):
        self.name = name
        self.image = image
        self.fact = fact
        self._downloaded_image = None
        self._download_image = lambda: session.get(image)

    def __dict__(self):
        return {
            "name": self.name,
            "image": self.image,
            "fact": self.fact
        }

    def __getitem__(self, key):
        return self.__dict__().get(key)

    def __repr__(self):
        return f"<Animal name=\"{self.name}\" image=\"{self.image}\" fact=\"{self.fact}\">"

    async def download_image(self) -> bytes:
        if self._downloaded_image:
            return self._downloaded_image

        res = await self._download_image()
        if res.status >= 400:
            raise RequestError(response=res)

        self._download_image = None
        self._downloaded_image = await re
