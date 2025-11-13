"""
Page Object Model for Habr.com login page/modal
"""
from playwright.sync_api import Page, Locator
from typing import Dict


class LoginPage:
    """Page Object Model for Habr.com login modal/window"""
    
    def __init__(self, page: Page):
        """
        Initialize LoginPage with Playwright page object
        
        Args:
            page: Playwright Page instance
        """
        self.page = page
    
    # Login modal/window container
    @property
    def login_modal(self) -> Locator:
        """Login modal/window container"""
        # Try multiple selectors for login modal - could be a modal overlay, dialog, or form
        return self.page.locator('div[class*="modal"], div[class*="dialog"], div[class*="popup"], form[class*="login"], div[class*="auth"]').filter(
            has=self.page.get_by_text("Войти", exact=False)
        ).first.or_(
            self.page.locator('div:has(input[type="email"]):has(input[type="password"])').first
        )
    
    # Login form title and labels
    @property
    def login_title(self) -> Locator:
        """Login title text ('Вход')"""
        return self.page.get_by_text("Вход", exact=True).or_(
            self.login_modal.get_by_text("Вход", exact=True)
        ).first
    
    @property
    def email_label(self) -> Locator:
        """Email label text"""
        return self.page.get_by_text("Email", exact=True).or_(
            self.login_modal.get_by_text("Email", exact=True)
        ).first
    
    @property
    def password_label(self) -> Locator:
        """Password label text ('Пароль')"""
        return self.page.get_by_text("Пароль", exact=True).or_(
            self.login_modal.get_by_text("Пароль", exact=True)
        ).first
    
    # Login form fields
    @property
    def email_input(self) -> Locator:
        """Email input field"""
        return self.page.get_by_label("Email").or_(
            self.page.locator('input[type="email"]')
        ).or_(
            self.page.locator('input[name*="email"], input[id*="email"]')
        ).first
    
    @property
    def password_input(self) -> Locator:
        """Password input field ('Пароль')"""
        return self.page.get_by_label("Пароль").or_(
            self.page.locator('input[type="password"]')
        ).or_(
            self.page.locator('input[name*="password"], input[id*="password"]')
        ).first
    
    # Login form buttons and links
    @property
    def login_submit_button(self) -> Locator:
        """Login submit button ('Войти')"""
        return self.login_modal.get_by_role("button", name="Войти").or_(
            self.page.get_by_role("button", name="Войти").filter(
                has=self.page.locator('input[type="email"], input[type="password"]').locator("..").locator("..")
            )
        ).first
    
    @property
    def forgot_password_link(self) -> Locator:
        """Forgot password link ('Забыли пароль?')"""
        return self.page.get_by_role("link", name="Забыли пароль?").or_(
            self.page.get_by_text("Забыли пароль?", exact=False)
        ).first
    
    # Social login section
    @property
    def social_buttons_block(self) -> Locator:
        """Social buttons block container"""
        return self.page.locator('div.socials-buttons')
    
    @property
    def social_login_text(self) -> Locator:
        """Social login text ('Или войдите с помощью других сервисов')"""
        return self.page.get_by_text("Или войдите с помощью других сервисов", exact=False).or_(
            self.page.get_by_text("войдите с помощью других сервисов", exact=False)
        ).first
    
    @property
    def social_login_github(self) -> Locator:
        """GitHub social login button ('Войти с помощью GitHub')"""
        return self.page.get_by_role("button", name="Войти с помощью GitHub").or_(
            self.page.locator('button, a').filter(has_text="GitHub")
        ).first
    
    @property
    def social_login_vk(self) -> Locator:
        """VK social login button ('Войти с помощью VK')"""
        return self.page.get_by_role("button", name="Войти с помощью VK").or_(
            self.page.locator('button, a').filter(has_text="VK")
        ).first
    
    @property
    def social_login_google(self) -> Locator:
        """Google social login button ('Войти с помощью Google')"""
        return self.page.get_by_role("button", name="Войти с помощью Google").or_(
            self.page.locator('button, a').filter(has_text="Google")
        ).first
    
    @property
    def social_login_facebook(self) -> Locator:
        """Facebook social login button ('Войти с помощью Facebook')"""
        return self.page.get_by_role("button", name="Войти с помощью Facebook").or_(
            self.page.locator('button, a').filter(has_text="Facebook")
        ).first
    
    @property
    def social_login_twitter(self) -> Locator:
        """Twitter social login button ('Войти с помощью Twitter')"""
        return self.page.get_by_role("button", name="Войти с помощью Twitter").or_(
            self.page.locator('button, a').filter(has_text="Twitter")
        ).first
    
    @property
    def social_login_yandex(self) -> Locator:
        """Yandex social login button ('Войти с помощью Yandex')"""
        return self.page.get_by_role("button", name="Войти с помощью Yandex").or_(
            self.page.locator('button, a').filter(has_text="Yandex")
        ).first
    
    # Social login icons
    @property
    def social_login_icon_github(self) -> Locator:
        """GitHub social login icon"""
        return self.social_login_github.locator('img[alt*="GitHub"], img[src*="github"], svg, img').first
    
    @property
    def social_login_icon_vk(self) -> Locator:
        """VK social login icon"""
        return self.social_login_vk.locator('img[alt*="VK"], img[src*="vk"], svg, img').first
    
    @property
    def social_login_icon_google(self) -> Locator:
        """Google social login icon"""
        return self.social_login_google.locator('img[alt*="Google"], img[src*="google"], svg, img').first
    
    @property
    def social_login_icon_facebook(self) -> Locator:
        """Facebook social login icon"""
        return self.social_login_facebook.locator('img[alt*="Facebook"], img[src*="facebook"], svg, img').first
    
    @property
    def social_login_icon_twitter(self) -> Locator:
        """Twitter social login icon"""
        return self.social_login_twitter.locator('img[alt*="Twitter"], img[src*="twitter"], svg, img').first
    
    @property
    def social_login_icon_yandex(self) -> Locator:
        """Yandex social login icon"""
        return self.social_login_yandex.locator('img[alt*="Yandex"], img[src*="yandex"], svg, img').first
    
    # Registration section
    @property
    def registration_text(self) -> Locator:
        """Registration text ('Ещё нет аккаунта?')"""
        return self.page.get_by_text("Ещё нет аккаунта?", exact=False).first
    
    @property
    def registration_link(self) -> Locator:
        """Registration link ('Зарегистрируйтесь')"""
        return self.page.get_by_role("link", name="Зарегистрируйтесь").or_(
            self.page.get_by_text("Зарегистрируйтесь", exact=False)
        ).first
    
    # Captcha section
    @property
    def captcha_container(self) -> Locator:
        """Smart captcha container"""
        return self.page.get_by_test_id('smartCaptcha-container')
    
    @property
    def captcha_iframe(self) -> Locator:
        """Captcha iframe"""
        return self.captcha_container.locator('iframe').first
    
    @property
    def captcha_frame_locator(self):
        """Captcha iframe frame locator - recommended way to access iframe content"""
        # Use frame_locator on page with specific selector for captcha iframe
        # First ensure captcha container exists, then get iframe within it
        return self.page.frame_locator('[data-testid="smartCaptcha-container"] iframe').first
    
    def get_captcha_checkbox(self):
        """Get captcha checkbox locator inside iframe"""
        try:
            # Wait for captcha container to be visible first
            if not self.captcha_container.is_visible(timeout=5000):
                return None
            
            # First try using frame_locator (recommended approach)
            frame_loc = self.captcha_frame_locator
            # Try multiple possible selectors for the checkbox
            selectors = [
                'div.CheckboxCaptcha-Checkbox',
                'div[class*="CheckboxCaptcha"]',
                'div[class*="checkbox"]',
                'span[role="checkbox"]',
                '#checkbox-captcha',
                '.checkbox-captcha'
            ]
            for selector in selectors:
                try:
                    locator = frame_loc.locator(selector).first
                    if locator.count() > 0:
                        return locator
                except Exception:
                    continue
        except Exception:
            pass
        
        # Fallback to content_frame approach
        try:
            iframe = self.captcha_iframe
            if iframe.count() > 0:
                # Wait for iframe to be visible
                iframe.wait_for(state="visible", timeout=5000)
                # Get frame content
                frame = iframe.content_frame()
                if frame:
                    # Wait for frame to load
                    frame.wait_for_load_state(timeout=10000)
                    # Try multiple selectors
                    selectors = [
                        'div.CheckboxCaptcha-Checkbox',
                        'div[class*="CheckboxCaptcha"]',
                        'div[class*="checkbox"]',
                        'span[role="checkbox"]'
                    ]
                    for selector in selectors:
                        try:
                            locator = frame.locator(selector).first
                            if locator.count() > 0:
                                return locator
                        except Exception:
                            continue
        except Exception:
            pass
        return None
    
    def get_captcha_title(self):
        """Get captcha title locator inside iframe"""
        try:
            # First try using frame_locator (recommended approach)
            frame_loc = self.captcha_frame_locator
            return frame_loc.locator('span#checkbox-label').first
        except Exception:
            # Fallback to content_frame approach
            try:
                iframe = self.captcha_iframe
                if iframe.count() > 0:
                    # Wait for iframe to be visible
                    iframe.wait_for(state="visible", timeout=5000)
                    # Get frame content
                    frame = iframe.content_frame()
                    if frame:
                        # Wait for frame to load
                        frame.wait_for_load_state(timeout=10000)
                        return frame.locator('span#checkbox-label').first
            except Exception:
                pass
        return None
    
    def get_captcha_description(self):
        """Get captcha description locator inside iframe"""
        try:
            # First try using frame_locator (recommended approach)
            frame_loc = self.captcha_frame_locator
            return frame_loc.locator('span#checkbox-description').first
        except Exception:
            # Fallback to content_frame approach
            try:
                iframe = self.captcha_iframe
                if iframe.count() > 0:
                    # Wait for iframe to be visible
                    iframe.wait_for(state="visible", timeout=5000)
                    # Get frame content
                    frame = iframe.content_frame()
                    if frame:
                        # Wait for frame to load
                        frame.wait_for_load_state(timeout=10000)
                        return frame.locator('span#checkbox-description').first
            except Exception:
                pass
        return None
    
    def get_captcha_links(self):
        """Get captcha links locator inside iframe"""
        try:
            # First try using frame_locator (recommended approach)
            frame_loc = self.captcha_frame_locator
            return frame_loc.locator('div.CaptchaLinks-Links').first
        except Exception:
            # Fallback to content_frame approach
            try:
                iframe = self.captcha_iframe
                if iframe.count() > 0:
                    # Wait for iframe to be visible
                    iframe.wait_for(state="visible", timeout=5000)
                    # Get frame content
                    frame = iframe.content_frame()
                    if frame:
                        # Wait for frame to load
                        frame.wait_for_load_state(timeout=10000)
                        return frame.locator('div.CaptchaLinks-Links').first
            except Exception:
                pass
        return None
    
    # Verification methods
    def verify_login_modal_exists(self) -> bool:
        """Verify login modal exists and is visible"""
        try:
            return self.login_modal.is_visible(timeout=5000)
        except Exception:
            return False
    
    def verify_login_title_exists(self) -> bool:
        """Verify login title text 'Вход' exists and is visible"""
        try:
            return self.login_title.is_visible(timeout=5000)
        except Exception:
            return False
    
    def verify_email_label_exists(self) -> bool:
        """Verify email label text exists and is visible"""
        try:
            return self.email_label.is_visible(timeout=5000)
        except Exception:
            return False
    
    def verify_password_label_exists(self) -> bool:
        """Verify password label text 'Пароль' exists and is visible"""
        try:
            return self.password_label.is_visible(timeout=5000)
        except Exception:
            return False
    
    def verify_email_input_exists(self) -> bool:
        """Verify email input field exists and is visible"""
        try:
            return self.email_input.is_visible(timeout=5000)
        except Exception:
            return False
    
    def verify_password_input_exists(self) -> bool:
        """Verify password input field exists and is visible"""
        try:
            return self.password_input.is_visible(timeout=5000)
        except Exception:
            return False
    
    def verify_email_input_enabled(self) -> bool:
        """Verify email input field is enabled"""
        try:
            return self.email_input.is_enabled()
        except Exception:
            return False
    
    def verify_password_input_enabled(self) -> bool:
        """Verify password input field is enabled"""
        try:
            return self.password_input.is_enabled()
        except Exception:
            return False
    
    def verify_login_submit_button_exists(self) -> bool:
        """Verify login submit button exists and is visible"""
        try:
            return self.login_submit_button.is_visible(timeout=5000)
        except Exception:
            return False
    
    def verify_login_submit_button_clickable(self) -> bool:
        """Verify login submit button is clickable"""
        try:
            return self.login_submit_button.is_enabled()
        except Exception:
            return False
    
    def verify_forgot_password_link_exists(self) -> bool:
        """Verify forgot password link exists and is visible"""
        try:
            return self.forgot_password_link.is_visible(timeout=5000)
        except Exception:
            return False
    
    def verify_forgot_password_link_clickable(self) -> bool:
        """Verify forgot password link is clickable"""
        try:
            return self.forgot_password_link.is_enabled()
        except Exception:
            return False
    
    def verify_social_login_text_exists(self) -> bool:
        """Verify social login text exists and is visible"""
        try:
            return self.social_login_text.is_visible(timeout=5000)
        except Exception:
            return False
    
    def verify_social_buttons_block_exists(self) -> bool:
        """Verify social buttons block exists and is visible"""
        try:
            return self.social_buttons_block.is_visible(timeout=5000)
        except Exception:
            return False
    
    def get_all_social_login_buttons(self) -> Dict[str, Locator]:
        """Get dictionary of all social login button locators"""
        return {
            "Войти с помощью GitHub": self.social_login_github,
            "Войти с помощью VK": self.social_login_vk,
            "Войти с помощью Google": self.social_login_google,
            "Войти с помощью Facebook": self.social_login_facebook,
            "Войти с помощью Twitter": self.social_login_twitter,
            "Войти с помощью Yandex": self.social_login_yandex
        }
    
    def get_all_social_login_icons(self) -> Dict[str, Locator]:
        """Get dictionary of all social login icon locators"""
        return {
            "GitHub": self.social_login_icon_github,
            "VK": self.social_login_icon_vk,
            "Google": self.social_login_icon_google,
            "Facebook": self.social_login_icon_facebook,
            "Twitter": self.social_login_icon_twitter,
            "Yandex": self.social_login_icon_yandex
        }
    
    def verify_registration_text_exists(self) -> bool:
        """Verify registration text exists and is visible"""
        try:
            return self.registration_text.is_visible(timeout=5000)
        except Exception:
            return False
    
    def verify_registration_link_exists(self) -> bool:
        """Verify registration link exists and is visible"""
        try:
            return self.registration_link.is_visible(timeout=5000)
        except Exception:
            return False
    
    def verify_registration_link_clickable(self) -> bool:
        """Verify registration link is clickable"""
        try:
            return self.registration_link.is_enabled()
        except Exception:
            return False
    
    def verify_captcha_container_exists(self) -> bool:
        """Verify captcha container exists and is visible"""
        try:
            return self.captcha_container.is_visible(timeout=5000)
        except Exception:
            return False
    
    def verify_captcha_iframe_exists(self) -> bool:
        """Verify captcha iframe exists"""
        try:
            return self.captcha_iframe.count() > 0
        except Exception:
            return False
    
    def verify_captcha_checkbox_exists(self) -> bool:
        """Verify captcha checkbox exists and is visible inside iframe"""
        try:
            checkbox = self.get_captcha_checkbox()
            if checkbox:
                # Give more time for iframe content to load
                return checkbox.is_visible(timeout=15000)
            return False
        except Exception:
            return False
    
    def verify_captcha_title_exists(self) -> bool:
        """Verify captcha title exists and is visible inside iframe"""
        try:
            title = self.get_captcha_title()
            if title:
                # Give more time for iframe content to load
                return title.is_visible(timeout=15000)
            return False
        except Exception:
            return False
    
    def verify_captcha_description_exists(self) -> bool:
        """Verify captcha description exists and is visible inside iframe"""
        try:
            description = self.get_captcha_description()
            if description:
                # Give more time for iframe content to load
                return description.is_visible(timeout=15000)
            return False
        except Exception:
            return False
    
    def verify_captcha_links_exists(self) -> bool:
        """Verify captcha links container exists and is visible inside iframe"""
        try:
            links = self.get_captcha_links()
            if links:
                # Give more time for iframe content to load
                return links.is_visible(timeout=15000)
            return False
        except Exception:
            return False

