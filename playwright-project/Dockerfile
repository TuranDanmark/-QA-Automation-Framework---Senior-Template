FROM mcr.microsoft.com/playwright/python:latest

WORKDIR /workspace

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Playwright browsers
RUN playwright install --with-deps

COPY . .

CMD ["pytest", "-n", "auto", "--alluredir=reports/allure-results"]
