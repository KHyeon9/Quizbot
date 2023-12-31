from typing import Union

import httpx
from pydantic import SecretStr


class Telegram:
    API_HOST = "https://api.telegram.org"

    def __init__(self, token: Union[str, SecretStr]) -> None:
        self._token = token
        self.client = httpx.AsyncClient(base_url=self.host)

    @property
    def token(self):
        if isinstance(self._token, SecretStr):
            return self._token.get_secret_value()
        return self._token

    @property
    def host(self):
        return f"{self.API_HOST}/bot{self.token}/"

    async def get_bot_info(self) -> dict:
        """Get current bot info"""
        r = await self.client.get("getMe")
        return r.json()

    async def get_webhook(self):
        r = await self.client.get("getWebhookInfo")
        return r.json()

    async def set_webhook(self, url: str):
        r = await self.client.post("setWebhook", data={"url": url})
        return r.json()

    async def send_message(self, chat_id: int, text: str):
        r = await self.client.post("sendMessage", data={"chat_id": chat_id, "text": text})

        return r.json()