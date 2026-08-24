# CodeReview AI

An AI-powered code review platform that analyzes Python source files and ZIP projects using Google Gemini.

The application provides automated code-quality analysis, issue detection, project-level insights, review history, and downloadable PDF reports through a FastAPI web interface.

## Features

- Upload individual Python files
- Upload complete ZIP projects
- AI-powered code review using Google Gemini
- Code quality scoring from 0–10
- Bug detection
- Security issue detection
- Performance issue detection
- PEP8 / style issue detection
- Strengths and weaknesses analysis
- Improvement suggestions
- Project-level AI analysis
- Architecture assessment
- Security assessment
- Performance assessment
- Maintainability assessment
- Project risk analysis
- Review history
- Individual project review pages
- Downloadable PDF reports
- Modern responsive web interface

## Tech Stack

- Python
- FastAPI
- Google Gemini API
- Jinja2
- HTML
- CSS
- JavaScript
- JSON-based project history
- Uvicorn

## Project Structure

```text
ai-software-review-platform/
│
├── app/
│   ├── api/
│   ├── services/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   ├── templates/
│   ├── data/
│   └── main.py
│
├── uploads/
├── .env
├── .gitignore
├── requirements.txt
└── README.md

