# def scrape_01():
#     url = "https://quotelibrary.org/quotes"
#     # url = "https://quotes.toscrape.com/"
#     option_ = Options()
#     option_.add_experimental_option("detach", True)
#
#     driver = webdriver.Chrome(options=option_)
#     driver.get(url)
#     randtime = randint(1, 10)
#     time.sleep(randtime)
#
#     # 이건 클릭하는 기능
#     driver.find_element(
#         By.CSS_SELECTOR,
#         ".px-2 py-1 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed",
#     ).click()  # 클릭으로 넘어가기sd
