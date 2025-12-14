"""
Steps class for Login Page test actions
Implements step-by-step actions for login functionality test execution
"""
from pages.main_page import MainPage
from pages.login_page import LoginPage
from playwright.sync_api import Page
import allure


class LoginPageSteps:
    """Steps class for Login Page test actions"""
    
    def __init__(self, page: Page):
        """
        Initialize LoginPageSteps with Playwright page object
        
        Args:
            page: Playwright Page instance
        """
        self.page = page
        self.main_page = MainPage(page)
        self.login_page = LoginPage(page)
    
    @allure.step("Verify login button exists, is visible, and clickable")
    def verify_login_button(self) -> dict:
        """
        Verify login button exists, is visible, and clickable
        
        Returns:
            dict: Dictionary with 'exists', 'visible', and 'clickable' status
        """
        try:
            exists = self.main_page.login_button.count() > 0
            if exists:
                visible = self.main_page.login_button.first.is_visible(timeout=5000)
                clickable = self.main_page.login_button.first.is_enabled() if visible else False
            else:
                visible = False
                clickable = False
        except Exception:
            exists = False
            visible = False
            clickable = False
        
        if visible:
            allure.attach(
                self.main_page.login_button.first.screenshot(),
                name="login_button",
                attachment_type=allure.attachment_type.PNG
            )
        
        return {"exists": exists, "visible": visible, "clickable": clickable}
    
    @allure.step("Click login button and wait for modal to appear")
    def click_login_button(self) -> None:
        """Click the login button and wait for login modal to appear"""
        self.main_page.login_button.click()
        # Wait for login modal to appear
        try:
            self.login_page.login_modal.wait_for(state="visible", timeout=10000)
        except Exception:
            # If modal wait fails, try waiting for email input field as fallback
            try:
                self.login_page.email_input.wait_for(state="visible", timeout=10000)
            except Exception:
                # If email input wait fails, try waiting for password input
                try:
                    self.login_page.password_input.wait_for(state="visible", timeout=10000)
                except Exception:
                    # If all waits fail, just continue - modal might be visible already
                    pass
        
        allure.attach(
            self.page.screenshot(),
            name="login_modal_opened",
            attachment_type=allure.attachment_type.PNG
        )
    
    @allure.step("Verify login window is displayed")
    def verify_login_window_displayed(self) -> bool:
        """
        Verify login window/modal is displayed and visible
        
        Returns:
            bool: True if login window is visible, False otherwise
        """
        is_visible = self.login_page.verify_login_modal_exists()
        
        if is_visible:
            allure.attach(
                self.login_page.login_modal.screenshot(),
                name="login_window",
                attachment_type=allure.attachment_type.PNG
            )
        else:
            allure.attach(
                "Login window/modal is not visible",
                name="login_window_not_visible",
                attachment_type=allure.attachment_type.TEXT
            )
        
        return is_visible
    
    @allure.step("Verify login form fields are present, visible, and enabled")
    def verify_login_form_fields(self) -> dict:
        """
        Verify login title, labels, Email and Password fields are present, visible, and enabled
        
        Returns:
            dict: Dictionary with field names as keys and dict with 'visible' and 'enabled' as values, plus title and labels
        """
        results = {}
        
        # Verify login title "Вход"
        login_title_visible = self.login_page.verify_login_title_exists()
        results["Вход"] = {"visible": login_title_visible}
        
        if login_title_visible:
            allure.attach(
                self.login_page.login_title.screenshot(),
                name="login_title",
                attachment_type=allure.attachment_type.PNG
            )
        else:
            allure.attach(
                "Login title 'Вход' is not visible",
                name="login_title_not_visible",
                attachment_type=allure.attachment_type.TEXT
            )
        
        # Verify Email label
        email_label_visible = self.login_page.verify_email_label_exists()
        results["Email_label"] = {"visible": email_label_visible}
        
        if email_label_visible:
            allure.attach(
                self.login_page.email_label.screenshot(),
                name="email_label",
                attachment_type=allure.attachment_type.PNG
            )
        else:
            allure.attach(
                "Email label text is not visible",
                name="email_label_not_visible",
                attachment_type=allure.attachment_type.TEXT
            )
        
        # Verify Password label "Пароль"
        password_label_visible = self.login_page.verify_password_label_exists()
        results["Пароль_label"] = {"visible": password_label_visible}
        
        if password_label_visible:
            allure.attach(
                self.login_page.password_label.screenshot(),
                name="password_label",
                attachment_type=allure.attachment_type.PNG
            )
        else:
            allure.attach(
                "Password label 'Пароль' is not visible",
                name="password_label_not_visible",
                attachment_type=allure.attachment_type.TEXT
            )
        
        # Verify Email field
        email_visible = self.login_page.verify_email_input_exists()
        email_enabled = self.login_page.verify_email_input_enabled() if email_visible else False
        
        results["Email"] = {
            "visible": email_visible,
            "enabled": email_enabled
        }
        
        # Verify Password field
        password_visible = self.login_page.verify_password_input_exists()
        password_enabled = self.login_page.verify_password_input_enabled() if password_visible else False
        
        results["Пароль"] = {
            "visible": password_visible,
            "enabled": password_enabled
        }
        
        return results
    
    @allure.step("Verify login form buttons are present, visible, and clickable")
    def verify_login_form_buttons(self) -> dict:
        """
        Verify Login submit button and Forgot Password link are present, visible, and clickable
        
        Returns:
            dict: Dictionary with button/link names as keys and dict with 'visible' and 'clickable' as values
        """
        results = {}
        
        # Verify Login submit button
        login_button_visible = self.login_page.verify_login_submit_button_exists()
        login_button_clickable = self.login_page.verify_login_submit_button_clickable() if login_button_visible else False
        
        results["Войти"] = {
            "visible": login_button_visible,
            "clickable": login_button_clickable
        }
        
        if login_button_visible:
            allure.attach(
                self.login_page.login_submit_button.screenshot(),
                name="login_submit_button",
                attachment_type=allure.attachment_type.PNG
            )
        else:
            allure.attach(
                "Login submit button is not visible",
                name="login_submit_button_not_visible",
                attachment_type=allure.attachment_type.TEXT
            )
        
        # Verify Forgot Password link
        forgot_password_visible = self.login_page.verify_forgot_password_link_exists()
        forgot_password_clickable = self.login_page.verify_forgot_password_link_clickable() if forgot_password_visible else False
        
        results["Забыли пароль?"] = {
            "visible": forgot_password_visible,
            "clickable": forgot_password_clickable
        }
        
        if forgot_password_visible:
            allure.attach(
                self.login_page.forgot_password_link.screenshot(),
                name="forgot_password_link",
                attachment_type=allure.attachment_type.PNG
            )
        else:
            allure.attach(
                "Forgot password link is not visible",
                name="forgot_password_link_not_visible",
                attachment_type=allure.attachment_type.TEXT
            )
        
        return results
    
    @allure.step("Verify social login options are displayed")
    def verify_social_login_options(self) -> dict:
        """
        Verify all social login buttons and icons are displayed
        
        Returns:
            dict: Dictionary with social login button names as keys and dict with 'visible', 'clickable', and 'icon_visible' as values
        """
        results = {}
        
        # Verify social buttons block
        social_buttons_block_visible = self.login_page.verify_social_buttons_block_exists()
        results["social_buttons_block"] = {"visible": social_buttons_block_visible}
        
        if social_buttons_block_visible:
            try:
                # Wait for element to be visible and stable before taking screenshot
                social_buttons_block_locator = self.login_page.social_buttons_block
                social_buttons_block_locator.wait_for(state="visible", timeout=10000)
                # Take screenshot - element is already visible and stable
                allure.attach(
                    social_buttons_block_locator.screenshot(timeout=5000),
                    name="social_buttons_block",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                # If screenshot fails, try taking page screenshot as fallback
                try:
                    allure.attach(
                        self.page.screenshot(timeout=3000),
                        name="social_buttons_block_page_fallback",
                        attachment_type=allure.attachment_type.PNG
                    )
                    allure.attach(
                        f"Social buttons block screenshot failed, using page screenshot as fallback. Error: {str(e)}",
                        name="social_buttons_block_screenshot_info",
                        attachment_type=allure.attachment_type.TEXT
                    )
                except Exception:
                    # If all screenshots fail, attach error message
                    allure.attach(
                        f"Social buttons block screenshot failed - element may not be stable. Error: {str(e)}",
                        name="social_buttons_block_screenshot_failed",
                        attachment_type=allure.attachment_type.TEXT
                    )
        else:
            allure.attach(
                "Social buttons block 'div.socials-buttons' is not visible",
                name="social_buttons_block_not_visible",
                attachment_type=allure.attachment_type.TEXT
            )
        
        # Verify social login text
        social_text_visible = self.login_page.verify_social_login_text_exists()
        results["social_login_text"] = {"visible": social_text_visible}
        
        if social_text_visible:
            try:
                # Wait for element to be visible and stable before taking screenshot
                social_text_locator = self.login_page.social_login_text
                social_text_locator.wait_for(state="visible", timeout=10000)
                # Take screenshot - element is already visible and stable
                allure.attach(
                    social_text_locator.screenshot(timeout=5000),
                    name="social_login_text",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                # If screenshot fails, try taking page screenshot as fallback
                try:
                    allure.attach(
                        self.page.screenshot(timeout=3000),
                        name="social_login_text_page_fallback",
                        attachment_type=allure.attachment_type.PNG
                    )
                    allure.attach(
                        f"Social login text screenshot failed, using page screenshot as fallback. Error: {str(e)}",
                        name="social_login_text_screenshot_info",
                        attachment_type=allure.attachment_type.TEXT
                    )
                except Exception:
                    # If all screenshots fail, attach error message
                    allure.attach(
                        f"Social login text screenshot failed - element may not be stable. Error: {str(e)}",
                        name="social_login_text_screenshot_failed",
                        attachment_type=allure.attachment_type.TEXT
                    )
        
        # Verify all social login buttons
        social_buttons = self.login_page.get_all_social_login_buttons()
        social_icons = self.login_page.get_all_social_login_icons()
        
        # Map button names to icon names
        button_to_icon_map = {
            "Войти с помощью GitHub": "GitHub",
            "Войти с помощью VK": "VK",
            "Войти с помощью Google": "Google",
            "Войти с помощью Facebook": "Facebook",
            "Войти с помощью Twitter": "Twitter",
            "Войти с помощью Yandex": "Yandex"
        }
        
        for button_name, button_locator in social_buttons.items():
            count = 0
            is_visible = False
            is_clickable = False
            try:
                # Use shorter timeout for count check to avoid long waits
                count = button_locator.count()
                if count > 0:
                    is_visible = button_locator.first.is_visible(timeout=3000)
                    if is_visible:
                        is_clickable = button_locator.first.is_enabled()
            except Exception:
                is_visible = False
                is_clickable = False
            
            # Verify icon for this button - only check if button is visible
            icon_name = button_to_icon_map.get(button_name, "")
            icon_visible = False
            if icon_name and icon_name in social_icons and is_visible:
                try:
                    icon_locator = social_icons[icon_name]
                    # Use shorter timeout for icon checks since they're nested
                    icon_count = icon_locator.count()
                    if icon_count > 0:
                        icon_visible = icon_locator.first.is_visible(timeout=2000)
                except Exception:
                    icon_visible = False
            
            results[button_name] = {
                "visible": is_visible,
                "clickable": is_clickable,
                "icon_visible": icon_visible
            }
            
            if not is_visible:
                allure.attach(
                    f"Social login button '{button_name}' is not visible (count: {count if 'count' in locals() else 0})",
                    name=f"missing_social_button_{button_name}",
                    attachment_type=allure.attachment_type.TEXT
                )
            
            if not icon_visible and icon_name:
                allure.attach(
                    f"Social login icon '{icon_name}' for button '{button_name}' is not visible",
                    name=f"missing_social_icon_{icon_name}",
                    attachment_type=allure.attachment_type.TEXT
                )
        
        return results
    
    @allure.step("Verify registration link is displayed and clickable")
    def verify_registration_link(self) -> dict:
        """
        Verify registration text and link are displayed and clickable
        
        Returns:
            dict: Dictionary with 'text_visible', 'link_visible', and 'link_clickable' status
        """
        results = {}
        
        # Verify registration text
        text_visible = self.login_page.verify_registration_text_exists()
        results["text_visible"] = text_visible
        
        if text_visible:
            try:
                # Use shorter timeout for screenshot to avoid long waits
                allure.attach(
                    self.login_page.registration_text.screenshot(timeout=3000),
                    name="registration_text",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception:
                # If screenshot fails, attach a text message instead
                allure.attach(
                    "Registration text screenshot failed - element may not be stable",
                    name="registration_text_screenshot_failed",
                    attachment_type=allure.attachment_type.TEXT
                )
        
        # Verify registration link
        link_visible = self.login_page.verify_registration_link_exists()
        link_clickable = self.login_page.verify_registration_link_clickable() if link_visible else False
        
        results["link_visible"] = link_visible
        results["link_clickable"] = link_clickable
        
        if link_visible:
            try:
                # Use shorter timeout for screenshot to avoid long waits
                allure.attach(
                    self.login_page.registration_link.screenshot(timeout=3000),
                    name="registration_link",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception:
                # If screenshot fails, attach a text message instead
                allure.attach(
                    "Registration link screenshot failed - element may not be stable",
                    name="registration_link_screenshot_failed",
                    attachment_type=allure.attachment_type.TEXT
                )
        else:
            allure.attach(
                "Registration link is not visible",
                name="registration_link_not_visible",
                attachment_type=allure.attachment_type.TEXT
            )
        
        return results
    
    @allure.step("Verify captcha container is displayed")
    def verify_captcha_iframe_form(self) -> dict:
        """
        Verify captcha container is displayed
        
        Returns:
            dict: Dictionary with captcha container 'visible' status
        """
        results = {}
        
        # Verify captcha container
        container_visible = self.login_page.verify_captcha_container_exists()
        results["captcha_container"] = {"visible": container_visible}
        
        if container_visible:
            allure.attach(
                self.login_page.captcha_container.screenshot(),
                name="captcha_container",
                attachment_type=allure.attachment_type.PNG
            )
        else:
            allure.attach(
                "Captcha container is not visible",
                name="captcha_container_not_visible",
                attachment_type=allure.attachment_type.TEXT
            )
        
        return results

