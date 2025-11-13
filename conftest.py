"""
Pytest configuration and fixtures for Playwright tests
"""
import sys
import platform
import pytest
from pathlib import Path
from playwright.sync_api import Playwright, Browser, BrowserContext, Page
from steps.main_page_steps import MainPageSteps
from steps.login_page_steps import LoginPageSteps


def create_allure_environment_file():
    """Create environment.properties file for Allure report"""
    import pkg_resources
    
    # Get Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    # Get platform info
    platform_info = platform.platform()
    
    # Get installed packages
    installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    
    # Get pytest and related packages
    packages_info = {}
    for pkg_name in ['pytest', 'pluggy']:
        if pkg_name in installed_packages:
            packages_info[pkg_name] = installed_packages[pkg_name]
    
    # Get pytest plugins
    plugins_info = {}
    # Map of plugin display names to package keys
    plugin_mapping = {
        'allure-pytest': 'allure-pytest',
        'anyio': 'anyio',
        'Faker': 'Faker',
        'libtmux': 'libtmux',
        'base-url': 'pytest-base-url',
        'html': 'pytest-html',
        'metadata': 'pytest-metadata',
        'playwright': 'pytest-playwright',
        'xdist': 'pytest-xdist'
    }
    
    for display_name, package_key in plugin_mapping.items():
        # Try different variations of the package name
        possible_keys = [
            package_key,
            package_key.replace('-', '_'),
            package_key.replace('_', '-'),
            display_name,
            display_name.replace('-', '_')
        ]
        
        for key in possible_keys:
            if key in installed_packages:
                plugins_info[display_name] = installed_packages[key]
                break
    
    # Create allure-results directory if it doesn't exist
    allure_results_dir = Path('reports/allure-results')
    allure_results_dir.mkdir(parents=True, exist_ok=True)
    
    # Write environment.properties file
    env_file = allure_results_dir / 'environment.properties'
    
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(f"Python={python_version}\n")
        f.write(f"Platform={platform_info}\n")
        f.write("\n")
        f.write("# Packages\n")
        for pkg_name, pkg_version in packages_info.items():
            f.write(f"Packages.{pkg_name}={pkg_version}\n")
        f.write("\n")
        f.write("# Plugins\n")
        for plugin_name, plugin_version in plugins_info.items():
            f.write(f"Plugins.{plugin_name}={plugin_version}\n")
        f.write("\n")
        f.write("Base URL=\n")


def pytest_configure(config):
    """Pytest configuration hook - called before test collection"""
    create_allure_environment_file()


@pytest.fixture(scope="session")
def playwright() -> Playwright:
    """Playwright instance fixture"""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright: Playwright) -> Browser:
    """
    Browser instance fixture (shared across all tests)
    
    Args:
        playwright: Playwright instance
        
    Returns:
        Browser instance
    """
    browser = playwright.chromium.launch(
        headless=False,  # Set to True for headless mode
        slow_mo=100  # Slow down operations by 100ms for better visibility
    )
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def browser_context(browser: Browser) -> BrowserContext:
    """
    Browser context fixture (new context for each test)
    
    Args:
        browser: Browser instance
        
    Returns:
        BrowserContext instance
    """
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="ru-RU"  # Set locale to Russian for Habr.com
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(browser_context: BrowserContext) -> Page:
    """
    Page fixture (new page for each test)
    
    Args:
        browser_context: BrowserContext instance
        
    Returns:
        Page instance
    """
    page = browser_context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def main_page_steps(page: Page) -> MainPageSteps:
    """
    MainPageSteps fixture (provides steps instance for each test)
    
    Args:
        page: Page instance
        
    Returns:
        MainPageSteps instance
    """
    return MainPageSteps(page)


@pytest.fixture(scope="function")
def login_page_steps(page: Page) -> LoginPageSteps:
    """
    LoginPageSteps fixture (provides steps instance for each test)
    
    Args:
        page: Page instance
        
    Returns:
        LoginPageSteps instance
    """
    return LoginPageSteps(page)

