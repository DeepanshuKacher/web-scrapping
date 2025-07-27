# web Scraping Tool

## Features I have implemented
 - Three levels of data extraction (user can choose which level they want)
 - Pagination and URL Discovery
 - both api and cli support

## Setup Instructions
1. **Clone the Repository**
   ```zsh
   git clone git@github.com:DeepanshuKacher/web-scrapping.git
   cd backend
   ```
2. **Create and Activate Virtual Environment**
   ```zsh
   python3 -m venv env
   source env/bin/activate
   ```
3. **Install Dependencies**
   ```zsh
   pip install -r requirements.txt
   ```

## How to run the tool

**Option 1 CLI**
 - python main_app_advanced.py 
 - enter cli prompts

**Option 2 API**
- python api_server.py
- http://0.0.0.0:8000/docs   :- for api documentation
- http://localhost:8000//process   :- access api