# Habr UI Autotest

UI automation testing project for Habr.com website using Playwright, Python, Pytest, and Allure.

## 📋 Project Description

This project is designed for automated UI testing of the Habr.com website. The project uses modern technology stack to create reliable and maintainable UI tests.

### Key Features:

- ✅ Automated UI testing of Habr.com main page elements
- ✅ Login modal/window testing and verification
- ✅ Main menu functionality testing
- ✅ Footer functionality testing
- ✅ HTML test plan generation from text file
- ✅ Detailed Allure reports generation with screenshots and steps
- ✅ Pytest HTML reports generation
- ✅ Page Object Model (POM) architecture
- ✅ Allure support for detailed reporting
- ✅ Explicit waits only (no hardcoded sleeps or implicit waits)

## 🏗️ Project Structure

```
HabrUIAutotest/
├── pages/                    # Page Object Model - page descriptions
│   ├── __init__.py
│   ├── main_page.py          # Habr.com main page
│   └── login_page.py         # Habr.com login modal/page
├── steps/                    # Test steps (business logic + Allure)
│   ├── __init__.py
│   ├── main_page_steps.py    # Steps for main page
│   └── login_page_steps.py   # Steps for login page
├── tests/                    # Tests
│   ├── __init__.py
│   └── test_main_page_elements.py  # Main page and login tests
├── reports/                  # Reports
│   ├── allure-results/       # Allure results
│   ├── allure-report/        # Generated Allure report
│   └── report.html           # Pytest HTML report
├── conftest.py               # Pytest configuration and fixtures
├── pytest.ini                # Pytest settings
├── requirements.txt          # Python dependencies
├── setup.py                  # Setup script
├── test_plan.txt             # Text test plan
├── test_plan.html            # HTML version of test plan
└── convert_test_plan_to_html.py  # Test plan conversion script
```

## 🚀 Installation and Setup

### Requirements

- Python 3.8 or higher
- pip (Python package manager)
- Allure (for report generation)

### Step 1: Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### Step 2: Install Allure

**Windows:**
```bash
# Via Scoop
scoop install allure

# Or via Chocolatey
choco install allure
```

**Linux/Mac:**
```bash
# Via npm
npm install -g allure-commandline
```

### Step 3: Verify Installation

```bash
# Check Python
python --version

# Check pytest
pytest --version

# Check Allure
allure --version

# Check Playwright
playwright --version
```

## 📖 Usage

### 1. Generate HTML Test Plan

Convert text test plan (`test_plan.txt`) to HTML format:

```bash
python convert_test_plan_to_html.py
```

This will create `test_plan.html` file and automatically open it in the browser.

**Test plan format:**
- Main items start with `-`
- Sub-items start with `*` and have indentation
- Hierarchical structure is supported

### 2. Run Autotests

#### Run all tests:
```bash
pytest
```

#### Run specific test file:
```bash
pytest tests/test_main_page_elements.py
```

#### Run specific test class:
```bash
# Main page elements test
pytest tests/test_main_page_elements.py::TestMainPageElements

# Main menu functionality test
pytest tests/test_main_page_elements.py::TestMainMenuFunctionality

# Footer functionality test
pytest tests/test_main_page_elements.py::TestFooterFunctionality

# Authorization button functionality test
pytest tests/test_main_page_elements.py::TestAuthorizationButtonFunctionality
```

#### Run with markers:
```bash
# Only smoke tests
pytest -m smoke

# Only main_page tests
pytest -m main_page
```

#### Run in parallel mode:
```bash
pytest -n auto
```

#### Run with verbose output:
```bash
pytest -v -s
```

### 3. Generate Allure Report

#### Step 1: Generate report
```bash
allure generate reports/allure-results -o reports/allure-report --clean
```

#### Step 2: Open report

**Option 1: Via HTTP server (recommended)**
```bash
# Start HTTP server
cd reports/allure-report
python -m http.server 8080

# Open in browser: http://localhost:8080
```

**Option 2: Via Allure serve**
```bash
allure serve reports/allure-results
```

**Option 3: Direct opening (may not work due to CORS)**
```bash
# Windows
start reports/allure-report/index.html

# Linux
xdg-open reports/allure-report/index.html

# Mac
open reports/allure-report/index.html
```

### 4. View Pytest HTML Report

HTML report is automatically generated when running tests and saved to `reports/report.html`.

Open the file in browser:
```bash
# Windows
start reports/report.html
```

## 🏛️ Project Architecture

The project uses **Page Object Model (POM)** with an additional **Steps** layer:

```
Tests (tests/)
    ↓ uses
Steps (steps/)          # Business logic + Allure integration
    ↓ uses
Pages (pages/)          # Page Objects - technical details
    ↓ uses
Playwright API          # Low-level operations
```

### Components:

1. **Pages** (`pages/`) - Page Object Model
   - Page element descriptions
   - Basic operations (navigation, element search)
   - Element locators
   - **main_page.py**: Main page elements (header, menu, footer, content tabs)
   - **login_page.py**: Login modal elements (form fields, buttons, social login, captcha)

