# 🧩 Contributing to Web Crawler

Thanks for your interest in contributing to this project! Whether you're fixing a bug, adding a feature, improving documentation, or writing tests — your help is appreciated.

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
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Create a new branch for your work**

   ```bash
   git checkout -b feature/my-new-feature
   ```

---

## 🐳 Docker (Alternative Setup)

You can also contribute using Docker if you prefer working in containers.

### 🔨 Build the Image

```bash
docker build -t web-crawler .
```

### 🚀 Run the Crawler

```bash
docker run --rm web-crawler python src/web_crawler.py https://www.overstory.com/
```

### 🧪 Run Tests

Build and run tests using a dedicated test image:

```bash
docker build -t async-web-crawler-test -f Dockerfile.test .
docker run --rm async-web-crawler-test
```

This runs the full test suite (including async tests) in an isolated container.

---

## 💡 What You Can Contribute

- 🚀 New features or improvements (e.g. crawl depth, rate-limiting, content filters)
- 🐛 Bug fixes
- 🧪 Test coverage for crawler or parser logic
- 📖 Documentation improvements
- 🔧 Dev tooling or CI enhancements

---

## 🧪 Running Tests

Make sure all tests pass before submitting a pull request:

```bash
pytest
```

> Tests for asynchronous code use `pytest-asyncio`.

---

## 🧼 Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Use meaningful variable and function names
- Include docstrings for all public functions and classes
- Keep functions small and focused

---

## ✅ Pull Request Checklist

- [ ] Code is clean and well-documented
- [ ] Tests are included for any new functionality
- [ ] All tests pass
- [ ] Description of the change is included in the PR
- [ ] Linting and formatting are followed

---

## 📬 Submitting a Pull Request

When you're ready, push your branch and open a pull request on GitHub. Fill out the PR template with a clear description of your changes.

---

## 🙏 Code of Conduct

We aim to foster a welcoming and inclusive environment. By participating in this project, you agree to abide by our [Code of Conduct](https://www.contributor-covenant.org/version/2/0/code_of_conduct/).

---

## 📫 Questions?

Open an issue or reach out via GitHub Discussions if you need help or have questions. Thanks again for helping improve this project!
