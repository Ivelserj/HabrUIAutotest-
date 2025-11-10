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
        # Wait for page to be fully loaded (all resources loaded) with increased timeout
        try:
            self.page.wait_for_load_state("load", timeout=30000)
        except Exception:
            # If load state times out, try networkidle as fallback
            try:
                self.page.wait_for_load_state("networkidle", timeout=15000)
            except Exception:
                # If both fail, just continue - page is likely loaded enough
                pass
        # If we're on feed page, navigate to articles page where all tabs are visible
        if "/ru/feed" in self.page.url:
            self.page.goto("https://habr.com/ru/articles/", wait_until="domcontentloaded")
            self.page.wait_for_selector("div.tm-header__container", state="visible", timeout=30000)
            try:
                self.page.wait_for_load_state("load", timeout=30000)
            except Exception:
                # If load state times out, try networkidle as fallback
                try:
                    self.page.wait_for_load_state("networkidle", timeout=15000)
                except Exception:
                    # If both fail, just continue - page is likely loaded enough
                    pass
    
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
        return self.page.locator('.tm-footer-menu')
    
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
    
    # Menu elements
    @property
    def menu_button(self) -> Locator:
        """Menu button element"""
        return self.page.locator('//*[@id="app"]/div/header/div/div/button').first
    
    @property
    def menu_panel(self) -> Locator:
        """Menu panel element"""
        return self.page.locator(".navigation-wrapper")
    
    # Main menu options
    @property
    def menu_whats_new(self) -> Locator:
        """What's New menu option ('Что нового')"""
        return self.page.get_by_role("link", name="Что нового").or_(
            self.page.get_by_text("Что нового")
        ).first
    
    @property
    def menu_backend(self) -> Locator:
        """Backend menu option ('Бэкенд')"""
        return self.page.get_by_role("link", name="Бэкенд").or_(
            self.page.get_by_text("Бэкенд")
        ).first
    
    @property
    def menu_frontend(self) -> Locator:
        """Frontend menu option ('Фронтенд')"""
        return self.page.get_by_role("link", name="Фронтенд").or_(
            self.page.get_by_text("Фронтенд")
        ).first
    
    @property
    def menu_administration(self) -> Locator:
        """Administration menu option ('Администрирование')"""
        return self.page.get_by_role("link", name="Администрирование").or_(
            self.page.get_by_text("Администрирование")
        ).first
    
    @property
    def menu_design(self) -> Locator:
        """Design menu option ('Дизайн')"""
        return self.page.get_by_role("link", name="Дизайн").or_(
            self.page.get_by_text("Дизайн")
        ).first
    
    @property
    def menu_management(self) -> Locator:
        """Management menu option ('Менеджмент')"""
        return self.page.get_by_role("link", name="Менеджмент").or_(
            self.page.get_by_text("Менеджмент")
        ).first
    
    @property
    def menu_marketing(self) -> Locator:
        """Marketing and content menu option ('Маркетинг и контент')"""
        return self.page.get_by_role("link", name="Маркетинг и контент").or_(
            self.page.get_by_text("Маркетинг и контент")
        ).first
    
    @property
    def menu_science(self) -> Locator:
        """Science popularization menu option ('Научпоп')"""
        return self.page.get_by_role("link", name="Научпоп").or_(
            self.page.get_by_text("Научпоп")
        ).first
    
    @property
    def menu_development(self) -> Locator:
        """Development menu option ('Разработка')"""
        return self.page.get_by_role("link", name="Разработка").or_(
            self.page.get_by_text("Разработка")
        ).first
    
    @property
    def menu_all_streams(self) -> Locator:
        """All streams menu option ('Все потоки')"""
        return self.page.get_by_role("link", name="Все потоки").or_(
            self.page.get_by_text("Все потоки")
        ).first
    
    # All Habr services section
    @property
    def services_section_header(self) -> Locator:
        """All Habr services section header ('Все сервисы Хабра')"""
        return self.page.get_by_text("Все сервисы Хабра").first
    
    @property
    def service_habr_link(self) -> Locator:
        """Habr service link ('Хабр')"""
        return self.page.get_by_role("link", name="Хабр").or_(
            self.page.locator('a[href*="habr.com"]').filter(has_text="Хабр")
        ).first
    
    @property
    def service_qa_link(self) -> Locator:
        """Q&A service link"""
        return self.page.get_by_role("link", name="Q&A").or_(
            self.page.get_by_text("Q&A")
        ).first
    
    @property
    def service_career_link(self) -> Locator:
        """Career service link ('Карьера')"""
        return self.page.get_by_role("link", name="Карьера").or_(
            self.page.get_by_text("Карьера")
        ).first
    
    @property
    def service_courses_link(self) -> Locator:
        """Courses service link ('Курсы')"""
        return self.page.get_by_role("link", name="Курсы").or_(
            self.page.get_by_text("Курсы")
        ).first
    
    # Menu verification methods
    def verify_menu_button_exists(self) -> bool:
        """Verify menu button exists and is visible"""
        return self.menu_button.is_visible()
    
    def verify_menu_button_clickable(self) -> bool:
        """Verify menu button is clickable"""
        return self.menu_button.is_enabled()
    
    def verify_menu_panel_displayed(self) -> bool:
        """Verify menu panel is displayed and visible"""
        try:
            return self.menu_panel.is_visible(timeout=5000)
        except Exception:
            return False
    
    def verify_menu_panel_hidden(self) -> bool:
        """Verify menu panel is hidden or not displayed"""
        try:
            return not self.menu_panel.is_visible(timeout=2000)
        except Exception:
            return True
    
    def get_all_menu_options(self) -> dict:
        """Get dictionary of all menu option locators"""
        return {
            "Что нового": self.menu_whats_new,
            "Бэкенд": self.menu_backend,
            "Фронтенд": self.menu_frontend,
            "Администрирование": self.menu_administration,
            "Дизайн": self.menu_design,
            "Менеджмент": self.menu_management,
            "Маркетинг и контент": self.menu_marketing,
            "Научпоп": self.menu_science,
            "Разработка": self.menu_development,
            "Все потоки": self.menu_all_streams
        }
    
    def get_all_service_links(self) -> dict:
        """Get dictionary of all service link locators"""
        return {
            "Хабр": self.service_habr_link,
            "Q&A": self.service_qa_link,
            "Карьера": self.service_career_link,
            "Курсы": self.service_courses_link
        }

