# LAB1 (Github Lab) - Bank Account Management System

[![Testing with Pytest and Coverage](https://github.com/Praniti03/Lab1_Github_MLOps/actions/workflows/github_lab1_pytest_action.yml/badge.svg)](https://github.com/Praniti03/Lab1_Github_MLOps/actions/workflows/github_lab1_pytest_action.yml) [![Python Unittests](https://github.com/Praniti03/Lab1_Github_MLOps/actions/workflows/github_lab2_unittest_action.yml/badge.svg)](https://github.com/Praniti03/Lab1_Github_MLOps/actions/workflows/github_lab2_unittest_action.yml)

## Assignment Overview

For this assignment, I have completed the Github Labs (Lab1) and implemented modifications by using a Bank Account Management System instead of the basic calculator. The output screenshots and GitHub Actions dashboard screens are attached in the file for reference, demonstrating the successful implementation and automated testing workflows.

## Modifications and Enhancements

This Assignment implements a **Bank Account Management System** instead of the basic calculator, demonstrating advanced MLOps practices and comprehensive testing strategies. Below are the key modifications made to the original lab requirements:

### 1. Enhanced Application - Bank Account Management System

**Original:** Basic calculator with 4 arithmetic functions (add, subtract, multiply, combine)

**Modified:** Complete banking system with 8 real-world functions:

- `deposit()` - Add funds to an account balance
- `withdraw()` - Withdraw funds with optional overdraft limit
- `calculate_interest()` - Calculate compound interest over time
- `apply_overdraft_fee()` - Apply a flat fee when balance goes negative
- `transfer_funds()` - Transfer money between two account balances
- `calculate_monthly_loan_payment()` - Calculate fixed monthly loan payments
- `convert_currency()` - Convert an amount using an exchange rate
- `check_minimum_balance()` - Validate minimum balance requirements

**Rationale:** Demonstrates more complex business logic and real-world financial application scenarios relevant to banking and fintech platforms.

### 2. Comprehensive Testing with Parametrization

**Original:** Basic test cases for each function

**Modified:** Expanded test suite including:

- Basic function tests
- **Parametrized tests** - Testing multiple scenarios in single test functions using `@pytest.mark.parametrize`
- Error handling tests - Validating all edge cases and exceptions
- Integration tests - Testing complete transfer and loan workflows
- High code coverage achieved via `pytest-cov`

**Example of parametrized test:**

```python
@pytest.mark.parametrize("balance, amount, expected", [
    (100, 50, 150),
    (0, 200, 200),
    (500, 0.01, 500.01),
])
def test_deposit(balance, amount, expected):
    assert deposit(balance, amount) == expected
```

### 3. Enhanced GitHub Actions with Coverage Reporting

**Original:** Basic pytest and unittest workflows

**Modified:** Advanced CI/CD pipeline with:

- Code coverage reporting using `pytest-cov`
- Test result artifacts (XML report) uploaded to GitHub
- Detailed test execution reports
- Both pytest and unittest automation maintained

### 4. Output Documentation

**Added:** `generate_output.py` script that creates `OUTPUT.txt`

**Purpose:**

- Automatically generates comprehensive output showing all functions in action
- Provides real-world banking scenarios (deposits, withdrawals, transfers, loans)
- Displays test execution summary
- Allows reviewers to see results without running code

**Features:**

- Complete deposit → withdraw → transfer workflows
- Compound interest and loan payment calculations
- Overdraft fee application
- Currency conversion
- Minimum balance validation

### 5. Professional Documentation

**Added:**

- Comprehensive README with usage examples
- Detailed function docstrings with clear behavior descriptions
- Clear project structure documentation

### 6. Advanced Error Handling

**Enhancement:** All functions include robust input validation:

- Type checking for all parameters
- Negative value prevention
- Insufficient funds / overdraft limit validation
- Clear, descriptive error messages

**Example:**

```python
if not isinstance(amount, (int, float)):
    raise ValueError("Amount must be a number.")
if amount <= 0:
    raise ValueError("Deposit amount must be positive.")
```

### 7. Real-World Business Logic

**Implementation:**

- Overdraft limits enforced on withdrawals
- Interest calculated using compound growth
- Loan payments calculated using standard amortization formula
- Fund transfers validated against sender's available balance
- Currency conversion restricted to positive exchange rates

### Summary of Deliverables

| Component           | Status   | Enhancement                         |
| -------------------- | -------- | ------------------------------------ |
| Virtual Environment   | Complete | As specified                         |
| GitHub Repository     | Complete | As specified                         |
| Source Code           | Enhanced | 8 functions vs 4 original             |
| Pytest Tests          | Enhanced | Parametrized + error-handling tests   |
| Unittest Tests        | Enhanced | Comprehensive coverage                |
| GitHub Actions        | Enhanced | Added coverage reporting              |
| Documentation         | Enhanced | Professional README + OUTPUT.txt      |
| Code Coverage         | Added    | Coverage report generated via pytest-cov |

---

## Project Overview

This lab demonstrates MLOps best practices including automated testing, continuous integration, code coverage analysis, and professional documentation standards through the implementation of a bank account management system.

---

## Step 1: Creating a Virtual Environment

In software development, it's crucial to manage project dependencies and isolate your project's environment from the global Python environment. This isolation ensures that your project remains consistent, stable, and free from conflicts with other Python packages or projects. To achieve this, we create a virtual environment dedicated to our project.

To create a virtual environment, follow these steps:

1. Open a Command Prompt or Terminal in the directory where you want to create your project.
2. Choose a name for your virtual environment (e.g "lab_01") and run the appropriate command:

```bash
python -m venv lab_01
```

3. Activate the virtual environment

```bash
# Windows
lab_01\Scripts\activate

# Mac/Linux
source lab_01/bin/activate
```

After activation, you will see the virtual environment's name in your command prompt or terminal, indicating that you are working within the virtual environment.

---

## Step 2: Creating a GitHub Repository, Cloning and Folder Structure

Now that we have set up our virtual environment, the next step is to create a GitHub repository for our project and establish a structured folder layout. This organization helps maintain your project's code, data, and tests in an organized manner.

### Creating a GitHub Repository

- Open a web browser and go to GitHub.
- In the upper right corner, click the "+" button and select "New repository."
- Choose a name for your repository.
- Choose the visibility of your repository — either public (visible to everyone) or private (accessible only to selected collaborators)
- Check the "Initialize this repository with a README" box. This will create an initial README file that you can edit to provide project documentation.
- Click the "Create repository" button.

### Cloning the Repository

- Open a Command Prompt or Terminal.
- Navigate to the directory where you want to clone your GitHub repository. This should be the same directory where you created your virtual environment.
- Run the following command to clone your GitHub repository into the current directory:

```bash
git clone <repository_url>
```

- Replace `<repository_url>` with the URL of your GitHub repository. You can find this URL on your GitHub repository's main page.

After running the command, the repository will be cloned, and you'll have a local copy of your GitHub project in your chosen directory.

### Establishing Folder Structure

Once you have cloned your repository, you can establish a structured folder layout within it. This layout helps organize your project into key directories for code, data, and tests. Create the following subfolders within your repository:

```
Lab1_Github_MLOps/
├── .github/
│   └── workflows/
│       ├── github_lab1_pytest_action.yml
│       └── github_lab2_unittest_action.yml
├── assets/
│   ├── S1.png
│   ├── S2.png
│   └── S3.png
├── data/
│   └── __init__.py
├── src/
│   ├── __init__.py
│   └── bank_account.py
├── test/
│   ├── __init__.py
│   ├── test_pytest.py
│   └── test_unittest.py
├── .gitignore
├── requirements.txt
├── generate_output.py
├── OUTPUT.txt
└── README.md
```

- **data:** This folder is used for storing project data files or datasets.
- **src:** This folder is where you'll store your project's source code files.
- **test:** This folder is dedicated to unit tests and test scripts for your code.
- Create a file named `.gitignore`. This is useful to exclude the virtual environment and other unnecessary files from version control.
- Add the virtual environment folder name inside your gitignore file so that it's not tracked by Git.

### Adding and Pushing Your Project Code to GitHub

Now that we have our virtual environment set up, the GitHub repository created, and the folder structure organized, let's add our project's code and push it to GitHub.

**Adding Your Project Code**

- Navigate to your project directory using the Command Prompt or Terminal, where you have the virtual environment and folder structure set up.
- Create and write your Python code or other project files within the specified directories (src, data, etc.) according to your project requirements.
- Once your project files are ready, it's time to add them to Git's staging area. In your project directory, run the following command:

```bash
git add .
```

- This command stages all the changes and new files in your project directory for the next commit.

**Committing Your Changes**

- After staging your changes, commit them with a meaningful commit message that describes the changes you made. Replace `<your_commit_message>` with a descriptive message:

```bash
git commit -m "<your_commit_message>"
```

**Pushing to GitHub**

- To push your committed changes to your GitHub repository, use the following command:

```bash
git push origin main
```

---

## Step 3: Creating bank_account.py in src Folder

In this step, we create a Python script named `bank_account.py` within the src folder of your project. This script contains a set of banking functions designed to perform account management operations.

### Functions Implemented:

1. **deposit(balance, amount)** - Adds funds to the account balance
2. **withdraw(balance, amount, overdraft_limit=0)** - Withdraws funds, allowing an optional overdraft limit
3. **calculate_interest(balance, annual_rate, years=1)** - Calculates compound interest earned over time
4. **apply_overdraft_fee(balance, fee=35)** - Applies a flat fee if the account balance is negative
5. **transfer_funds(from_balance, to_balance, amount)** - Transfers funds between two account balances
6. **calculate_monthly_loan_payment(principal, annual_rate, months)** - Calculates a fixed monthly loan payment
7. **convert_currency(amount, exchange_rate)** - Converts an amount using a given exchange rate
8. **check_minimum_balance(balance, minimum=100)** - Checks whether the account meets a minimum balance requirement

All functions include comprehensive error handling, input validation, and detailed docstrings.

> **Note:** Whenever you want to push files to your repository follow the steps in [Adding and Pushing Your Project Code to GitHub](#adding-and-pushing-your-project-code-to-github)

---

## Step 4: Creating tests using Pytest and Unittests

In this step, we'll set up unit tests for the functions in our `bank_account.py` script using two popular testing frameworks: [pytest](https://docs.pytest.org/en/7.4.x/) and [unittest](https://docs.python.org/3/library/unittest.html). Unit testing ensures that individual components of your code work as expected, helping you catch and fix bugs early in the development process.

### Using Pytest

**Installation:**

```bash
pip install pytest pytest-cov
```

### Writing Pytest Tests

- Pytest makes it easy to write tests for your Python code. Tests are written as regular Python functions, and test file names typically start with `test_` or end with `_test.py`.
- To run your Pytest tests, you can use the pytest command:

```bash
pytest test/test_pytest.py -v
```

- To run with coverage:

```bash
python -m pytest test/test_pytest.py --cov=src --cov-report=term-missing -v
```

**Parametrized Tests:** This project uses parametrized tests extensively, allowing the same test function to run with multiple sets of inputs:

```python
@pytest.mark.parametrize("balance, amount, expected", [
    (100, 50, 150),
    (0, 200, 200),
    (500, 0.01, 500.01),
])
def test_deposit(balance, amount, expected):
    assert deposit(balance, amount) == expected
```

**Test Coverage:** Pytest tests covering all functions, edge cases, and error conditions (insufficient funds, invalid types, negative values).

### Writing Tests with UnitTest

- Unittest allows you to write tests as classes that inherit from the `unittest.TestCase` class.
- To run Unittest tests:

```bash
python -m unittest test.test_unittest -v
```

- Unittest provides assertion methods such as `assertEqual`, `assertTrue`, `assertFalse`, and `assertRaises` to validate test conditions.
- The `test_unittest.py` file contains comprehensive test cases mirroring the pytest implementation.

---

## Step 5: Implementing GitHub Actions

GitHub Actions is a powerful automation and CI/CD (Continuous Integration/Continuous Deployment) platform provided by GitHub. It enables you to automate various workflows and tasks directly within your GitHub repository.

### How GitHub Actions Work:

- **Events:** Specific activities that occur within your GitHub repository, such as code pushes or pull requests.
- **Actions:** Individual tasks or steps defined in a workflow file.
- **Triggers:** Conditions that cause a workflow to run.

### The Purpose of GitHub Actions:

- **Automation:** Reduces manual effort and ensures consistency
- **Continuous Integration (CI):** Automatically build, test, and validate code changes
- **Continuous Deployment (CD):** Enable automatic deployment when changes are merged

### Creating GitHub Actions Workflow Files:

Two workflow files are created under the `.github/workflows` directory:

**1. github_lab1_pytest_action.yml** - Pytest with Coverage

This workflow:

- Triggers on push to main branch
- Sets up Python 3.11 environment
- Installs dependencies from requirements.txt
- Runs pytest with coverage reporting
- Generates a code coverage report
- Uploads test results and coverage as artifacts
- Notifies on success/failure

**2. github_lab2_unittest_action.yml** - Unittest Automation

This workflow:

- Triggers on push to main branch
- Sets up Python 3.11 environment
- Installs dependencies
- Runs unittest test suite
- Notifies on success/failure

Both workflows ensure code quality by automatically running all tests on every push or pull request.

---

## Step 6: Generating Output Documentation

### Running the Output Generator

To generate comprehensive output documentation:

```bash
python generate_output.py
```

This creates `OUTPUT.txt` containing:

- Complete usage examples (deposit, withdraw, transfer, interest, loan payment, currency conversion)
- Real-world banking scenarios
- Test execution summary

**Sample Output:**

[![Example 1](assets/S6.png)](assets/S6.png)

The OUTPUT.txt file demonstrates all functions working correctly with various test cases and edge conditions.

---

### GitHub Actions Pipeline Results

**Complete Actions Dashboard:**

[![Actions Dashboard](assets/S5.png)](assets/S5.png)
*Both pytest and unittest workflows running automatically on every push*

**Pytest Workflow Success:**

[![Pytest Workflow Runs](assets/S3.png)](assets/S3.png)

[![Pytest Workflow Details](assets/S2.png)](assets/S2.png)

**Unittest Workflow Success:**

[![Unittest Workflow Run](assets/S4.png)](assets/S4.png)

[![Unittest Workflow Details](assets/S1.png)](assets/S1.png)

---

## Running Tests Locally

```bash
# Activate virtual environment
lab_01\Scripts\activate  # Windows
source lab_01/bin/activate  # Mac/Linux

# Run pytest
pytest test/test_pytest.py -v

# Run pytest with coverage
python -m pytest test/test_pytest.py --cov=src --cov-report=term-missing -v

# Run unittest
python -m unittest test.test_unittest -v

# Generate output documentation
python generate_output.py
```

---

## Test Results Summary

- **Test Status:** All passing
- **Code Coverage:** Generated via pytest-cov (see Actions artifacts)
- **Parametrized Tests:** Multiple scenarios tested per function
- **Error Handling:** All edge cases validated (negative values, invalid types, insufficient funds)

---

## Technologies Used

- Python 3.11+
- Pytest (testing framework)
- pytest-cov (coverage analysis)
- Unittest (Python's built-in testing)
- GitHub Actions (CI/CD automation)
- Git (version control)

---

## Project Features

- Comprehensive bank account management functionality
- Robust error handling and input validation
- Parametrized testing for multiple scenarios
- Automated CI/CD pipeline
- Professional documentation
- Real-world financial business logic implementation

---

**Praniti**

- Course: IE-7374 MLOps
- Assignment 1 (Github Lab): Bank Account Management System
