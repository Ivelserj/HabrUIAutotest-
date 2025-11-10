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


@allure.epic("Habr.com UI Tests")
@allure.feature("Main Menu Functionality")
@allure.story("TEST CASE 2: Verify Main Menu Functionality")
class TestMainMenuFunctionality:
    """Test class for verifying main menu functionality"""
    
    @allure.title("Verify main menu can be opened and closed, and all menu options are displayed and clickable")
    @allure.description(
        "This test verifies the main menu functionality on the main page.\n"
        "It checks:\n"
        "- Menu button exists and is clickable\n"
        "- Menu opens successfully\n"
        "- All main menu options are displayed and clickable\n"
        "- 'Все сервисы Хабра' section is displayed with all service links\n"
        "- Menu closes successfully"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("main_page", "menu", "smoke")
    @pytest.mark.smoke
    def test_verify_main_menu_functionality(self, main_page_steps: MainPageSteps):
        """
        Test to verify main menu functionality
        
        Args:
            main_page_steps: MainPageSteps fixture
        """
        # Step 1: Navigate to the main page
        with allure.step("Step 1: Navigate to the main page URL (https://habr.com)"):
            main_page_steps.navigate_to_main_page()
        
        # Step 2: Verify the menu button exists
        with allure.step("Step 2: Verify the menu button exists"):
            menu_button_results = main_page_steps.verify_menu_button()
            assert menu_button_results["exists"], "Menu button should be present and visible"
            assert menu_button_results["clickable"], "Menu button should be clickable"
            allure.attach(
                f"Menu button exists: {menu_button_results['exists']}, "
                f"clickable: {menu_button_results['clickable']}",
                name="Menu button verification",
                attachment_type=allure.attachment_type.TEXT
            )
        
        # Step 3: Open the menu
        with allure.step("Step 3: Open the menu"):
            main_page_steps.open_menu()
            menu_panel_visible = main_page_steps.verify_menu_panel_displayed()
            assert menu_panel_visible, "Menu panel should be displayed and visible after opening"
            allure.attach(
                "Menu opened successfully and menu panel is displayed",
                name="Menu opened verification",
                attachment_type=allure.attachment_type.TEXT
            )
        
        # Step 4: Verify main menu options are displayed
        with allure.step("Step 4: Verify main menu options are displayed"):
            menu_options_results = main_page_steps.verify_menu_options()
            
            expected_menu_options = [
                "Что нового",
                "Бэкенд",
                "Фронтенд",
                "Администрирование",
                "Дизайн",
                "Менеджмент",
                "Маркетинг и контент",
                "Научпоп",
                "Разработка",
                "Все потоки"
            ]
            
            missing_options = [
                option for option in expected_menu_options
                if not menu_options_results.get(option, {}).get("visible", False)
            ]
            
            not_clickable_options = [
                option for option in expected_menu_options
                if menu_options_results.get(option, {}).get("visible", False)
                and not menu_options_results.get(option, {}).get("clickable", False)
            ]
            
            assert len(missing_options) == 0, (
                f"Some menu options are missing or not visible: {missing_options}. "
                f"All options should be present: {expected_menu_options}"
            )
            
            assert len(not_clickable_options) == 0, (
                f"Some menu options are not clickable: {not_clickable_options}. "
                f"All visible options should be clickable"
            )
            
            options_status = "\n".join([
                f"- {option}: visible={menu_options_results.get(option, {}).get('visible', False)}, "
                f"clickable={menu_options_results.get(option, {}).get('clickable', False)}"
                for option in expected_menu_options
            ])
            
            allure.attach(
                f"All main menu options verification:\n{options_status}",
                name="Menu options verification",
                attachment_type=allure.attachment_type.TEXT
            )
        
        # Step 5: Verify "Все сервисы Хабра" section
        with allure.step("Step 5: Verify 'Все сервисы Хабра' section"):
            services_results = main_page_steps.verify_services_section()
            
            assert services_results["section_header"], (
                "'Все сервисы Хабра' section header should be present and visible"
            )
            
            expected_service_links = ["Хабр", "Q&A", "Карьера", "Курсы"]
            service_links_results = services_results.get("service_links", {})
            
            missing_service_links = [
                link for link in expected_service_links
                if not service_links_results.get(link, {}).get("visible", False)
            ]
            
            not_clickable_service_links = [
                link for link in expected_service_links
                if service_links_results.get(link, {}).get("visible", False)
                and not service_links_results.get(link, {}).get("clickable", False)
            ]
            
            assert len(missing_service_links) == 0, (
                f"Some service links are missing or not visible: {missing_service_links}. "
                f"All service links should be present: {expected_service_links}"
            )
            
            assert len(not_clickable_service_links) == 0, (
                f"Some service links are not clickable: {not_clickable_service_links}. "
                f"All visible service links should be clickable"
            )
            
            service_links_status = "\n".join([
                f"- {link}: visible={service_links_results.get(link, {}).get('visible', False)}, "
                f"clickable={service_links_results.get(link, {}).get('clickable', False)}"
                for link in expected_service_links
            ])
            
            allure.attach(
                f"'Все сервисы Хабра' section verification:\n"
                f"Section header: {services_results['section_header']}\n"
                f"Service links:\n{service_links_status}",
                name="Services section verification",
                attachment_type=allure.attachment_type.TEXT
            )
        
        # Step 6: Verify menu options functionality
        with allure.step("Step 6: Verify menu options functionality"):
            # Verify menu structure is correct
            all_options_visible = all(
                menu_options_results.get(option, {}).get("visible", False)
                for option in expected_menu_options
            )
            assert all_options_visible, "All menu options should be properly displayed in the menu"
            
            allure.attach(
                "Menu structure is correct and all menu options are properly displayed",
                name="Menu structure verification",
                attachment_type=allure.attachment_type.TEXT
            )
        
        # Step 7: Close the menu
        with allure.step("Step 7: Close the menu"):
            main_page_steps.close_menu()
            menu_panel_hidden = main_page_steps.verify_menu_panel_hidden()
            assert menu_panel_hidden, "Menu panel should be hidden or not displayed after closing"
            allure.attach(
                "Menu closed successfully and menu panel is hidden",
                name="Menu closed verification",
                attachment_type=allure.attachment_type.TEXT
            )
        
        # Final assertion: All menu functionality should work correctly
        with allure.step("Verify all menu functionality works correctly - Final Check"):
            all_checks = [
                menu_button_results["exists"],
                menu_button_results["clickable"],
                menu_panel_visible,
                all(menu_options_results.get(option, {}).get("visible", False) 
                    for option in expected_menu_options),
                all(menu_options_results.get(option, {}).get("clickable", False) 
                    for option in expected_menu_options),
                services_results["section_header"],
                all(service_links_results.get(link, {}).get("visible", False) 
                    for link in expected_service_links),
                all(service_links_results.get(link, {}).get("clickable", False) 
                    for link in expected_service_links),
                menu_panel_hidden
            ]
            
            assert all(all_checks), (
                "Not all menu functionality works correctly. "
                "Please check the test results above for details."
            )
            
            allure.attach(
                "✓ All main menu functionality works correctly:\n"
                "- Menu button exists and is clickable\n"
                "- Menu opens successfully\n"
                "- All menu options are displayed and clickable\n"
                "- 'Все сервисы Хабра' section is displayed with all service links\n"
                "- Menu closes successfully",
                name="Final verification result",
                attachment_type=allure.attachment_type.TEXT
            )