2. **Steps** (`steps/`) - Test steps
   - Combination of actions from Page Objects
   - Allure integration (screenshots, steps)
   - Validations and checks
   - **main_page_steps.py**: Steps for main page interactions
   - **login_page_steps.py**: Steps for login modal interactions

3. **Tests** (`tests/`) - Tests
   - Test scenarios
   - Assertions
   - Allure annotations
   - **test_main_page_elements.py**: Contains 4 test classes:
     - `TestMainPageElements`: Main page elements verification
     - `TestMainMenuFunctionality`: Main menu open/close and options verification
     - `TestFooterFunctionality`: Footer elements and links verification
     - `TestAuthorizationButtonFunctionality`: Login modal opening and elements verification

### Best Practices:

- ✅ **Explicit waits only**: No `time.sleep()`, `wait_for_timeout()`, or hardcoded timeout values
- ✅ **Playwright auto-waiting**: Leverages Playwright's built-in waiting mechanisms
- ✅ **Element state waits**: Uses `wait_for(state="visible")` for explicit element state checks
- ✅ **No implicit waits**: Avoids `implicitly_wait()` or similar mechanisms

## 📊 Reporting

### Allure Report

Allure report includes:
- ✅ Detailed information about each test
- ✅ Screenshots at each step
- ✅ Environment information (Python version, platform, packages)
- ✅ Test execution history
- ✅ Charts and statistics

### Pytest HTML Report

HTML report includes:
- ✅ List of all tests
- ✅ Execution results
- ✅ Environment information
- ✅ Execution logs

## 🔧 Configuration

### pytest.ini

Main pytest settings are in `pytest.ini`:
- Test paths
- Output options
- Test markers
- Logging settings

### conftest.py

Contains:
- Playwright fixtures (browser, page, context)
- Test steps fixtures
- Automatic generation of `environment.properties` for Allure

## 📝 Test Plan

Text test plan (`test_plan.txt`) contains:
- Test case descriptions
- Execution steps
- Expected results

To generate HTML version use:
```bash
python convert_test_plan_to_html.py
```

## 🛠️ Development

### Adding a New Test

1. Create Page Object in `pages/` (if new page is needed)
2. Create Steps in `steps/` for business logic
3. Create test in `tests/` using Steps

### Example structure:

```python
# pages/new_page.py
class NewPage:
    def __init__(self, page):
        self.page = page
    
    @property
    def element(self):
        return self.page.locator("selector")
    
    def verify_element_exists(self) -> bool:
        try:
            return self.element.is_visible()  # Uses Playwright auto-waiting
        except Exception:
            return False

# steps/new_page_steps.py
class NewPageSteps:
    def __init__(self, page):
        self.page = page
        self.new_page = NewPage(page)
    
    @allure.step("Do something")
    def do_something(self):
        # Wait explicitly for element state, not hardcoded timeout
        self.new_page.element.wait_for(state="visible")
        # Step logic
        pass

# tests/test_new_page.py
def test_new_feature(new_page_steps: NewPageSteps):
    new_page_steps.do_something()
```

### Important: Wait Strategy

**❌ DON'T:**
```python
time.sleep(5)  # Never use sleep
page.wait_for_timeout(500)  # Never use wait_for_timeout
element.is_visible(timeout=5000)  # Avoid hardcoded timeouts
```

**✅ DO:**
```python
element.wait_for(state="visible")  # Explicit state wait
element.is_visible()  # Uses Playwright default timeout
page.wait_for_load_state("networkidle")  # Explicit load state wait
```

## 📦 Dependencies

Main project dependencies:

- **playwright** (1.40.0) - Browser automation
- **pytest** (7.4.3) - Testing framework
- **pytest-playwright** (0.4.3) - Playwright integration with pytest
- **pytest-html** (4.1.1) - HTML reports
- **pytest-xdist** (3.5.0) - Parallel test execution
- **allure-pytest** (2.13.2) - Allure integration
- **python-dotenv** (1.0.0) - Working with .env files

See `requirements.txt` for exact versions.

## 🐛 Troubleshooting

### Issue: Allure report shows "Loading..."

**Solution:** Allure reports should be opened via HTTP server, not directly as a file.

```bash
cd reports/allure-report
python -m http.server 8080
# Open http://localhost:8080
```

### Issue: Tests fail with TimeoutError

**Solution:** Check:
- Internet speed
- Habr.com website availability
- Playwright uses explicit waits by default - no hardcoded timeouts needed
- If needed, adjust timeout in `wait_for()` calls, but avoid hardcoded `timeout=` values

### Issue: Browser doesn't start

**Solution:** Make sure Playwright browsers are installed:

```bash
playwright install chromium
```

## 📄 License

This project is created for educational purposes.

## 👥 Authors

Project created for automated UI testing of Habr.com website.

## 🔗 Useful Links

- [Playwright Documentation](https://playwright.dev/python/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Allure Documentation](https://docs.qameta.io/allure/)
- [Habr.com](https://habr.com)

---

**Note:** This project uses Page Object Model and Allure to create reliable and maintainable UI tests.
