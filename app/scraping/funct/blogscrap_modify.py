import time
from random import randint

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class QuoteScraper:
    def __init__(self, url):
        """드라이버 초기화
        detach = False: 크롤링 종료 후 브라우저 창을 닫음(True일 시 열어둠)
        quote_list: 수집한 인용문을 저장
        """
        self.option_ = Options()
        self.option_.add_experimental_option("detach", False)
        self.driver = webdriver.Chrome(options=self.option_)
        randtime = randint(1, 3)
        time.sleep(randtime)
        self.driver.get(url)

        # velog: React 기반. 콘텐츠 로딩 대기.
        time.sleep(3)

        self.quote_list = []

    def scrape_page(self):
        """
        단일 페이지의 HTML을 파싱해서 quote 추출
        Args:
            html(str): 페이지의 html 소스 코드
        BeautifulSoup으로 html 파싱
        .quote 클래스를 가진 모든 요소 선택
        """
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        items = soup.select(".quote-item")

        for item in items:
            try:
                quote_text = item.select_one("p.quote")
                author_text = item.select_one("p.author")
                """
                얘네가 존재한다면 이라는 if문
                quote, author 변수에 text로 받고(공백제거:strip)
                딕셔너리 형태로 받기
                """
                if quote_text and author_text:
                    quote = quote_text.get_text(strip=True)
                    author = author_text.get_text(strip=True)
                    self.quote_list.append(
                        {"quote": quote, "author": author}
                    )  # 리스트에 인용문 추가
            except Exception as e:
                print(f"추출 오류: {e}")

    def close(self):
        # 드라이버 종료
        self.driver.quit()


class SelfReflectScraper:
    def __init__(self, url):
        """드라이버 초기화
        detach = False: 크롤링 종료 후 브라우저 창을 닫음(True일 시 열어둠)
        quote_list: 수집한 인용문을 저장
        """
        self.option_ = Options()
        self.option_.add_experimental_option("detach", False)
        self.driver = webdriver.Chrome(options=self.option_)
        randtime = randint(1, 3)
        time.sleep(randtime)
        self.driver.get(url)

        # velog: React 기반. 콘텐츠 로딩 대기.
        time.sleep(3)

        self.reflect_list = []

    def scrape_page(self):
        """
        단일 페이지의 HTML을 파싱해서 quote 추출
        Args:
            html(str): 페이지의 html 소스 코드
        BeautifulSoup으로 html 파싱
        .quote 클래스를 가진 모든 요소 선택
        """
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
        # 드라이버 종료
        self.driver.quit()
