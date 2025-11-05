"""
Steps class for Main Page test actions
Implements step-by-step actions for test execution
"""
from pages.main_page import MainPage
from playwright.sync_api import Page
import allure


class MainPageSteps:
    """Steps class for Main Page test actions"""
    
    def __init__(self, page: Page):
        """
        Initialize MainPageSteps with Playwright page object
        
        Args:
            page: Playwright Page instance
        """
        self.page = page
        self.main_page = MainPage(page)
    
    @allure.step("Navigate to main page")
    def navigate_to_main_page(self) -> None:
        """Navigate to the main page"""
        self.main_page.navigate()
        allure.attach(
            self.page.screenshot(),
            name="main_page_loaded",
            attachment_type=allure.attachment_type.PNG
        )
    
    @allure.step("Verify header container exists and is visible")
    def verify_header_container(self) -> bool:
        """
        Verify header container exists and is visible
        
        Returns:
            bool: True if header container is visible, False otherwise
        """
        is_visible = self.main_page.verify_header_container_exists()
        if is_visible:
            allure.attach(
                self.main_page.header_container.screenshot(),
                name="header_container",
                attachment_type=allure.attachment_type.PNG
            )
        return is_visible
    
    @allure.step("Verify logo link exists and is visible")
    def verify_logo_link(self) -> bool:
        """
        Verify logo link exists and is visible
        
        Returns:
            bool: True if logo link is visible, False otherwise
        """
        return self.main_page.verify_logo_exists()
    
    @allure.step("Verify all content tabs are present and visible")
    def verify_all_content_tabs(self) -> dict:
        """
        Verify all content tabs are present and visible
        
        Returns:
            dict: Dictionary with tab names as keys and visibility status as values
        """
        tabs = {
            "Статьи": self.main_page.articles_tab,
            "Посты": self.main_page.posts_tab,
            "Новости": self.main_page.news_tab,
            "Хабы": self.main_page.hubs_tab,
            "Авторы": self.main_page.authors_tab,
            "Компании": self.main_page.companies_tab
        }
        
        results = {}
        for tab_name, tab_locator in tabs.items():
            try:
                # Check if element exists and is visible
                count = tab_locator.count()
                if count > 0:
                    is_visible = tab_locator.first.is_visible(timeout=5000)
                else:
                    is_visible = False
            except Exception:
                is_visible = False
            
            results[tab_name] = is_visible
            if not is_visible:
                allure.attach(
                    f"Tab '{tab_name}' is not visible (count: {tab_locator.count() if 'tab_locator' in locals() else 0})",
                    name=f"missing_tab_{tab_name}",
                    attachment_type=allure.attachment_type.TEXT
                )
        
        return results
    
    @allure.step("Verify header elements are present and visible")
    def verify_header_elements(self) -> dict:
        """
        Verify header elements (All Streams, Search, Write Publication, Settings, Login) are visible
        
        Returns:
            dict: Dictionary with element names as keys and visibility status as values
        """
        elements = {
            "Все потоки": self.main_page.all_streams_link,
            "Поиск": self.main_page.search_link,
            "Написать публикацию": self.main_page.write_publication_link,
            "Настройки": self.main_page.settings_button,
            "Войти": self.main_page.login_button
        }
        
        results = {}
        for element_name, element_locator in elements.items():
            is_visible = element_locator.is_visible()
            results[element_name] = is_visible
            if not is_visible:
                allure.attach(
                    f"Element '{element_name}' is not visible",
                    name=f"missing_element_{element_name}",
                    attachment_type=allure.attachment_type.TEXT
                )
        
        return results
    
    @allure.step("Verify main content area exists and is visible")
    def verify_main_content_area(self) -> bool:
        """
        Verify main content area exists and is visible
        
        Returns:
            bool: True if main content area is visible, False otherwise
        """
        is_visible = self.main_page.verify_main_content_area_exists()
        if is_visible:
            allure.attach(
                self.main_page.main_content_area.first.screenshot(),
                name="main_content_area",
                attachment_type=allure.attachment_type.PNG
            )
        return is_visible
    
    @allure.step("Verify footer section exists and is visible")
    def verify_footer_section(self) -> bool:
        """
        Verify footer section exists and is visible
        
        Returns:
            bool: True if footer section is visible, False otherwise
        """
        # Scroll to footer to ensure it's visible
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        # Wait for footer to be visible instead of fixed timeout
        self.main_page.footer_section.first.wait_for(state="visible", timeout=5000)
        
        is_visible = self.main_page.verify_footer_section_exists()
        if is_visible:
            allure.attach(
                self.main_page.footer_section.first.screenshot(),
                name="footer_section",
                attachment_type=allure.attachment_type.PNG
            )
        return is_visible

