"""
Test Case 1: Verify Main Page Elements
Tests for verifying that all main page elements are present and displayed correctly
"""
import pytest
import allure
from steps.main_page_steps import MainPageSteps


@allure.epic("Habr.com UI Tests")
@allure.feature("Main Page Elements")
@allure.story("TEST CASE 1: Verify Main Page Elements")
class TestMainPageElements:
    """Test class for verifying main page elements"""
    
    @allure.title("Verify all main page elements are present and visible")
    @allure.description(
        "This test verifies that all main page elements are present and displayed correctly on the main page.\n"
        "It checks:\n"
        "- Header container\n"
        "- Logo link\n"
        "- All content tabs (Статьи, Посты, Новости, Хабы, Авторы, Компании)\n"
        "- Header elements (Все потоки, Поиск, Написать публикацию, Настройки, Войти)\n"
        "- Main content area\n"
        "- Footer section"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("main_page", "elements", "smoke")
    @pytest.mark.smoke
    def test_verify_main_page_elements(self, main_page_steps: MainPageSteps):
        """
        Test to verify all main page elements are present and visible
        
        Args:
            main_page_steps: MainPageSteps fixture
        """
        # Step 1: Navigate to the main page
        with allure.step("Step 1: Navigate to the main page URL (https://habr.com)"):
            main_page_steps.navigate_to_main_page()
        
        # Step 2: Verify the header element exists
        with allure.step("Step 2: Verify the header element exists"):
            header_visible = main_page_steps.verify_header_container()
            assert header_visible, "Header container should be present and visible"
            allure.attach(
                "Header container with class 'tm-header__container' is present and visible",
                name="Header verification",
                attachment_type=allure.attachment_type.TEXT
            )
        
        # Step 3: Verify all content tabs are present and displayed
        with allure.step("Step 3: Verify all content tabs are present and displayed"):
            tabs_results = main_page_steps.verify_all_content_tabs()
            
            expected_tabs = ["Статьи", "Посты", "Новости", "Хабы", "Авторы", "Компании"]
            missing_tabs = [tab for tab in expected_tabs if not tabs_results.get(tab, False)]
            
            assert len(missing_tabs) == 0, (
                f"Some content tabs are missing or not visible: {missing_tabs}. "
                f"All tabs should be present: {expected_tabs}"
            )
            
            allure.attach(
                f"All content tabs are present and visible:\n" + 
                "\n".join([f"- {tab}: {'✓' if tabs_results.get(tab) else '✗'}" 
                          for tab in expected_tabs]),
                name="Content tabs verification",
                attachment_type=allure.attachment_type.TEXT
            )
        
        # Step 4: Verify other significant main page elements
        with allure.step("Step 4: Verify other significant main page elements"):
            # Verify logo link
            logo_visible = main_page_steps.verify_logo_link()
            assert logo_visible, "Logo link ('Хабр') should be present and visible"
            
            # Verify header elements
            header_elements_results = main_page_steps.verify_header_elements()
            
            expected_header_elements = [
                "Все потоки", 
                "Поиск", 
                "Написать публикацию", 
                "Настройки", 
                "Войти"
            ]
            missing_header_elements = [
                elem for elem in expected_header_elements 
                if not header_elements_results.get(elem, False)
            ]
            
            assert len(missing_header_elements) == 0, (
                f"Some header elements are missing or not visible: {missing_header_elements}. "
                f"All elements should be present: {expected_header_elements}"
            )
            
            # Verify main content area
            content_area_visible = main_page_steps.verify_main_content_area()
            assert content_area_visible, "Main content area should be present and visible"
            
            # Verify footer section
            footer_visible = main_page_steps.verify_footer_section()
            assert footer_visible, "Footer section should be present and visible"
            
            allure.attach(
                f"All main page elements verification:\n"
                f"- Logo link: {'✓' if logo_visible else '✗'}\n"
                f"- Header elements:\n" + 
                "\n".join([f"  - {elem}: {'✓' if header_elements_results.get(elem) else '✗'}" 
                          for elem in expected_header_elements]) + "\n"
                f"- Main content area: {'✓' if content_area_visible else '✗'}\n"
                f"- Footer section: {'✓' if footer_visible else '✗'}",
                name="Main page elements verification",
                attachment_type=allure.attachment_type.TEXT
            )
        
        # Final assertion: All elements should be present
        with allure.step("Verify all elements are present - Final Check"):
            all_checks = [
                header_visible,
                logo_visible,
                all(tabs_results.get(tab) for tab in expected_tabs),
                all(header_elements_results.get(elem) for elem in expected_header_elements),
                content_area_visible,
                footer_visible
            ]
            
            assert all(all_checks), (
                "Not all main page elements are present and visible. "
                "Please check the test results above for details."
            )
            
            allure.attach(
                "✓ All main page elements are present and displayed correctly",
                name="Final verification result",
                attachment_type=allure.attachment_type.TEXT
            )

