# Habr UI Autotest

UI automation testing project for Habr.com website using Playwright, Python, Pytest, and Allure.

## 📋 Project Description

This project is designed for automated UI testing of the Habr.com website. The project uses modern technology stack to create reliable and maintainable UI tests.

### Key Features:

- ✅ Automated UI testing of Habr.com main page elements
- ✅ HTML test plan generation from text file
- ✅ Detailed Allure reports generation with screenshots and steps
- ✅ Pytest HTML reports generation
- ✅ Page Object Model (POM) architecture
- ✅ Allure support for detailed reporting

## 🏗️ Project Structure

```
HabrUIAutotest/
├── pages/                    # Page Object Model - page descriptions
│   ├── __init__.py
│   └── main_page.py          # Habr.com main page
├── steps/                    # Test steps (business logic + Allure)
│   ├── __init__.py
│   └── main_page_steps.py   # Steps for main page
├── tests/                    # Tests
│   ├── __init__.py
│   └── test_main_page_elements.py  # Main page elements tests
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

#### Run specific test:
```bash
pytest tests/test_main_page_elements.py
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

2. **Steps** (`steps/`) - Test steps
   - Combination of actions from Page Objects
   - Allure integration (screenshots, steps)
   - Validations and checks

3. **Tests** (`tests/`) - Tests
   - Test scenarios
   - Assertions
   - Allure annotations

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

# steps/new_page_steps.py
class NewPageSteps:
    @allure.step("Do something")
    def do_something(self):
        # Step logic
        pass

# tests/test_new_page.py
def test_new_feature(new_page_steps: NewPageSteps):
    new_page_steps.do_something()
```

## 📦 Dependencies

Main project dependencies:

- **playwright** (1.40.0) - Browser automation
- **pytest** (7.4.3) - Testing framework
- **pytest-playwright** (0.4.3) - Playwright integration with pytest
- **pytest-html** (4.1.1) - HTML reports
- **allure-pytest** (2.13.2) - Allure integration
- **python-dotenv** (1.0.0) - Working with .env files

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
- Timeout settings in `pages/main_page.py`
- Habr.com website availability

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
