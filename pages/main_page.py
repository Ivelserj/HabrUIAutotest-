"""
Page Object Model for Habr.com main page
"""
import re
from playwright.sync_api import Page, Locator
from typing import List


class MainPage:
    """Page Object Model for Habr.com main page"""
    
    URL = "https://habr.com"
    
    def __init__(self, page: Page):
        """
        Initialize MainPage with Playwright page object
        
        Args:
            page: Playwright Page instance
        """
        self.page = page
    
    def navigate(self) -> None:
        """Navigate to the main page"""
        self.page.goto(self.URL, wait_until="domcontentloaded")
        # Wait for header container to be visible as an indicator that page is loaded
        self.page.wait_for_selector("div.tm-header__container", state="visible", timeout=30000)
        # Wait for page to be fully loaded (all resources loaded)
        self.page.wait_for_load_state("load", timeout=10000)
        # If we're on feed page, navigate to articles page where all tabs are visible
        if "/ru/feed" in self.page.url:
            self.page.goto("https://habr.com/ru/articles/", wait_until="domcontentloaded")
            self.page.wait_for_selector("div.tm-header__container", state="visible", timeout=30000)
            self.page.wait_for_load_state("load", timeout=10000)
    
    # Header elements
    @property
    def header_container(self) -> Locator:
        """Header container element"""
        return self.page.locator("div.tm-header__container")
    
    @property
    def logo_link(self) -> Locator:
        """Habr logo link"""
        return self.header_container.locator('a[href*="/ru/feed"]').or_(
            self.header_container.locator('a[href="/"]')
        ).first
    
    # Content tabs - located in main content area
    @property
    def articles_tab(self) -> Locator:
        """Articles tab ('Статьи')"""
        # Tab is in main content, using href to find it
        return self.page.locator('a[href="/ru/articles/"]').filter(has_text="Статьи").first
    
    @property
    def posts_tab(self) -> Locator:
        """Posts tab ('Посты')"""
        # Posts tab might be in main content area
        return self.page.locator('a[href="/ru/posts/"]').filter(has_text="Посты").or_(
            self.page.get_by_role("link", name="Посты")
        ).first
    
    @property
    def news_tab(self) -> Locator:
        """News tab ('Новости')"""
        return self.page.locator('a[href="/ru/news/"]').filter(has_text="Новости").first
    
    @property
    def hubs_tab(self) -> Locator:
        """Hubs tab ('Хабы')"""
        return self.page.locator('a[href="/ru/hubs/"]').filter(has_text="Хабы").first
    
    @property
    def authors_tab(self) -> Locator:
        """Authors tab ('Авторы')"""
        return self.page.locator('a[href="/ru/users/"]').filter(has_text="Авторы").first
    
    @property
    def companies_tab(self) -> Locator:
        """Companies tab ('Компании')"""
        return self.page.locator('a[href="/ru/companies/"]').filter(has_text="Компании").first
    
    # Other header elements - scoped to header
    @property
    def all_streams_link(self) -> Locator:
        """All Streams link ('Все потоки')"""
        return self.header_container.get_by_role("link", name="Все потоки").first
    
    @property
    def search_link(self) -> Locator:
        """Search link ('Поиск')"""
        return self.header_container.get_by_role("link", name="Поиск").first
    
    @property
    def write_publication_link(self) -> Locator:
        """Write Publication link ('Написать публикацию')"""
        return self.header_container.get_by_role("link", name="Написать публикацию").first
    
    @property
    def settings_button(self) -> Locator:
        """Settings button ('Настройки')"""
        return self.header_container.get_by_role("button", name="Настройки").first
    
    @property
    def login_button(self) -> Locator:
        """Login button ('Войти')"""
        return self.header_container.get_by_role("button", name="Войти").first
    
    # Content areas
    @property
    def main_content_area(self) -> Locator:
        """Main content area"""
        return self.page.locator("main").or_(self.page.locator("div.tm-base-page__content"))
    
    @property
    def footer_section(self) -> Locator:
        """Footer section"""
        return self.page.locator("footer").or_(self.page.locator("div.tm-footer"))
    
    # Verification methods
    def verify_header_container_exists(self) -> bool:
        """Verify header container exists and is visible"""
        return self.header_container.is_visible()
    
    def verify_logo_exists(self) -> bool:
        """Verify logo link exists and is visible"""
        return self.logo_link.is_visible()
    
    def verify_all_content_tabs_exist(self) -> bool:
        """Verify all content tabs exist and are visible"""
        tabs = [
            self.articles_tab,
            self.posts_tab,
            self.news_tab,
            self.hubs_tab,
            self.authors_tab,
            self.companies_tab
        ]
        return all(tab.is_visible() for tab in tabs)
    
    def verify_header_elements_exist(self) -> bool:
        """Verify all header elements exist and are visible"""
        elements = [
            self.all_streams_link,
            self.search_link,
            self.write_publication_link,
            self.settings_button,
            self.login_button
        ]
        return all(element.is_visible() for element in elements)
    
    def verify_main_content_area_exists(self) -> bool:
        """Verify main content area exists and is visible"""
        return self.main_content_area.first.is_visible()
    
    def verify_footer_section_exists(self) -> bool:
        """Verify footer section exists and is visible"""
        return self.footer_section.first.is_visible()
    
    def get_all_content_tabs(self) -> List[Locator]:
        """Get list of all content tab locators"""
        return [
            self.articles_tab,
            self.posts_tab,
            self.news_tab,
            self.hubs_tab,
            self.authors_tab,
            self.companies_tab
        ]

