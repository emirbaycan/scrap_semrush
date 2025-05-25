# SEMrush Keyword & Organic Pages Scraper (Python + Selenium)

## Purpose
This repository provides Python scripts for automating the extraction of keyword data and organic pages from **SEMrush** using Selenium WebDriver.  
The tools are ideal for automating keyword research, SEO analysis, and tracking competitor performance at scale.

## Disclaimer
- **SEMrush is a paid, login-required service. These scripts require a valid account and exported session cookies to function.**
- Intended for **academic, research, and personal analytics** only.
- Excessive automated requests may violate SEMrush’s Terms of Service.
- **Use responsibly and always comply with relevant laws and site terms!**

## Requirements
- Python 3.x
- Selenium (`pip install selenium`)
- Google Chrome and ChromeDriver (or a compatible browser/driver)
- A `cookies.json` file exported from a logged-in SEMrush session
- (Note) XPath selectors in the code may require updates if SEMrush’s UI changes

## Usage

### 1. Keyword Analysis Script
- The script visits SEMrush’s "Keyword Overview" and "Keyword Magic" pages for your target keyword.
- Extracts keywords and saves them to a `.txt` file.
- By default, the script limits itself to 50 pages (adjustable via `page_count`).
- **Before running:**
  - Log in to SEMrush in your browser, export your session cookies as `cookies.json`.
  - Edit the `keyword = "..."` line as needed.

### 2. Organic Pages & Keywords Script
- The script visits SEMrush’s organic pages analysis for a given domain.
- For each discovered page, it collects top keywords and SERP analysis data.
- Results are saved line-by-line in `datas.txt` as JSON.
- **Before running:**
  - Log in and export cookies as above.

### Cookie Usage
- The scripts load `cookies.json`, convert it to a pickle (`cookies.pkl`), and inject all cookies into the Selenium browser.
- The code strips any `expiry` field to avoid Selenium errors.

## Limitations & Notes
- The XPath selectors are based on SEMrush’s current UI. If SEMrush updates their UI, XPath values may need to be changed.
- SEMrush may block or throttle excessive automated activity; use at a reasonable pace.
- `time.sleep()` and `WebDriverWait` are used for timing; adjust if you encounter issues or slow loading.
- Never share your `cookies.json` file—it grants access to your SEMrush account!

## Example Run
```bash
python semrush_keyword_scraper.py
python semrush_organic_pages_scraper.py
