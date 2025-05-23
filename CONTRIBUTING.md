# 🧩 Contributing to Web Crawler

Thanks for your interest in contributing to this project! Whether you're fixing a bug, adding a feature, improving documentation, or writing tests — your help is appreciated.

---

## Table of Contents

- [Getting Started](#-getting-started)
- [Docker](#-docker-alternative-setup)
- [Run Tests](#-run-tests)
  - [Unit Tests](#unit-tests)
  - [Integration Tests](#integration-tests)
- [What You Can Contribute](#-what-you-can-contribute)
- [Code Style](#-code-style)
  - [Running Automated Code Style Checks](#running-automated-code-style-checks)
  - [Pre-Commit](#pre-commit)
- [Submitting a Pull Request](#-submitting-a-pull-request)
- [Code of Conduct](#-code-of-conduct)
- [Questions?](#-questions)

---

## 🛠️ Getting Started

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/mfdickerson/web-crawler.git
   cd web-crawler
   ```
3. **Create a virtual environment**

   It's recommended to isolate your environment using `venv`. Directions for a Mac:

   ```bash
   cd src
   virtualenv -p python3.13 venv && source venv/bin/activate
   pip install -r requirements/dev.txt
   ```

4. **Install dependencies**

   ```bash
   pip install -r requirements/dev.txt
   ```

5. **Create a new branch for your work**

   ```bash
   git checkout -b feature/my-new-feature
   ```

6. **Build the Docker Image**

   From the root of the project directory:

   ```bash
   docker build -t web-crawler .
   ```

## 🚀 Run the Crawler

Replace `<URL>` with your desired starting point:

```bash
docker run --rm web-crawler <URL> [--max_page_limit=<100>]
```

---

## 🧪 Run Tests

Make sure all tests pass before submitting a pull request:

### Unit Tests
Run test unit tests by starting virtual environment, installing dependencies and running `pytest`:

```bash
cd src
virtualenv -p python3.13 venv && source venv/bin/activate
pip install -r requirements/dev.txt
pytest
```

### Integration Tests
Run integration tests by starting virtual environment, installing dependencies and running `pytest`:

```bash
cd test/integration
virtualenv -p python3.13 venv && source venv/bin/activate
pip install -r requirements.txt
pytest
```

---

## 💡 What You Can Contribute

- 🚀 New features or improvements (e.g. crawl depth, rate-limiting, content filters)
- 🐛 Bug fixes
- 🧪 Test coverage for crawler or parser logic
- 📖 Documentation improvements
- 🔧 Dev tooling or CI enhancements

---

## 🧼 Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Use meaningful variable and function names
- Include docstrings for all public functions and classes
- Keep functions small and focused
- Uses Black, Flake8, iSort, 

### Running Automated Code Style Checks

To ensure consistent code style across the project, run the following tools before submitting your changes:

```bash
# Auto-format with Black
black src/ tests/

# Sort imports with isort
isort src/ tests/

# Lint with Flake8
flake8 src/ tests/

# Lint with Pylint
pylint src/ tests/
```

### Pre-Commit

The easiest way to make sure your Pull Request adheres to the code style is to install [pre-commit](https://pre-commit.com/). To set up pre-commit locally, run the following command after [sourcing the virtual environment](#️-getting-started):

```
pre-commit install
```

---

## 📬 Submitting a Pull Request

When you're ready, push your branch and open a pull request on GitHub. Fill out the PR template with a clear description of your changes.

### GitHub Actions

There are several GitHub Actions that will run against Pull Requests when they are opened, reopened,
or synchronized. The following checks ensure that code quality analyses and unit tests run against
each PR before it is merged into `main`:

- Code Style Checks
  - iSort
- Unit Tests

To learn more, read the [GitHub Actions documentation](https://docs.github.com/en/actions) or view
the files in this repo under the `.github/workflows/` directory.

### ✅ Pull Request Checklist

- [ ] Code is clean and well-documented
- [ ] Tests are included for any new functionality
- [ ] All tests pass
- [ ] Description of the change is included in the PR
- [ ] Linting and formatting are followed

---

## 🙏 Code of Conduct

We aim to foster a welcoming and inclusive environment. By participating in this project, you agree to abide by our [Code of Conduct](https://www.contributor-covenant.org/version/2/0/code_of_conduct/).

---

## 📫 Questions?

Open an issue or reach out via GitHub Discussions if you need help or have questions. Thanks again for helping improve this project!
