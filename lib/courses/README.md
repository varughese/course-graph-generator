This is some hacky scraper code from a combination the PittAPI and major-master (both public Github repos). It is multithreaded which makes it slightly faster. 

The idea is, it scrapes per semester, and saves the data in `scraped/<termcode>/course_data.json`. To make sure it so it can pause and resume scraping, it writes to a "scraped" file.