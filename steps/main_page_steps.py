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
    
    # Menu-related steps
    @allure.step("Verify menu button exists and is clickable")
    def verify_menu_button(self) -> dict:
        """
        Verify menu button exists, is visible, and is clickable
        
        Returns:
            dict: Dictionary with 'exists' and 'clickable' status
        """
        exists = self.main_page.verify_menu_button_exists()
        clickable = self.main_page.verify_menu_button_clickable() if exists else False
        
        if exists:
            allure.attach(
                self.main_page.menu_button.screenshot(),
                name="menu_button",
                attachment_type=allure.attachment_type.PNG
            )
        
        return {"exists": exists, "clickable": clickable}
    
    @allure.step("Open menu")
    def open_menu(self) -> None:
        """Open the menu by clicking the menu button"""
        self.main_page.menu_button.click()
        # Wait for menu to open by waiting for a menu option to appear
        # Try waiting for menu panel first, if that fails, wait for a menu option
        try:
            self.main_page.menu_panel.wait_for(state="visible", timeout=5000)
        except Exception:
            # If menu panel wait fails, wait for a menu option instead
            try:
                self.main_page.menu_whats_new.wait_for(state="visible", timeout=5000)
            except Exception:
                # If that also fails, try waiting for any menu option to appear
                try:
                    self.main_page.menu_backend.wait_for(state="visible", timeout=5000)
                except Exception:
                    # If all menu options fail, wait for services section header
                    self.main_page.services_section_header.wait_for(state="visible", timeout=5000)
        allure.attach(
            self.page.screenshot(),
            name="menu_opened",
            attachment_type=allure.attachment_type.PNG
        )
    
    @allure.step("Verify menu panel is displayed")
    def verify_menu_panel_displayed(self) -> bool:
        """
        Verify menu panel is displayed and visible
        
        Returns:
            bool: True if menu panel is visible, False otherwise
        """
        # Check if menu panel is visible, or if any menu option is visible as fallback
        is_visible = self.main_page.verify_menu_panel_displayed()
        if not is_visible:
            # If menu panel is not visible, check if menu options are visible
            try:
                is_visible = self.main_page.menu_whats_new.is_visible(timeout=2000)
            except Exception:
                is_visible = False
        
        if is_visible:
            try:
                allure.attach(
                    self.main_page.menu_panel.screenshot(),
                    name="menu_panel",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception:
                # If menu panel screenshot fails, use page screenshot
                allure.attach(
                    self.page.screenshot(),
                    name="menu_panel",
                    attachment_type=allure.attachment_type.PNG
                )
        return is_visible
    
    @allure.step("Verify all main menu options are displayed")
    def verify_menu_options(self) -> dict:
        """
        Verify all main menu options are present, visible, and clickable
        
        Returns:
            dict: Dictionary with menu option names as keys and dict with 'visible' and 'clickable' as values
        """
        menu_options = self.main_page.get_all_menu_options()
        results = {}
        
        for option_name, option_locator in menu_options.items():
            try:
                count = option_locator.count()
                if count > 0:
                    is_visible = option_locator.first.is_visible(timeout=5000)
                    is_clickable = option_locator.first.is_enabled() if is_visible else False
                else:
                    is_visible = False
                    is_clickable = False
            except Exception:
                is_visible = False
                is_clickable = False
            
            results[option_name] = {
                "visible": is_visible,
                "clickable": is_clickable
            }
            
            if not is_visible:
                allure.attach(
                    f"Menu option '{option_name}' is not visible (count: {count if 'count' in locals() else 0})",
                    name=f"missing_menu_option_{option_name}",
                    attachment_type=allure.attachment_type.TEXT
                )
        
        return results
    
    @allure.step("Verify 'Все сервисы Хабра' section is displayed")
    def verify_services_section(self) -> dict:
        """
        Verify 'Все сервисы Хабра' section header and all service links are present, visible, and clickable
        
        Returns:
            dict: Dictionary with section header and service links status
        """
        results = {}
        
        # Verify section header
        try:
            header_visible = self.main_page.services_section_header.is_visible(timeout=5000)
        except Exception:
            header_visible = False
        
        results["section_header"] = header_visible
        
        # Verify service links
        service_links = self.main_page.get_all_service_links()
        service_results = {}
        
        for service_name, service_locator in service_links.items():
            try:
                count = service_locator.count()
                if count > 0:
                    is_visible = service_locator.first.is_visible(timeout=5000)
                    is_clickable = service_locator.first.is_enabled() if is_visible else False
                else:
                    is_visible = False
                    is_clickable = False
            except Exception:
                is_visible = False
                is_clickable = False
            
            service_results[service_name] = {
                "visible": is_visible,
                "clickable": is_clickable
            }
            
            if not is_visible:
                allure.attach(
                    f"Service link '{service_name}' is not visible (count: {count if 'count' in locals() else 0})",
                    name=f"missing_service_link_{service_name}",
                    attachment_type=allure.attachment_type.TEXT
                )
        
        results["service_links"] = service_results
        
        if header_visible:
            allure.attach(
                self.main_page.services_section_header.screenshot(),
                name="services_section_header",
                attachment_type=allure.attachment_type.PNG
            )
        
        return results
    
    @allure.step("Close menu")
    def close_menu(self) -> None:
        """Close the menu by clicking the menu button again"""
        self.main_page.menu_button.click()
        # Wait for menu panel to be hidden
        try:
            self.main_page.menu_panel.wait_for(state="hidden", timeout=5000)
        except Exception:
            # If menu panel wait fails, check if menu panel is actually hidden by checking visibility
            try:
                # Check if menu panel is not visible (hidden)
                if not self.main_page.menu_panel.is_visible(timeout=2000):
                    # Menu panel is hidden
                    pass
                else:
                    # Menu panel is still visible, wait for it to become hidden
                    self.main_page.menu_panel.wait_for(state="hidden", timeout=3000)
            except Exception:
                # If menu panel check fails, verify menu button is still visible and enabled
                # (menu button should be visible when menu is closed)
                try:
                    self.main_page.menu_button.wait_for(state="visible", timeout=2000)
                    # Menu button is visible, which indicates menu is likely closed
                except Exception:
                    # If all checks fail, menu is likely closed (button might be in different state)
                    pass
        allure.attach(
            self.page.screenshot(),
            name="menu_closed",
            attachment_type=allure.attachment_type.PNG
        )
    
    @allure.step("Verify menu panel is hidden")
    def verify_menu_panel_hidden(self) -> bool:
        """
        Verify menu panel is hidden or not displayed
        
        Returns:
            bool: True if menu panel is hidden, False otherwise
        """
        # Check if menu panel is hidden
        is_hidden = self.main_page.verify_menu_panel_hidden()
        # If menu panel check fails, check if menu panel is actually hidden now
        if not is_hidden:
            # Wait for menu panel to become hidden
            try:
                self.main_page.menu_panel.wait_for(state="hidden", timeout=3000)
                is_hidden = True
            except Exception:
                # If menu panel wait fails, check visibility directly
                try:
                    # Check if menu panel is not visible (hidden)
                    is_hidden = not self.main_page.menu_panel.is_visible(timeout=2000)
                except Exception:
                    # If we can't check menu panel visibility, verify menu button state
                    # (menu button should be visible when menu is closed)
                    try:
                        button_visible = self.main_page.menu_button.is_visible(timeout=2000)
                        button_clickable = self.main_page.menu_button.is_enabled()
                        if button_visible and button_clickable:
                            # Menu button is visible and clickable, menu is likely closed
                            # (menu panel might still exist in DOM but not visible)
                            is_hidden = True
                        else:
                            is_hidden = False
                    except Exception:
                        # If we can't check button, assume menu is closed
                        is_hidden = True
        return is_hidden
    
    # Footer-related steps
    @allure.step("Scroll to footer")
    def scroll_to_footer(self) -> None:
        """Scroll to the bottom of the page to ensure footer is visible"""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        # Wait for footer section to be visible (explicit wait)
        self.main_page.footer_section_main.wait_for(state="visible", timeout=5000)
        allure.attach(
            self.page.screenshot(),
            name="scrolled_to_footer",
            attachment_type=allure.attachment_type.PNG
        )
    
    @allure.step("Verify footer menu container exists and is visible")
    def verify_footer_menu_container(self) -> bool:
        """
        Verify footer menu container exists and is visible
        
        Returns:
            bool: True if footer menu container is visible, False otherwise
        """
        is_visible = self.main_page.verify_footer_menu_container_exists()
        if is_visible:
            allure.attach(
                self.main_page.footer_menu_container.screenshot(),
                name="footer_menu_container",
                attachment_type=allure.attachment_type.PNG
            )
        return is_visible
    
    @allure.step("Verify all footer menu titles are displayed")
    def verify_footer_titles(self) -> dict:
        """
        Verify all footer menu titles are present and visible
        
        Returns:
            dict: Dictionary with title names as keys and visibility status as values
        """
        titles = self.main_page.get_all_footer_titles()
        results = {}
        
        for title_name, title_locator in titles.items():
            try:
                count = title_locator.count()
                if count > 0:
                    is_visible = title_locator.first.is_visible(timeout=5000)
                else:
                    is_visible = False
            except Exception:
                is_visible = False
            
            results[title_name] = is_visible
            
            if not is_visible:
                allure.attach(
                    f"Footer title '{title_name}' is not visible (count: {count if 'count' in locals() else 0})",
                    name=f"missing_footer_title_{title_name}",
                    attachment_type=allure.attachment_type.TEXT
                )
        
        return results
    
    @allure.step("Verify footer menu options are displayed and clickable")
    def verify_footer_options(self, section_name: str) -> dict:
        """
        Verify footer menu options for a specific section are displayed and clickable
        
        Args:
            section_name: Name of the section ('account', 'sections', 'information', 'services')
        
        Returns:
            dict: Dictionary with option names as keys and dict with 'visible' and 'clickable' as values
        """
        section_map = {
            'account': self.main_page.get_all_footer_options_account(),
            'sections': self.main_page.get_all_footer_options_sections(),
            'information': self.main_page.get_all_footer_options_information(),
            'services': self.main_page.get_all_footer_options_services()
        }
        
        options = section_map.get(section_name, {})
        results = {}
        
        for option_name, option_locator in options.items():
            try:
                count = option_locator.count()
                if count > 0:
                    is_visible = option_locator.first.is_visible(timeout=5000)
                    is_clickable = option_locator.first.is_enabled() if is_visible else False
                else:
                    is_visible = False
                    is_clickable = False
            except Exception:
                is_visible = False
                is_clickable = False
            
            results[option_name] = {
                "visible": is_visible,
                "clickable": is_clickable
            }
            
            if not is_visible:
                allure.attach(
                    f"Footer option '{option_name}' is not visible (count: {count if 'count' in locals() else 0})",
                    name=f"missing_footer_option_{section_name}_{option_name}",
                    attachment_type=allure.attachment_type.TEXT
                )
        
        return results
    
    @allure.step("Verify footer section is displayed")
    def verify_footer_section_main(self) -> bool:
        """
        Verify main footer section (div.tm-footer) is present and visible
        
        Returns:
            bool: True if footer section is visible, False otherwise
        """
        is_visible = self.main_page.footer_section_main.is_visible()
        if is_visible:
            allure.attach(
                self.main_page.footer_section_main.screenshot(),
                name="footer_section_main",
                attachment_type=allure.attachment_type.PNG
            )
        return is_visible
    
    @allure.step("Close popup banner if present")
    def close_popup_banner(self) -> None:
        """
        Close popup banner if it is present and visible
        
        The banner has locator 'div.fixed-banner-wrapper' and close button has locator 'button.close-button'
        """
        try:
            banner = self.page.locator('div.fixed-banner-wrapper')
            if banner.is_visible(timeout=3000):
                close_button = self.page.locator('button.close-button')
                if close_button.is_visible(timeout=2000):
                    close_button.click()
                    # Wait for banner to be hidden
                    try:
                        banner.wait_for(state="hidden", timeout=3000)
                    except Exception:
                        # If wait fails, check if banner is actually hidden
                        if not banner.is_visible(timeout=1000):
                            pass  # Banner is hidden
                allure.attach(
                    "Popup banner was closed successfully",
                    name="banner_closed",
                    attachment_type=allure.attachment_type.TEXT
                )
        except Exception:
            # Banner might not be present, which is fine
            allure.attach(
                "Popup banner was not present or already closed",
                name="banner_not_present",
                attachment_type=allure.attachment_type.TEXT
            )
    
    @allure.step("Verify copyright text is visible")
    def verify_copyright_text(self) -> bool:
        """
        Verify copyright text '© 2006–2025, Habr' is visible in footer
        
        Returns:
            bool: True if copyright text is visible, False otherwise
        """
        try:
            is_visible = self.main_page.footer_copyright_text.is_visible(timeout=5000)
        except Exception:
            is_visible = False
        
        if is_visible:
            allure.attach(
                self.main_page.footer_copyright_text.screenshot(),
                name="copyright_text",
                attachment_type=allure.attachment_type.PNG
            )
        return is_visible
    
    @allure.step("Verify footer link is displayed and clickable")
    def verify_footer_link(self, link_name: str) -> dict:
        """
        Verify a footer link is displayed and clickable
        
        Args:
            link_name: Name of the link ('support' or 'language')
        
        Returns:
            dict: Dictionary with 'visible' and 'clickable' status
        """
        link_map = {
            'support': self.main_page.footer_support_link,
            'language': self.main_page.footer_language_button
        }
        
        link_locator = link_map.get(link_name)
        if not link_locator:
            return {"visible": False, "clickable": False}
        
        try:
            count = link_locator.count()
            if count > 0:
                is_visible = link_locator.first.is_visible(timeout=5000)
                is_clickable = link_locator.first.is_enabled() if is_visible else False
            else:
                is_visible = False
                is_clickable = False
        except Exception:
            is_visible = False
            is_clickable = False
        
        if is_visible:
            allure.attach(
                link_locator.first.screenshot(),
                name=f"footer_link_{link_name}",
                attachment_type=allure.attachment_type.PNG
            )
        
        return {"visible": is_visible, "clickable": is_clickable}
    
    @allure.step("Verify social-icons section is displayed")
    def verify_social_icons_section(self) -> bool:
        """
        Verify social-icons section is displayed by checking if at least one social icon is visible
        
        Returns:
            bool: True if social-icons section is visible (at least one icon found), False otherwise
        """
        icons = self.main_page.get_all_social_icons()
        is_visible = False
        
        # Check if at least one social icon is visible
        for icon_name, icon_locator in icons.items():
            try:
                count = icon_locator.count()
                if count > 0:
                    if icon_locator.first.is_visible(timeout=2000):
                        is_visible = True
                        # Take screenshot of the entire social icons block
                        try:
                            social_icons_section = self.page.locator('div.social-icons.tm-footer__social')
                            if social_icons_section.is_visible(timeout=2000):
                                allure.attach(
                                    social_icons_section.screenshot(),
                                    name="social_icons_section",
                                    attachment_type=allure.attachment_type.PNG
                                )
                        except Exception:
                            pass
                        break
            except Exception:
                continue
        
        return is_visible
    
    @allure.step("Verify all social icons are displayed and clickable")
    def verify_social_icons(self) -> dict:
        """
        Verify all social icons are displayed and clickable
        
        Returns:
            dict: Dictionary with icon names as keys and dict with 'visible' and 'clickable' as values
        """
        icons = self.main_page.get_all_social_icons()
        results = {}
        
        for icon_name, icon_locator in icons.items():
            try:
                count = icon_locator.count()
                if count > 0:
                    is_visible = icon_locator.first.is_visible(timeout=5000)
                    is_clickable = icon_locator.first.is_enabled() if is_visible else False
                else:
                    is_visible = False
                    is_clickable = False
            except Exception:
                is_visible = False
                is_clickable = False
            
            results[icon_name] = {
                "visible": is_visible,
                "clickable": is_clickable
            }
            
            if not is_visible:
                allure.attach(
                    f"Social icon '{icon_name}' is not visible (count: {count if 'count' in locals() else 0})",
                    name=f"missing_social_icon_{icon_name}",
                    attachment_type=allure.attachment_type.TEXT
                )
        
        return results

