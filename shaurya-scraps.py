import os
import re
import zipfile
import asyncio
import aiohttp
import time
import telebot
import json
import hashlib
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
import shutil
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from fake_useragent import UserAgent
import random
import subprocess
import sys
import urllib3
from typing import Dict, List, Tuple, Optional, Set
import xml.etree.ElementTree as ET
import sqlite3
import aiofiles
import cloudscraper
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import base64
import mimetypes

# ==================== ENHANCED CONFIGURATION ====================
BOT_TOKEN = ""
OWNER_ID = 
OWNER_USERNAME = 

# Channel Settings
CHANNEL1_LINK = ""
CHANNEL2_ID = 
CHANNEL2_LINK = ""
WELCOME_IMAGE_URL = "A"

# Bot Settings
MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB (increased)
MAX_ASSETS = 500  # Increased asset limit
MAX_DEPTH = 3  # Maximum crawl depth
REQUEST_TIMEOUT = 45
CONCURRENT_DOWNLOADS = 25  # Increased concurrent downloads
CONCURRENT_REQUESTS = 20
MAX_PAGES_PER_DOMAIN = 100

# Backend Detection Settings
BACKEND_PATTERNS = {
    'php': ['.php', 'index.php', 'wp-content', 'wp-includes', 'wp-admin', 'config.php', 'admin.php'],
    'laravel': ['/storage/', '/app/', '/database/', '/resources/', 'artisan', '.env.example'],
    'django': ['/static/', '/media/', '/admin/', 'settings.py', 'urls.py', 'manage.py'],
    'flask': ['/static/', '/templates/', 'app.py', 'run.py'],
    'nodejs': ['package.json', 'node_modules', 'app.js', 'server.js', 'index.js'],
    'ruby': ['Gemfile', 'config.ru', '.rb', 'rails'],
    'aspnet': ['.aspx', '.ashx', '.asmx', 'web.config'],
    'wordpress': ['wp-json', 'xmlrpc.php', 'wp-login.php'],
    'joomla': ['/administrator/', 'index.php?option='],
    'drupal': ['/sites/', '/modules/', '/themes/'],
    'express': ['/routes/', '/controllers/', '/models/'],
}

# Sensitive Files
SENSITIVE_FILES = [
    '.env', '.git/config', '.htaccess', 'web.config', 'config.php',
    'wp-config.php', 'database.yml', 'settings.py', 'config.json',
    'robots.txt', 'sitemap.xml', 'package.json', 'composer.json',
    'admin/', 'administrator/', 'wp-admin/', 'cgi-bin/'
]

# Common Backend Endpoints
BACKEND_ENDPOINTS = [
    # PHP endpoints
    '/admin/index.php', '/admin/login.php', '/admin/admin.php',
    '/config.php', '/db.php', '/database.php',
    '/phpinfo.php', '/test.php', '/debug.php',
    
    # WordPress
    '/wp-admin/', '/wp-login.php', '/wp-config.php',
    '/xmlrpc.php', '/wp-json/wp/v2/users',
    
    # Laravel
    '/.env', '/storage/logs/laravel.log',
    
    # Django
    '/admin/login/', '/admin/', '/static/admin/',
    
    # Generic
    '/cgi-bin/', '/server-status', '/phpmyadmin/',
    '/adminer.php', '/backup/', '/database/',
    '/logs/', '/error_log', '/debug/',
]

# Database file
DB_FILE = 'scraper_database.db'

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

