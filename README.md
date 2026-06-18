# Advanced Web Scraper Telegram Bot

## Overview

Advanced Web Scraper Bot is a feature-rich Telegram bot designed to perform comprehensive website analysis, asset collection, backend technology detection, and security reconnaissance. The bot automatically scans websites, downloads publicly accessible assets, identifies backend technologies, analyzes website structures, and generates detailed reports packaged in ZIP archives.

> **Disclaimer:** This tool is intended for educational, research, and authorized security assessment purposes only. Always obtain proper authorization before scanning or analyzing any website.

---

## Features

### Website Analysis

* Automatic website accessibility verification
* Website structure mapping
* Metadata extraction
* API endpoint discovery
* Form, script, image, and link analysis

### Backend Technology Detection

Detects common technologies including:

* PHP
* Laravel
* Django
* Flask
* Node.js
* Express.js
* ASP.NET
* WordPress
* Joomla
* Drupal
* Ruby on Rails

### Asset Collection

Downloads and organizes:

* HTML files
* CSS stylesheets
* JavaScript files
* Images
* Fonts
* Documents
* Media files
* Configuration files
* Source code files

### Security Analysis

Scans for indicators of:

* SQL Injection patterns
* Cross-Site Scripting (XSS)
* Hardcoded credentials
* Debug configurations
* Directory listing exposure
* Command execution functions
* File inclusion vulnerabilities

### Backend Discovery

Searches for common endpoints such as:

* Admin panels
* Login portals
* Configuration files
* Backup directories
* Debug pages
* API endpoints
* Sensitive files

### Reporting

Generates:

* Comprehensive analysis report
* Backend assessment report
* Vulnerability summary
* Asset inventory
* Download statistics
* ZIP archive containing all collected data

### Database Tracking

Stores:

* User information
* Scraping sessions
* Download statistics
* Asset metadata
* Backend findings

---

## Project Structure

```text
Advanced_Web_Scraper/
│
├── sessions/
├── reports/
├── temp/
├── backups/
│
├── html_files/
├── javascript/
├── stylesheets/
├── assets/
│   ├── images/
│   ├── media/
│   └── fonts/
│
├── backend/
│   ├── php_files/
│   ├── python/
│   ├── java/
│   ├── config/
│   └── detected/
│
├── documents/
├── archives/
├── executables/
│
├── comprehensive_analysis.json
├── backend_analysis.json
└── failed_assets.txt
```

---

## Requirements

### Python Version

```bash
Python 3.9+
```

### Dependencies

```bash
pip install pyTelegramBotAPI
pip install aiohttp
pip install aiofiles
pip install beautifulsoup4
pip install requests
pip install fake-useragent
pip install cloudscraper
pip install selenium
pip install undetected-chromedriver
```

Or install all at once:

```bash
pip install pyTelegramBotAPI aiohttp aiofiles beautifulsoup4 requests fake-useragent cloudscraper selenium undetected-chromedriver
```

---

## Configuration

Update the following variables inside the script:

```python
BOT_TOKEN = "YOUR_BOT_TOKEN"
OWNER_ID = YOUR_TELEGRAM_ID
OWNER_USERNAME = "@your_username"
```

Optional:

```python
CHANNEL1_LINK = "https://t.me/yourchannel"
CHANNEL2_LINK = "https://t.me/yourchannel2"
WELCOME_IMAGE_URL = "https://example.com/image.jpg"
```

---

## Running the Bot

```bash
python scrapper.py
```

Upon startup the bot will:

1. Initialize the database
2. Create required directories
3. Register Telegram commands
4. Start polling Telegram updates

---

## Available Commands

| Command  | Description              |
| -------- | ------------------------ |
| `/start` | Start the bot            |
| `/help`  | Display usage guide      |
| `/about` | About the project        |
| `/stats` | Show user statistics     |
| `/admin` | Admin panel (owner only) |

---

## How It Works

### Step 1: URL Submission

User sends:

```text
https://example.com
```

### Step 2: Analysis

The bot:

* Validates URL
* Detects technologies
* Maps website structure
* Searches backend endpoints

### Step 3: Asset Collection

Downloads:

* HTML
* CSS
* JavaScript
* Images
* Documents
* Backend files

### Step 4: Security Scan

Analyzes:

* Vulnerabilities
* Sensitive files
* Misconfigurations
* API exposure

### Step 5: Packaging

Creates:

```text
Advanced_Scrape_<domain>_<timestamp>.zip
```

### Step 6: Delivery

User receives:

* ZIP archive
* Analysis summary
* Backend report
* Security findings

---

## Database Schema

### Users

```sql
users
```

Stores:

* User ID
* Username
* Join date
* Last active date
* Total scrapes
* Download statistics

### Scraping Sessions

```sql
scraping_sessions
```

Stores:

* Session ID
* Target URL
* Start time
* End time
* Status
* Detected technologies

### Assets

```sql
assets
```

Stores:

* Asset URL
* Filename
* File type
* Size
* Download status

### Backend Files

```sql
backend_files
```

Stores:

* File path
* Vulnerability score
* Content preview

---

## Security Notice

This project performs automated scanning and resource collection.

You should:

* Only analyze websites you own or are authorized to test.
* Respect website terms of service.
* Follow local laws and regulations.
* Avoid unauthorized security testing.

The author is not responsible for misuse of this software.

---

## Logging

Logs are stored in:

```text
advanced_scraper_bot.log
```

Includes:

* Bot activity
* Errors
* Download events
* User actions
* Scan results

---

## Performance Settings

Default configuration:

```python
MAX_FILE_SIZE = 200 MB
MAX_ASSETS = 500
MAX_DEPTH = 3
CONCURRENT_DOWNLOADS = 25
CONCURRENT_REQUESTS = 20
REQUEST_TIMEOUT = 45
```

These values can be adjusted according to server resources.

---

## Technologies Used

* Python
* Telegram Bot API
* aiohttp
* BeautifulSoup4
* SQLite
* Selenium
* Undetected ChromeDriver
* Cloudscraper
* Requests

---

## Future Improvements

* Multi-page crawling
* Proxy support
* Scheduled scans
* PDF reporting
* Dashboard interface
* REST API
* Advanced vulnerability checks
* Docker deployment

---

## License

This project is provided for educational and research purposes.

Use responsibly and only against systems you are authorized to assess.

---

## Author

**SHAURYA**

Telegram:

```text
@SHAURYAOWNS
```

For support, bug reports, or feature requests, contact the project maintainer.
