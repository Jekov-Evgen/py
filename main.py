import asyncio
from playwright.async_api import async_playwright
import unittest

class TestChatApp(unittest.TestCase):

    async def asyncSetUp(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch()
        self.page = await self.browser.new_page()

    async def asyncTearDown(self):
        await self.browser.close()
        await self.playwright.stop()

    async def test_send_message(self):
        await self.page.goto("https://example-chat-app.com")
        await self.page.fill("input#username", "testuser")
        await self.page.click("button#login")
        await self.page.fill("input#message", "Hello, world!")
        await self.page.click("button#send")
        messages = await self.page.query_selector_all(".message")
        texts = [await message.inner_text() for message in messages]
        self.assertIn("Hello, world!", texts)

    async def test_receive_message(self):
        await self.page.goto("https://example-chat-app.com")
        await self.page.fill("input#username", "testuser")
        await self.page.click("button#login")
        messages = await self.page.query_selector_all(".message")
        texts = [await message.inner_text() for message in messages]
        self.assertIn("Welcome to the chat!", texts)

    def runTest(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.asyncSetUp())
        loop.run_until_complete(self.test_send_message())
        loop.run_until_complete(self.test_receive_message())
        loop.run_until_complete(self.asyncTearDown())

if __name__ == "__main__":
    unittest.main()