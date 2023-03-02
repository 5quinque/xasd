import asyncio
import logging
from enum import Enum
from typing import Any, Optional

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.core.utils import ChromeType
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

logger = logging.getLogger(__name__)


class Browser(Enum):
    FIREFOX = "firefox"
    CHROME = "chrome"
    CHROMIUM = "chromium"


class AsyncWebDriver:
    """
    Context manager for asynchronous webdriver.

    Usage:
        async with AsyncWebDriver() as driver:
            await driver.get("https://example.com")
    """

    def __init__(
        self,
        browser: Browser = Browser.FIREFOX,
        headless: bool = False,
        source_name: Optional[str] = None,
    ):
        self.browser = browser
        self.headless = headless
        self.source_name = source_name

        self._driver_attributes = {
            Browser.FIREFOX: {
                "options": webdriver.FirefoxOptions(),
                "driver_class": webdriver.Firefox,
                "driver_service": FirefoxService(GeckoDriverManager().install()),
            },
            Browser.CHROME: {
                "options": webdriver.ChromeOptions(),
                "driver_class": webdriver.Chrome,
                "driver_service": ChromeService(ChromeDriverManager().install()),
            },
            Browser.CHROMIUM: {
                "options": webdriver.ChromeOptions(),
                "driver_class": webdriver.Chrome,
                "driver_service": ChromeService(
                    ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
                ),
            },
        }

        self._driver = None

    @property
    def driver_attributes(self) -> dict:
        """
        Get the driver attributes for the current browser.

        Returns:
            dict: The driver attributes for the current browser.
        """
        if self.browser not in self._driver_attributes:
            raise ValueError(
                f"Browser {self.browser} is not supported. "
                f"Supported browsers are: {', '.join(self._driver_attributes.keys())}"
            )

        return self._driver_attributes[self.browser]

    @driver_attributes.setter
    def driver_attributes(self, value) -> None:
        """
        Set the driver attributes for the current browser.

        Args:
            value (dict): The driver attributes for the current browser.
        """
        self._driver_attributes[self.browser] = value

    async def __aenter__(self) -> webdriver.Remote:
        """
        Start the asynchronous webdriver.

        Returns:
            webdriver.Remote: The asynchronous webdriver.
        """

        self.driver_attributes["options"].headless = self.headless
        options = self.driver_attributes["options"]
        driver_service = self.driver_attributes["driver_service"]
        driver_class = self.driver_attributes["driver_class"]

        logger.info(f"Source: {self.source_name}. Starting {self.browser} webdriver.")
        try:
            self._driver = await asyncio.to_thread(
                lambda: driver_class(
                    service=driver_service,
                    options=options,
                )
            )
        except WebDriverException as e:
            logger.error(f"Source: {self.source_name}. {e}")
        finally:
            return self._driver

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Close the asynchronous webdriver.
        """
        if self._driver is not None:
            logger.info(f"Source: {self.source_name}. Closing webdriver.")
            await asyncio.to_thread(self._driver.quit)

    def __getattr__(self, name) -> Any:
        """
        Delegate attribute access to the webdriver object.
        """
        if self._driver is None:
            raise AttributeError(
                f"AttributeError when tring to call `{name}`. WebDriver object has no attribute '_driver'"
            )

        return getattr(self._driver, name)

    async def get(self, url: str) -> None:
        """
        Get the URL.

        Args:
            url (str): The url to get.
        """
        logger.info(f"Source: {self.source_name}. Getting url: {url}")
        await asyncio.to_thread(self._driver.get, url)

        # Check if the title is "Just a moment..." and if so, wait for user input before continuing.
        try:
            logger.info(
                f"Source: {self.source_name}. Checking for human verification. {self._driver.title}"
            )
            if self._driver.title == "Just a moment...":
                input(
                    """
                    Well, well, well. It seems the jig is up.
                    But don't worry, we'll keep this between us.
                    Just complete the human verification test and we'll be on our way.

                    Press Enter to continue..."""
                )
        except NoSuchElementException:
            pass


class Source:
    source_name: Optional[str] = None
    _driver: webdriver.Remote
    base_url: Optional[str] = None
    last_scraped: Optional[str] = None
    title_link_selector: Optional[str] = None
    next_page_selector: Optional[str] = None

    def __init__(self):
        """
        Abstract class for a source.

        Args:
            base_url (str): The base url for the source.
            title_link_selector (str): The CSS selector for the title link.
            next_page_selector (str): The CSS selector for the next page button.
        """
        self._next_page_url: Optional[str] = None
        self.queued_magnet_links: list[str] = []

    def __str__(self) -> str:
        return (
            f"Source: {self.source_name}\n"
            f"Base URL: {self.base_url}\n"
            f"Last Scraped: {self.last_scraped}\n"
            f"Title Link Selector: {self.title_link_selector}\n"
            f"Next Page Selector: {self.next_page_selector}\n"
            f"Queued Magnet Links: {self.queued_magnet_links}"
        )

    async def load_initial_page(self):
        """
        Load the initial page.
        """
        await self._driver.get(self.base_url)
        logger.info(f"Source: {self.source_name}. Loaded initial page.")

        await self.set_next_page_url()

    async def find_links(self):
        """
        Find links on the current page.

        Returns:
            list: A list of links.
        """
        title_elements = self._driver.find_elements(
            by=By.CSS_SELECTOR, value=self.title_link_selector
        )

        return [title.get_attribute("href") for title in title_elements]

    @property
    def next_page_url(self):
        """
        Get the next page url.

        Returns:
            str: The next page url.
        """
        return self._next_page_url

    async def set_next_page_url(self) -> None:
        """
        Set the next page url.
        """
        try:
            next_page = self._driver.find_element(
                by=By.CSS_SELECTOR, value=self.next_page_selector
            )
            self._next_page_url = next_page.get_attribute("href")
            logger.info(
                f"Source: {self.source_name}. Set next page url to {self.next_page_url}"
            )
        except NoSuchElementException:
            self._next_page_url = None
            logger.info(f"Source: {self.source_name}. Last page reached.")

    async def extract_magnet_links(self):
        """
        Extract magnet links from the current page.
        """
        more_links = self._driver.find_elements(by=By.TAG_NAME, value="a")
        for more_link in more_links:
            if href := more_link.get_attribute("href"):
                if href.startswith("magnet"):
                    self.queued_magnet_links.append(href)
                    logger.info(
                        f"Source: {self.source_name}. Found magnet link: {href}"
                    )

    async def crawl(self):
        """
        Crawl the source.
        """
        self._driver = AsyncWebDriver(source_name=self.source_name)
        async with self._driver:
            await self.load_initial_page()

            while self.has_next_page():
                links = await self.find_links()

                for link in links:
                    await self._driver.get(link)
                    await self.extract_magnet_links()

                await self.load_next_page()

    def has_next_page(self):
        """
        Check if there is a next page.

        Returns:
            bool: True if there is a next page, False otherwise.
        """
        return self.next_page_url is not None

    async def load_next_page(self):
        """
        Load the next page.
        """
        await self._driver.get(self.next_page_url)
        await self.set_next_page_url()