# Setup enhanced logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
    handlers=[
        logging.FileHandler('advanced_scraper_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Enhanced User Agent
ua = UserAgent()

# SSL context for bypassing SSL verification
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==================== ENHANCED FOLDER CONFIGURATION ====================
FOLDERS = {
    '.html': 'html_files',
    '.htm': 'html_files',
    '.php': 'backend/php_files',
    '.js': 'javascript',
    '.css': 'stylesheets',
    '.scss': 'stylesheets',
    '.sass': 'stylesheets',
    '.less': 'stylesheets',
    '.json': 'data/json',
    '.xml': 'data/xml',
    '.csv': 'data/csv',
    '.sql': 'backend/database',
    '.py': 'backend/python',
    '.rb': 'backend/ruby',
    '.java': 'backend/java',
    '.jar': 'backend/java',
    '.war': 'backend/java',
    '.go': 'backend/go',
    '.rs': 'backend/rust',
    '.c': 'backend/c',
    '.cpp': 'backend/cpp',
    '.cs': 'backend/csharp',
    '.swift': 'backend/swift',
    '.kt': 'backend/kotlin',
    '.dart': 'backend/dart',
    '.ts': 'backend/typescript',
    '.jsx': 'backend/react',
    '.tsx': 'backend/react',
    '.vue': 'backend/vue',
    '.env': 'backend/config',
    '.config': 'backend/config',
    '.yml': 'backend/config',
    '.yaml': 'backend/config',
    '.toml': 'backend/config',
    '.ini': 'backend/config',
    '.sh': 'backend/scripts',
    '.bat': 'backend/scripts',
    '.ps1': 'backend/scripts',
    '.md': 'documentation',
    '.txt': 'documentation',
    '.pdf': 'documents',
    '.doc': 'documents',
    '.docx': 'documents',
    '.xls': 'documents',
    '.xlsx': 'documents',
    '.ppt': 'documents',
    '.pptx': 'documents',
    '.odt': 'documents',
    '.ods': 'documents',
    '.odp': 'documents',
    '.jpg': 'assets/images',
    '.jpeg': 'assets/images',
    '.png': 'assets/images',
    '.gif': 'assets/images',
    '.svg': 'assets/images',
    '.webp': 'assets/images',
    '.bmp': 'assets/images',
    '.ico': 'assets/images',
    '.tiff': 'assets/images',
    '.webm': 'assets/media',
    '.mp4': 'assets/media',
    '.avi': 'assets/media',
    '.mov': 'assets/media',
    '.wmv': 'assets/media',
    '.flv': 'assets/media',
    '.mkv': 'assets/media',
    '.mp3': 'assets/media',
    '.wav': 'assets/media',
    '.ogg': 'assets/media',
    '.m4a': 'assets/media',
    '.aac': 'assets/media',
    '.flac': 'assets/media',
    '.woff': 'assets/fonts',
    '.woff2': 'assets/fonts',
    '.ttf': 'assets/fonts',
    '.otf': 'assets/fonts',
    '.eot': 'assets/fonts',
    '.zip': 'archives',
    '.rar': 'archives',
    '.7z': 'archives',
    '.tar': 'archives',
    '.gz': 'archives',
    '.bz2': 'archives',
    '.exe': 'executables',
    '.msi': 'executables',
    '.dmg': 'executables',
    '.apk': 'executables',
    '.deb': 'executables',
    '.rpm': 'executables',
}

BASE_DIR = 'Advanced_Web_Scraper'
USER_DATA_FILE = 'user_data.json'
SCRAPING_SESSIONS_FILE = 'scraping_sessions.json'

# ==================== DATABASE FUNCTIONS ====================
def init_database():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP,
            total_scrapes INTEGER DEFAULT 0,
            total_assets_downloaded INTEGER DEFAULT 0,
            total_size_downloaded INTEGER DEFAULT 0,
            banned INTEGER DEFAULT 0
        )
    ''')
    
    # Create scraping_sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scraping_sessions (
            session_id TEXT PRIMARY KEY,
            user_id INTEGER,
            url TEXT,
            start_time TIMESTAMP,
            end_time TIMESTAMP,
            total_files INTEGER,
            total_size INTEGER,
            status TEXT,
            backend_detected TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    # Create assets table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assets (
            asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            url TEXT,
            filename TEXT,
            filetype TEXT,
            size INTEGER,
            download_status TEXT,
            FOREIGN KEY (session_id) REFERENCES scraping_sessions (session_id)
        )
    ''')
    
    # Create backend_files table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS backend_files (
            file_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            path TEXT,
            content_preview TEXT,
            vulnerability_score INTEGER,
            FOREIGN KEY (session_id) REFERENCES scraping_sessions (session_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def update_user_in_db(user_id, username, first_name):
    """Update user in database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR REPLACE INTO users 
        (user_id, username, first_name, last_active) 
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
    ''', (user_id, username, first_name))
    
    conn.commit()
    conn.close()

def increment_user_scrapes(user_id):
    """Increment user's scrape count"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE users 
        SET total_scrapes = total_scrapes + 1,
            last_active = CURRENT_TIMESTAMP
        WHERE user_id = ?
    ''', (user_id,))
    
    conn.commit()
    conn.close()

def save_scraping_session(session_data):
    """Save scraping session to database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO scraping_sessions 
        (session_id, user_id, url, start_time, end_time, total_files, total_size, status, backend_detected)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        session_data['session_id'],
        session_data['user_id'],
        session_data['url'],
        session_data['start_time'],
        session_data['end_time'],
        session_data['total_files'],
        session_data['total_size'],
        session_data['status'],
        session_data.get('backend_detected', '')
    ))
    
    conn.commit()
    conn.close()

# ==================== ENHANCED UTILITY FUNCTIONS ====================
def format_text(text):
    """Convert text to stylish font with emojis"""
    char_map = {
        'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ',
        'f': 'ꜰ', 'g': 'ɢ', 'h': 'ʜ', 'i': 'ɪ', 'j': 'ᴊ',
        'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ',
        'p': 'ᴘ', 'q': 'ǫ', 'r': 'ʀ', 's': 'ꜱ', 't': 'ᴛ',
        'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x', 'y': 'ʏ',
        'z': 'ᴢ'
    }
    
    result = []
    for char in text:
        if char.lower() in char_map:
            result.append(char_map[char.lower()])
        else:
            result.append(char)
    
    return ''.join(result)

def detect_backend_technology(url, soup, content, response_headers=None):
    """Detect backend technology used by website"""
    detected_techs = []
    html_lower = str(soup).lower() if soup else ''
    content_lower = content.lower() if content else ''
    
    # Check for specific patterns in HTML
    for tech, patterns in BACKEND_PATTERNS.items():
        for pattern in patterns:
            if pattern in html_lower or pattern in content_lower:
                detected_techs.append(tech)
                break
    
    # Check response headers
    if response_headers:
        headers_lower = {k.lower(): v.lower() for k, v in response_headers.items()}
        
        # Check server header
        server = headers_lower.get('server', '')
        if 'apache' in server:
            detected_techs.append('apache')
        if 'nginx' in server:
            detected_techs.append('nginx')
        if 'iis' in server:
            detected_techs.append('iis')
        if 'cloudflare' in server:
            detected_techs.append('cloudflare')
        
        # Check X-Powered-By header
        powered_by = headers_lower.get('x-powered-by', '')
        if 'php' in powered_by:
            detected_techs.append('php')
        if 'asp.net' in powered_by:
            detected_techs.append('aspnet')
        if 'express' in powered_by:
            detected_techs.append('express')
        
        # Check X-Generator header (for CMS)
        generator = headers_lower.get('x-generator', '')
        if 'wordpress' in generator:
            detected_techs.append('wordpress')
        if 'drupal' in generator:
            detected_techs.append('drupal')
        if 'joomla' in generator:
            detected_techs.append('joomla')
    
    # Check URL patterns
    parsed_url = urlparse(url)
    path_lower = parsed_url.path.lower()
    
    if '.php' in path_lower:
        detected_techs.append('php')
    if '.aspx' in path_lower:
        detected_techs.append('aspnet')
    if '.jsp' in path_lower:
        detected_techs.append('java')
    if '.py' in path_lower:
        detected_techs.append('python')
    
    return list(set(detected_techs))

async def find_backend_files(base_url, session):
    """Find backend files by trying common endpoints"""
    found_files = []
    
    for endpoint in BACKEND_ENDPOINTS:
        test_url = urljoin(base_url, endpoint)
        try:
            async with session.get(test_url, timeout=5, ssl=False) as response:
                if response.status in [200, 403, 401, 500]:
                    # Try to get content for analysis
                    try:
                        content = await response.read()
                        content_str = content.decode('utf-8', errors='ignore')[:1000]
                        
                        # Analyze content for technology indicators
                        vulnerabilities = analyze_vulnerabilities(content_str, test_url)
                        
                        found_files.append({
                            'url': test_url,
                            'path': endpoint,
                            'status': response.status,
                            'size': len(content),
                            'vulnerabilities': vulnerabilities,
                            'content_preview': content_str[:200]
                        })
                    except:
                        found_files.append({
                            'url': test_url,
                            'path': endpoint,
                            'status': response.status,
                            'size': 0,
                            'vulnerabilities': [],
                            'content_preview': ''
                        })
        except:
            continue
    
    return found_files

def analyze_vulnerabilities(content, filepath):
    """Analyze file content for potential vulnerabilities"""
    vulnerabilities = []
    
    if not content or not isinstance(content, str):
        return vulnerabilities
    
    content_lower = content.lower()
    
    # Common vulnerability patterns
    patterns = {
        'sql_injection': [
            r'select\s.*\sfrom',
            r'insert\s+into',
            r'update\s.*\sset',
            r'delete\s+from',
            r'drop\s+table',
            r'union\s+select'
        ],
        'xss': [
            r'<script>',
            r'alert\(',
            r'document\.cookie',
            r'eval\(',
            r'innerhtml\s*=',
            r'document\.write\('
        ],
        'hardcoded_credentials': [
            r'password\s*=\s*[\'"][^\'"]+[\'"]',
            r'api[_-]?key\s*=\s*[\'"][^\'"]+[\'"]',
            r'secret\s*=\s*[\'"][^\'"]+[\'"]',
            r'token\s*=\s*[\'"][^\'"]+[\'"]',
            r'db[_-]?password\s*=\s*[\'"][^\'"]+[\'"]'
        ],
        'debug_mode': [
            r'debug\s*=\s*true',
            r'debug_mode\s*=\s*true',
            r'app\.debug\s*=\s*true',
            r'display_errors\s*=\s*on'
        ],
        'file_inclusion': [
            r'include\s*\([^)]*\$_',
            r'require\s*\([^)]*\$_',
            r'file_get_contents\s*\([^)]*\$_'
        ],
        'command_injection': [
            r'system\s*\(',
            r'exec\s*\(',
            r'shell_exec\s*\(',
            r'passthru\s*\(',
            r'popen\s*\('
        ]
    }
    
    for vuln_type, regex_list in patterns.items():
        for regex in regex_list:
            if re.search(regex, content_lower, re.IGNORECASE):
                vulnerabilities.append(vuln_type)
                break
    
    # Check for PHP info disclosure
    if 'phpinfo()' in content_lower:
        vulnerabilities.append('php_info_disclosure')
    
    # Check for exposed directories
    if 'index of /' in content_lower:
        vulnerabilities.append('directory_listing')
    
    return vulnerabilities

async def fetch_with_retry(session, url, max_retries=3):
    """Fetch URL content with retry logic and random user agent"""
    headers = {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    
    for attempt in range(max_retries):
        try:
            timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
            async with session.get(url, headers=headers, timeout=timeout, ssl=False) as response:
                if response.status == 200:
                    content = await response.read()
                    content_type = response.headers.get('Content-Type', '')
                    response_headers = dict(response.headers)
                    return content, content_type, response.status, response_headers
                elif response.status in [403, 404, 500]:
                    return None, None, response.status, dict(response.headers)
        except asyncio.TimeoutError:
            if attempt == max_retries - 1:
                logger.warning(f"Timeout fetching {url}")
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
        except Exception as e:
            if attempt == max_retries - 1:
                logger.warning(f"Error fetching {url}: {e}")
            await asyncio.sleep(2 ** attempt)
    
    return None, None, 0, {}

def extract_assets_from_css(css_content, base_url):
    """Extract URLs from CSS content"""
    urls = []
    
    # Find url() patterns
    url_patterns = re.findall(r'url\([\'"]?(.*?)[\'"]?\)', css_content)
    for url in url_patterns:
        if not url.startswith(('data:', '#')):
            full_url = urljoin(base_url, url)
            urls.append(full_url)
    
    # Find @import statements
    import_patterns = re.findall(r'@import\s+[\'"]?(.*?)[\'"]?;', css_content)
    for url in import_patterns:
        if url.startswith(('http://', 'https://', '//')):
            urls.append(url if url.startswith('http') else f'https:{url}')
        else:
            urls.append(urljoin(base_url, url))
    
    return urls

def sanitize_filename(filename):
    """Sanitize filename to remove invalid characters"""
    if not filename:
        return "unnamed_file"
    
    # Extract filename from URL
    filename = unquote(filename.split("?")[0].split("#")[0])
    filename = os.path.basename(filename)
    
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    filename = re.sub(r'\s+', '_', filename)
    filename = filename.strip('._')
    
    # Truncate if too long
    if len(filename) > 150:
        name, ext = os.path.splitext(filename)
        filename = name[:100] + "_" + hashlib.md5(name.encode()).hexdigest()[:8] + ext
    
    return filename or "unnamed_file"

def format_size(bytes_size):
    """Format file size in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"

def create_progress_bar(percentage, length=20):
    """Create a progress bar"""
    filled = int(length * percentage / 100)
    bar = "█" * filled + "░" * (length - filled)
    return f"[{bar}] {percentage:.1f}%"

# ==================== ENHANCED WEB SCRAPING FUNCTIONS ====================
async def check_scrapable(url):
    """Check if URL is scrapable with enhanced detection"""
    try:
        async with aiohttp.ClientSession() as session:
            content, content_type, status, headers = await fetch_with_retry(session, url, max_retries=2)
            if status != 200:
                return False, f"HTTP {status}", None, None
            
            soup = BeautifulSoup(content, 'html.parser') if content else None
            
            # Detect backend technology
            detected_techs = detect_backend_technology(url, soup, content.decode('utf-8', errors='ignore') if content else '', headers)
            
            return True, "OK", detected_techs, soup
    except Exception as e:
        return False, str(e), None, None

def analyze_website_structure(soup, base_url):
    """Analyze website structure and return metadata"""
    metadata = {
        'title': soup.title.string if soup.title else 'No Title',
        'description': '',
        'keywords': [],
        'language': 'en',
        'viewport': '',
        'forms': len(soup.find_all('form')),
        'links': len(soup.find_all('a')),
        'images': len(soup.find_all('img')),
        'scripts': len(soup.find_all('script')),
        'stylesheets': len(soup.find_all('link', rel='stylesheet')),
        'meta_tags': {},
        'api_endpoints': [],
        'backend_files': []
    }
    
    # Extract meta tags
    for meta in soup.find_all('meta'):
        name = meta.get('name') or meta.get('property') or meta.get('http-equiv')
        content = meta.get('content', '')
        if name:
            metadata['meta_tags'][name] = content
    
    # Extract description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc:
        metadata['description'] = meta_desc.get('content', '')
    
    meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
    if meta_keywords:
        metadata['keywords'] = [k.strip() for k in meta_keywords.get('content', '').split(',')]
    
    meta_lang = soup.find('html')
    if meta_lang and meta_lang.get('lang'):
        metadata['language'] = meta_lang.get('lang')
    
    meta_viewport = soup.find('meta', attrs={'name': 'viewport'})
    if meta_viewport:
        metadata['viewport'] = meta_viewport.get('content', '')
    
    # Extract potential API endpoints
    for script in soup.find_all('script'):
        if script.string:
            # Look for API URLs in JavaScript
            api_patterns = [
                r'fetch\([\'"]([^\'"]+)[\'"]\)',
                r'axios\.(?:get|post|put|delete)\([\'"]([^\'"]+)[\'"]\)',
                r'\.ajax\([^)]*url:\s*[\'"]([^\'"]+)[\'"]',
                r'\/api\/[^\s"\']+',
                r'\/v[0-9]+\/[^\s"\']+',
            ]
            for pattern in api_patterns:
                matches = re.findall(pattern, script.string)
                for match in matches:
                    if match.startswith('/'):
                        full_url = urljoin(base_url, match)
                        metadata['api_endpoints'].append(full_url)
    
    return metadata

# ==================== MAIN SCRAPING FUNCTION WITH BACKEND DETECTION ====================
async def scrape_website_with_backend_detection(url, chat_id, user_info):
    """Advanced website scraping with automatic backend detection"""
    start_time = time.time()
    status_msg = None
    scrap_id = hashlib.md5(f"{url}{chat_id}{start_time}".encode()).hexdigest()[:10]
    
    try:
        # Step 1: Check if URL is scrapable and detect technology
        status_msg = bot.send_message(
            chat_id, 
            format_text(f"🔍 Analyzing website structure...\n📝 Scrap ID: {scrap_id}"),
            parse_mode=None
        )
        
        is_scrapable, reason, detected_techs, soup = await check_scrapable(url)
        if not is_scrapable:
            bot.edit_message_text(
                format_text(f"❌ Cannot scrape this URL\n⚠️ Reason: {reason}"),
                chat_id,
                status_msg.message_id,
                parse_mode=None
            )
            notify_owner_about_scrape(
                user_info, url, {}, 
                success=False, 
                error_msg=f"Not scrapable: {reason}"
            )
            return
        
        # Show detected technologies
        tech_message = ", ".join(detected_techs) if detected_techs else "Frontend only"
        bot.edit_message_text(
            format_text(f"✅ Website accessible\n🛠️ Detected: {tech_message}\n🔄 Starting comprehensive scan..."),
            chat_id,
            status_msg.message_id,
            parse_mode=None
        )
        
        # Step 2: Prepare directories
        parsed = urlparse(url)
        domain = re.sub(r'[^\w\-]', '_', parsed.netloc.replace('www.', ''))
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_folder = os.path.join(BASE_DIR, f"{domain}_{timestamp}_{scrap_id}")
        
        clean_directory(base_folder)
        os.makedirs(base_folder, exist_ok=True)
        
        # Step 3: Create scraper session for backend detection
        async with aiohttp.ClientSession() as session:
            # Step 4: Fetch main page with headers
            bot.edit_message_text(
                format_text("🌐 Fetching main page content..."),
                chat_id,
                status_msg.message_id,
                parse_mode=None
            )
            
            html_content, content_type, status, headers = await fetch_with_retry(session, url)
            
            if not html_content:
                bot.edit_message_text(
                    format_text(f"❌ Failed to fetch main page\n⚠️ HTTP Status: {status}"),
                    chat_id,
                    status_msg.message_id,
                    parse_mode=None
                )
                notify_owner_about_scrape(
                    user_info, url, {}, 
                    success=False, 
                    error_msg=f"HTTP {status}"
                )
                return
            
            # Parse HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Analyze website structure
            metadata = analyze_website_structure(soup, url)
            metadata['backend_technologies'] = detected_techs
            metadata['response_headers'] = {k: str(v) for k, v in headers.items()}
            
            # Step 5: Search for backend files
            bot.edit_message_text(
                format_text(f"🔍 Searching for backend files...\n🛠️ Technologies: {tech_message}"),
                chat_id,
                status_msg.message_id,
                parse_mode=None
            )
            
            backend_files = await find_backend_files(url, session)
            metadata['backend_files_found'] = backend_files
            
            # Step 6: Extract assets from HTML
            bot.edit_message_text(
                format_text("📦 Extracting assets and links..."),
                chat_id,
                status_msg.message_id,
                parse_mode=None
            )
            
            assets = set()
            backend_assets = set()
            asset_types = {}
            
            # Find assets in HTML
            tags_to_check = [
                ('script', 'src'),
                ('link', 'href'),
                ('img', 'src'),
                ('source', 'src'),
                ('video', 'src'),
                ('audio', 'src'),
                ('iframe', 'src'),
                ('embed', 'src'),
                ('object', 'data'),
                ('a', 'href'),
                ('form', 'action'),
                ('button', 'formaction'),
                ('input', 'src'),
                ('track', 'src'),
                ('area', 'href'),
                ('base', 'href'),
                ('meta', 'content')
            ]
            
            for tag, attr in tags_to_check:
                for elem in soup.find_all(tag):
                    link = elem.get(attr)
                    if link and not link.startswith(('data:', 'javascript:', 'mailto:', 'tel:', '#')):
                        full_url = urljoin(url, link.strip())
                        if full_url.startswith('//'):
                            full_url = 'https:' + full_url if url.startswith('https') else 'http:' + full_url
                        
                        ext = os.path.splitext(full_url.split("?")[0])[-1].lower()
                        
                        # Check if it's a backend file
                        is_backend = False
                        for tech, patterns in BACKEND_PATTERNS.items():
                            for pattern in patterns:
                                if pattern in full_url:
                                    is_backend = True
                                    backend_assets.add(full_url)
                                    break
                            if is_backend:
                                break
                        
                        if ext in FOLDERS or tag in ['img', 'script', 'link'] or is_backend:
                            if is_backend:
                                backend_assets.add(full_url)
                            else:
                                assets.add(full_url)
                            
                            asset_types.setdefault(ext, 0)
                            asset_types[ext] += 1
            
            # Find inline CSS and extract URLs
            for style in soup.find_all('style'):
                if style.string:
                    css_urls = extract_assets_from_css(style.string, url)
                    assets.update(css_urls)
            
            # Find CSS files and extract their assets
            css_links = soup.find_all('link', rel='stylesheet')
            css_contents = []
            
            for css_link in css_links[:5]:  # Limit to 5 CSS files
                css_url = css_link.get('href')
                if css_url:
                    full_css_url = urljoin(url, css_url)
                    css_content, _, _, _ = await fetch_with_retry(session, full_css_url)
                    if css_content:
                        try:
                            css_text = css_content.decode('utf-8', errors='ignore')
                            css_urls = extract_assets_from_css(css_text, full_css_url)
                            assets.update(css_urls)
                            css_contents.append(css_text)
                        except:
                            pass
            
            # Combine all assets
            all_assets = list(assets) + list(backend_assets)
            all_assets = all_assets[:MAX_ASSETS]  # Limit number of assets
            
            # Step 7: Download assets with progress
            bot.edit_message_text(
                format_text(f"📥 Downloading {len(all_assets)} assets...\n{create_progress_bar(0)}"),
                chat_id,
                status_msg.message_id,
                parse_mode=None
            )
            
            downloaded_files = []
            failed_assets = []
            downloaded_count = 0
            backend_downloaded = 0
            total_size = 0
            
            semaphore = asyncio.Semaphore(CONCURRENT_DOWNLOADS)
            
            async def download_asset(asset_url, idx):
                async with semaphore:
                    try:
                        content, _, status, _ = await fetch_with_retry(session, asset_url)
                        if content and len(content) < MAX_FILE_SIZE:
                            ext = os.path.splitext(asset_url.split("?")[0])[-1].lower()
                            folder_name = FOLDERS.get(ext, 'unknown')
                            
                            # Check if it's a backend file
                            is_backend = asset_url in backend_assets
                            if is_backend:
                                folder_name = 'backend/detected'
                            
                            filename = sanitize_filename(os.path.basename(asset_url))
                            
                            if not filename or filename == 'unnamed_file':
                                filename = f"asset_{idx}_{get_file_hash(content)}.{ext[1:] if ext else 'bin'}"
                            
                            return {
                                'url': asset_url,
                                'content': content,
                                'filename': filename,
                                'folder': folder_name,
                                'extension': ext,
                                'size': len(content),
                                'is_backend': is_backend,
                                'success': True
                            }
                    except Exception as e:
                        logger.error(f"Error downloading {asset_url}: {e}")
                    
                    return {
                        'url': asset_url,
                        'success': False
                    }
            
            # Create download tasks
            tasks = [download_asset(url, idx) for idx, url in enumerate(all_assets)]
            
            # Process downloads with progress updates
            for idx, task in enumerate(asyncio.as_completed(tasks)):
                result = await task
                
                if result['success']:
                    downloaded_count += 1
                    total_size += result['size']
                    
                    if result['is_backend']:
                        backend_downloaded += 1
                    
                    folder_name = result['folder']
                    filename = result['filename']
                    content = result['content']
                    
                    # Save file
                    folder_path = os.path.join(base_folder, folder_name)
                    os.makedirs(folder_path, exist_ok=True)
                    file_path = os.path.join(folder_path, filename)
                    
                    try:
                        if result['extension'] in ['.js', '.css', '.html', '.htm', '.php', '.txt', '.json', '.xml', '.py', '.rb']:
                            try:
                                text = content.decode('utf-8', errors='ignore')
                                with open(file_path, 'w', encoding='utf-8') as f:
                                    f.write(text)
                            except:
                                with open(file_path, 'wb') as f:
                                    f.write(content)
                        else:
                            with open(file_path, 'wb') as f:
                                f.write(content)
                        
                        downloaded_files.append({
                            'path': file_path,
                            'size': result['size'],
                            'folder': folder_name,
                            'is_backend': result['is_backend']
                        })
                    except Exception as e:
                        logger.error(f"Error saving file {filename}: {e}")
                        failed_assets.append(result['url'])
                else:
                    failed_assets.append(result['url'])
                
                # Update progress every 10 downloads or when done
                if idx % 10 == 0 or idx == len(all_assets) - 1:
                    progress = (idx + 1) * 100 // len(all_assets)
                    bot.edit_message_text(
                        format_text(f"📥 Downloading {len(all_assets)} assets...\n"
                                   f"{create_progress_bar(progress)}\n"
                                   f"✅ Downloaded: {downloaded_count}/{len(all_assets)}\n"
                                   f"🔧 Backend files: {backend_downloaded}"),
                        chat_id,
                        status_msg.message_id,
                        parse_mode=None
                    )
            
            # Step 8: Save main HTML
            html_folder = os.path.join(base_folder, 'html_files')
            os.makedirs(html_folder, exist_ok=True)
            
            html_text = html_content.decode('utf-8', errors='ignore')
            index_path = os.path.join(html_folder, 'index.html')
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(html_text)
            
            # Step 9: Create comprehensive metadata file
            metadata['scrap_id'] = scrap_id
            metadata['url'] = url
            metadata['timestamp'] = timestamp
            metadata['domain'] = domain
            metadata['total_assets_found'] = len(all_assets)
            metadata['assets_downloaded'] = downloaded_count
            metadata['backend_files_downloaded'] = backend_downloaded
            metadata['assets_failed'] = len(failed_assets)
            metadata['asset_types'] = asset_types
            metadata['total_size'] = total_size
            
            # Add vulnerability analysis
            vulnerabilities = []
            for backend_file in backend_files:
                vulnerabilities.extend(backend_file.get('vulnerabilities', []))
            metadata['vulnerabilities_found'] = list(set(vulnerabilities))
            
            metadata_path = os.path.join(base_folder, 'comprehensive_analysis.json')
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            # Save backend files report separately
            backend_report_path = os.path.join(base_folder, 'backend_analysis.json')
            with open(backend_report_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'backend_files': backend_files,
                    'detected_technologies': detected_techs,
                    'vulnerability_summary': {
                        'total_vulnerabilities': len(vulnerabilities),
                        'vulnerability_types': list(set(vulnerabilities)),
                        'high_risk_files': [f for f in backend_files if len(f.get('vulnerabilities', [])) > 0]
                    }
                }, f, indent=2, ensure_ascii=False)
            
            # Save failed assets list
            if failed_assets:
                failed_path = os.path.join(base_folder, 'failed_assets.txt')
                with open(failed_path, 'w', encoding='utf-8') as f:
                    for asset in failed_assets:
                        f.write(f"{asset}\n")
            
            # Step 10: Create ZIP file
            bot.edit_message_text(
                format_text("📦 Creating ZIP archive..."),
                chat_id,
                status_msg.message_id,
                parse_mode=None
            )
            
            zip_filename = f"Advanced_Scrape_{domain}_{timestamp}.zip"
            zip_path = os.path.join(BASE_DIR, zip_filename)
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(base_folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, base_folder)
                        zipf.write(file_path, arcname)
            
            # Step 11: Calculate statistics
            time_taken = time.time() - start_time
            
            stats = {
                'total_files': len(downloaded_files) + 1,  # +1 for index.html
                'total_size': total_size,
                'time_taken': time_taken,
                'domain': domain,
                'scrap_id': scrap_id,
                'backend_technologies': detected_techs,
                'backend_files_found': len(backend_files),
                'vulnerabilities_found': len(vulnerabilities),
                'metadata': metadata
            }
            
            # Step 12: Send to user with detailed report
            bot.edit_message_text(
                format_text("📤 Preparing final package..."),
                chat_id,
                status_msg.message_id,
                parse_mode=None
            )
            
            # Prepare detailed message
            if vulnerabilities:
                vuln_text = f"⚠️ Vulnerabilities: {len(vulnerabilities)} found\n"
            else:
                vuln_text = "✅ No vulnerabilities detected\n"
            
            report_message = format_text(f"""
🎉 Website Scraping Complete!

📋 Summary:
🔗 URL: {url[:50]}...
📁 Domain: {domain}
🆔 Scrap ID: {scrap_id}
🕐 Time Taken: {time_taken:.1f}s

🛠️ Technology Analysis:
{', '.join(detected_techs) if detected_techs else 'Frontend only'}

📊 Download Statistics:
📦 Total Files: {len(downloaded_files) + 1}
💾 Total Size: {format_size(total_size)}
✅ Successfully downloaded: {downloaded_count}/{len(all_assets)}
🔧 Backend files: {backend_downloaded}
❌ Failed: {len(failed_assets)}

🔍 Security Analysis:
🛡️ Backend endpoints scanned: {len(backend_files)}
{vuln_text}
📁 Sensitive files found: {len([f for f in backend_files if f['status'] in [200, 403, 401]])}

📈 Website Structure:
📄 HTML Pages: 1 (main page)
🖼️ Images: {metadata['images']}
📜 Scripts: {metadata['scripts']}
🎨 Stylesheets: {metadata['stylesheets']}
🔗 Links: {metadata['links']}
📝 Forms: {metadata['forms']}
🔌 API Endpoints: {len(metadata['api_endpoints'])}
""")
            
            # Send ZIP file
            markup = InlineKeyboardMarkup()
            markup.row(
                InlineKeyboardButton("📊 View Analysis", callback_data=f"analysis_{scrap_id}"),
                InlineKeyboardButton("🔧 Backend Report", callback_data=f"backend_{scrap_id}")
            )
            markup.row(
                InlineKeyboardButton("👨‍💻 Developer", url=f"https://t.me/{OWNER_USERNAME[1:] if OWNER_USERNAME.startswith('@') else OWNER_USERNAME}"),
                InlineKeyboardButton("⭐ Rate Bot", callback_data="rate_bot")
            )
            
            try:
                with open(zip_path, 'rb') as f:
                    bot.send_document(
                        chat_id,
                        f,
                        caption=report_message,
                        reply_markup=markup,
                        timeout=300,
                        parse_mode=None,
                        visible_file_name=zip_filename
                    )
                
                # Delete status message
                bot.delete_message(chat_id, status_msg.message_id)
                
                # Update user stats
                update_user_in_db(user_info['id'], user_info.get('username', 'unknown'), user_info.get('first_name', ''))
                increment_user_scrapes(user_info['id'])
                
                # Save session data
                session_data = {
                    'session_id': scrap_id,
                    'user_id': user_info['id'],
                    'url': url,
                    'start_time': datetime.fromtimestamp(start_time).isoformat(),
                    'end_time': datetime.now().isoformat(),
                    'total_files': len(downloaded_files) + 1,
                    'total_size': total_size,
                    'status': 'completed',
                    'backend_detected': ', '.join(detected_techs) if detected_techs else ''
                }
                save_scraping_session(session_data)
                
                # Notify owner
                notify_owner_about_scrape(user_info, url, stats, success=True)
                
            except Exception as e:
                logger.error(f"Error sending ZIP: {e}")
                bot.edit_message_text(
                    format_text(f"❌ Error sending file: {str(e)[:100]}"),
                    chat_id,
                    status_msg.message_id,
                    parse_mode=None
                )
            
            # Cleanup
            try:
                os.remove(zip_path)
                clean_directory(base_folder)
            except Exception as e:
                logger.error(f"Cleanup error: {e}")
    
    except Exception as e:
        logger.error(f"Error in scrape_website_with_backend_detection: {e}")
        if status_msg:
            bot.edit_message_text(
                format_text(f"❌ Scraping failed: {str(e)[:200]}"),
                chat_id,
                status_msg.message_id,
                parse_mode=None
            )
        
        notify_owner_about_scrape(
            user_info, url, {}, 
            success=False, 
            error_msg=str(e)[:200]
        )

def get_file_hash(content):
    """Generate hash for file content"""
    return hashlib.md5(content).hexdigest()[:12]

def clean_directory(path):
    """Remove directory and all contents"""
    try:
        if os.path.exists(path):
            shutil.rmtree(path)
    except Exception as e:
        logger.error(f"Error cleaning directory {path}: {e}")

# ==================== TELEGRAM BOT HANDLERS ====================
@bot.callback_query_handler(func=lambda call: call.data.startswith("analysis_"))
def handle_analysis_view(call):
    """Handle analysis viewing"""
    try:
        scrap_id = call.data.split("_")[1]
        
        # In a real implementation, you would load the analysis from file/database
        # For now, we'll send a placeholder message
        
        analysis_text = format_text(f"""
📊 Analysis Report - Session {scrap_id}

Detailed analysis includes:
• Website structure mapping
• Technology stack identification
• Asset inventory
• Security vulnerability scan
• Backend file discovery
• API endpoint detection

The full analysis is available in the downloaded ZIP file.
""")
        
        bot.send_message(call.message.chat.id, analysis_text, parse_mode=None)
        bot.answer_callback_query(call.id, "📊 Analysis loaded")
    except Exception as e:
        bot.answer_callback_query(call.id, f"❌ Error: {str(e)[:50]}", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data.startswith("backend_"))
def handle_backend_report(call):
    """Handle backend report viewing"""
    try:
        scrap_id = call.data.split("_")[1]
        
        backend_text = format_text(f"""
🔧 Backend Report - Session {scrap_id}

This report contains:
• Detected backend technologies
• Found backend files
• Vulnerability analysis
• Security recommendations
• Configuration file discovery

The complete backend report is in the 'backend_analysis.json' file within the downloaded ZIP.
""")
        
        bot.send_message(call.message.chat.id, backend_text, parse_mode=None)
        bot.answer_callback_query(call.id, "🔧 Backend report loaded")
    except Exception as e:
        bot.answer_callback_query(call.id, f"❌ Error: {str(e)[:50]}", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "verify_membership")
def handle_verification(call):
    """Handle membership verification"""
   
            
            welcome_msg = format_text(f"""
✨ Welcome to UnknownGuy Advanced Web Scraper! ✨

I can automatically detect and scrape:
• Frontend assets (HTML, CSS, JavaScript, Images)
• Backend files (PHP, Python, Node.js, Config files)
• API endpoints and sensitive directories
• Security vulnerabilities and misconfigurations

📝 Simply send me any website URL starting with http:// or https://

🛠️ I will automatically:
1. Detect backend technologies
2. Scan for vulnerabilities
3. Download all assets
4. Provide comprehensive analysis

⚠️ Note: Only scrape websites you have permission to access.
""")
            
            bot.send_message(call.message.chat.id, welcome_msg, parse_mode=None)
            
  

# ==================== EXISTING FUNCTIONS (keep from original) ====================


def send_welcome_image(chat_id):
    """Send welcome message with image"""
    caption = format_text("""
✨ Welcome to UnknownGuy Advanced Web Scraper! ✨

🔹 You must join our channels to use this bot
🔹 After joining, click Verify button below
🔹 Then send me any website URL to scrape

🛠️ Advanced Features:
• Automatic backend detection
• Vulnerability scanning
• Comprehensive asset downloading
• Security analysis
""")
    try:
        bot.send_photo(
            chat_id,
            photo=WELCOME_IMAGE_URL,
            caption=caption,
            reply_markup=create_verification_buttons(),
            parse_mode=None
        )
    except Exception as e:
        logger.error(f"Error sending welcome image: {e}")
        bot.send_message(chat_id, caption, reply_markup=create_verification_buttons())



def notify_owner_about_scrape(user_info, url, stats, success=True, error_msg=""):
    """Send notification to owner about scraping activity"""
    try:
        user_id = user_info.get('id', 'Unknown')
        username = user_info.get('username', 'Unknown')
        first_name = user_info.get('first_name', 'User')
        
        if success:
            message = format_text(f"""
🚀 New Website Scraped by User!

👤 User: {first_name} (@{username})
🆔 ID: {user_id}
🔗 URL: {url}

📊 Scraping Results:
📁 Total Files: {stats.get('total_files', 0)}
📦 Total Size: {format_size(stats.get('total_size', 0))}
⏱️ Time Taken: {stats.get('time_taken', 0):.1f}s
🛠️ Backend Tech: {', '.join(stats.get('backend_technologies', ['None']))}
⚠️ Vulnerabilities: {stats.get('vulnerabilities_found', 0)}
✅ Status: Successful
📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
""")
        else:
            message = format_text(f"""
❌ Failed Scraping Attempt

👤 User: {first_name} (@{username})
🆔 ID: {user_id}
🔗 URL: {url}

⚠️ Error: {error_msg[:200]}
📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
""")
        
        bot.send_message(OWNER_ID, message, parse_mode=None)
        
        # Also send to owner's username if different from ID
        if OWNER_USERNAME and OWNER_USERNAME != f"@{bot.get_chat(OWNER_ID).username}":
            try:
                bot.send_message(OWNER_USERNAME, message, parse_mode=None)
            except:
                pass
                
    except Exception as e:
        logger.error(f"Error notifying owner: {e}")

@bot.message_handler(commands=['start', 'help', 'about'])
def handle_start(message):
    """Handle start, help, and about commands"""

    
    if message.text.startswith('/help'):
        help_text = format_text("""
🆘 Help Guide:

📌 How to use:
1. Send me any website URL (must start with http:// or https://)
2. I'll automatically detect backend technologies
3. Scan for vulnerabilities and sensitive files
4. Download all assets (frontend and backend)
5. You'll receive a ZIP file with comprehensive analysis

🛠️ Advanced Features:
• Automatic backend technology detection
• Vulnerability scanning (SQLi, XSS, credentials, etc.)
• Backend file discovery (config files, admin panels, etc.)
• API endpoint extraction
• Directory enumeration
• Security analysis report

📁 Supported file types:
• HTML, CSS, JavaScript, PHP, Python, Ruby, Java
• Images (JPG, PNG, GIF, SVG, WebP)
• Fonts (WOFF, TTF, OTF, EOT)
• Media (MP4, MP3, WAV, PDF)
• Documents (DOC, XLS, PPT, TXT)
• Configuration files (.env, config, .yml, .json)

⚡ Commands:
/start - Start the bot
/help - Show this help
/about - About the bot
/stats - Your statistics
/admin - Admin panel (owner only)

⚠️ Important:
• Only scrape websites you have permission to access
• Large websites may take time
• Maximum 500 assets per scrape
• Respect robots.txt and website terms
""")
        bot.reply_to(message, help_text, parse_mode=None)
    
    elif message.text.startswith('/about'):
        about_text = format_text(f"""
🤖 About UnknownGuy Advanced Web Scraper

Developer: {OWNER_USERNAME}
Version: 4.0 (Backend Detection)
Created: 2024

🔧 Advanced Features:
• Automatic backend technology detection
• Comprehensive vulnerability scanning
• Backend file discovery and analysis
• API endpoint extraction
• Security assessment
• Smart asset organization

📞 Contact: {OWNER_USERNAME}
⭐ Rate: /rate

This bot is designed for:
• Web developers
• Security researchers
• Penetration testers (with permission)
• SEO specialists
• Content archivists

⚠️ Warning: Use responsibly and ethically.
Always respect website terms of service.
""")
        bot.reply_to(message, about_text, parse_mode=None)
    
    else:
        welcome_text = format_text(f"""
👋 Welcome {message.from_user.first_name}!

I'm Shaurya,s Advanced Web Scraper - the most powerful scraping tool.

🛠️ When you send me a website URL, I automatically:
1. 🔍 Detect backend technologies (PHP, Python, Node.js, etc.)
2. 🛡️ Scan for security vulnerabilities
3. 📁 Discover backend files and sensitive directories
4. 📥 Download ALL assets (frontend & backend)
5. 📊 Provide comprehensive analysis report

✨ Try me now! Send any website URL...
""")
        bot.reply_to(message, welcome_text, parse_mode=None)

@bot.message_handler(commands=['stats'])
def handle_stats(message):
    """Show user statistics"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (message.from_user.id,))
        user_data = cursor.fetchone()
        
        if user_data:
            user_id, username, first_name, join_date, last_active, total_scrapes, total_assets, total_size, banned = user_data
            
            # Get recent sessions
            cursor.execute('SELECT COUNT(*) FROM scraping_sessions WHERE user_id = ?', (user_id,))
            total_sessions = cursor.fetchone()[0]
            
            stats_text = format_text(f"""
📊 Your Statistics:

👤 User: @{username} ({first_name})
📅 Joined: {join_date[:10]}
🕒 Last Active: {last_active[:19]}
🚀 Total Scrapes: {total_scrapes}
📊 Total Sessions: {total_sessions}
📦 Total Assets Downloaded: {total_assets}
💾 Total Size Downloaded: {format_size(total_size)}
🔒 Account Status: {'✅ Active' if not banned else '❌ Banned'}
""")
        else:
            stats_text = format_text("📊 No statistics yet. Start by scraping a website!")
        
        conn.close()
        bot.reply_to(message, stats_text, parse_mode=None)
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        bot.reply_to(message, format_text("❌ Error loading statistics"), parse_mode=None)

@bot.message_handler(func=lambda message: True)
def handle_url(message):
    """Handle website URL messages"""
    # Check membership

    
    url = message.text.strip()
    
    # Validate URL
    if not (url.startswith('http://') or url.startswith('https://')):
        bot.reply_to(message, format_text("❌ URL must start with http:// or https://"), parse_mode=None)
        return
    
    # Basic URL validation
    try:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            bot.reply_to(message, format_text("❌ Invalid URL format"), parse_mode=None)
            return
    except:
        bot.reply_to(message, format_text("❌ Invalid URL"), parse_mode=None)
        return
    
    # Inform user
    bot.reply_to(
        message,
        format_text(f"✅ Starting advanced scraping with backend detection...\n🔗 URL: {url[:50]}..."),
        parse_mode=None
    )
    
    # Prepare user info
    user_info = {
        'id': message.from_user.id,
        'username': message.from_user.username,
        'first_name': message.from_user.first_name
    }
    
    # Start scraping in background thread
    def run_scrape():
        asyncio.run(scrape_website_with_backend_detection(url, message.chat.id, user_info))
    
    thread = threading.Thread(target=run_scrape, daemon=True)
    thread.start()

# ==================== BOT STARTUP ====================
def init_system():
    """Initialize system directories and database"""
    # Create base directory
    os.makedirs(BASE_DIR, exist_ok=True)
    
    # Initialize database
    init_database()
    
    # Create subdirectories
    subdirs = ['sessions', 'reports', 'temp', 'backups']
    for subdir in subdirs:
        os.makedirs(os.path.join(BASE_DIR, subdir), exist_ok=True)
    
    logger.info("✅ System initialized successfully")

start_bot_time = time.time()

def run_bot():
    """Main bot runner"""
    logger.info("🚀 Advanced Web Scraper Bot Starting...")
    logger.info(f"👑 Owner: {OWNER_USERNAME} (ID: {OWNER_ID})")
    logger.info(f"📁 Base Directory: {BASE_DIR}")
    logger.info(f"💾 Database: {DB_FILE}")
    
    # Send startup notification
    try:
        bot.send_message(
            OWNER_ID,
            format_text(f"""
🤖 Advanced Web Scraper Started!
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
⚡ Version: 4.0 (Auto Backend Detection)
📊 Features:
• Automatic backend technology detection
• Vulnerability scanning
• Backend file discovery
• Security analysis
• Comprehensive asset downloading
"""),
            parse_mode=None
        )
    except Exception as e:
        logger.error(f"Startup notification error: {e}")
    
    # Main bot loop
    while True:
        try:
            logger.info("🔄 Bot is running...")
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except KeyboardInterrupt:
            logger.info("⏹️ Bot stopped by user")
            break
        except Exception as e:
            logger.error(f"❌ Bot error: {e}")
            time.sleep(10)

if __name__ == '__main__':
    # Initialize system
    init_system()
    
    # Set bot commands
    bot.set_my_commands([
        telebot.types.BotCommand("/start", "Start the bot"),
        telebot.types.BotCommand("/help", "Show help guide"),
        telebot.types.BotCommand("/stats", "Show your statistics"),
        telebot.types.BotCommand("/admin", "Admin panel (owner only)"),
    ])
    
    # Run the bot
    run_bot()
