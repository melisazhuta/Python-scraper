from classes.Scraper import Scraper

s = Scraper()

try:
    csv_file = s.get_input_csv_file()
    urls = s.get_urls_from_csv_file(csv_file)
    watches = s.scrape(urls)
    s.store_watches_to_json(watches)
except Exception as e:
    print(f'{e}')
