import time
from random import randint
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import shutil


def create_driver():
    """
    Ubuntu 서버 환경에서도 안정적으로 실행 가능한 Chrome 드라이버 생성 함수
    - headless 모드로 실행
    - sandbox / dev-shm 이슈 해결
    - 자동 경로 탐색 (chromedriver 위치)
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # GUI 없이 실행
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--lang=ko-KR")

    chromedriver_path = shutil.which("chromedriver") or "/usr/local/bin/chromedriver"
    service = Service(chromedriver_path)

    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except Exception as e:
        print(f"❌ Chrome 드라이버 실행 실패: {e}")
        raise


class QuoteScraper:
    def __init__(self, url):
        """명언 스크래핑용 드라이버 초기화"""
        print("🚀 명언 스크래핑 시작")
        self.driver = create_driver()

        randtime = randint(1, 3)
        time.sleep(randtime)
        self.driver.get(url)
        time.sleep(3)

        self.quote_list = []

    def scrape_page(self):
        """단일 페이지에서 quote / author 추출"""
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        items = soup.select(".quote-item")

        for item in items:
            try:
                quote_text = item.select_one("p.quote")
                author_text = item.select_one("p.author")
                if quote_text and author_text:
                    quote = quote_text.get_text(strip=True)
                    author = author_text.get_text(strip=True)
                    self.quote_list.append({"quote": quote, "author": author})
            except Exception as e:
                print(f"추출 오류: {e}")

    def close(self):
        self.driver.quit()


class SelfReflectScraper:
    def __init__(self, url):
        """질문(자기반성) 스크래핑용 드라이버 초기화"""
        print("🚀 자기반성 질문 스크래핑 시작")
        self.driver = create_driver()

        randtime = randint(1, 3)
        time.sleep(randtime)
        self.driver.get(url)
        time.sleep(3)

        self.reflect_list = []

    def scrape_page(self):
        """단일 페이지에서 질문 추출"""
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        items = soup.select(".question")

        for item in items:
            try:
                reflect = item.get_text(strip=True)
                if reflect:
                    self.reflect_list.append(reflect)
            except Exception as e:
                print(f"추출 오류: {e}")

    def close(self):
        self.driver.quit()
