from funct.blogscrap_modify import QuoteScraper, SelfReflectScraper
from funct.dbinsert import DatabaseManager, get_db_config

if __name__ == "__main__":

    # db 설정 + 연결 진행
    print("DB setting")
    DB_CONFIG = get_db_config()
    db = DatabaseManager(**DB_CONFIG)

    try:
        db.connect()
        db.create_tables()

        # 명언 스크래핑 실행
        print("명언 스크래핑 실행")
        quote_url = "https://velog.io/@silverew/scrap-purpose-quote-use"
        quote_scraper = None

        try:
            quote_scraper = QuoteScraper(quote_url)
            quote_scraper.scrape_page()

            # 결과 확인용
            print(quote_scraper.quote_list[:10])
            if quote_scraper.quote_list:
                print(f"TEST: {len(quote_scraper.quote_list)} 개 수집 완료")
                db.insert_quotes(quote_scraper.quote_list)

            else:
                print("No Quotes Collected")
        except Exception as e:
            print(f"ERROR on Quotes Scraping: {e}")

        finally:
            if quote_scraper:
                quote_scraper.close()

        # 질문 스크래핑
        print("\n질문 스크래핑 실행")
        question_url = "https://velog.io/@silverew/scrap-purpose-selfreflect-use"
        reflect_scraper = None

        try:
            # url을 초기화 시점에 전달(마찬가지)
            reflect_scraper = SelfReflectScraper(question_url)
            reflect_scraper.scrape_page()
            print(reflect_scraper.reflect_list[:5])
            if reflect_scraper.reflect_list:
                print(f"SAMPLE: {len(reflect_scraper.reflect_list)}")
                db.insert_questions(reflect_scraper.reflect_list)
            else:
                print("No Reflect Collected")

        except Exception as e:
            print(f"Error on Question Scraping: {e}")

        finally:
            if reflect_scraper:
                reflect_scraper.close()

    except Exception as e:
        print(f"ERROR on Entire Process/Structure: {e}")

    finally:
        db.close()

    print("\n작업 종료")
