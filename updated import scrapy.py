import scrapy

class LAUDataSpider(scrapy.Spider):
    name = 'LAU_data'
    start_urls = ['https://www.bls.gov/web/laus/lauhsthl.htm']

    def parse(self, response):
        self.logger.debug(response.text)  # print the page source to check if it's correct
        # Extract the state names from the "td" elements in the first row of the table
        for i, row in enumerate(response.xpath('//table[@class="regular"]//tr')):
            # Skip the first row since it contains the state names
            if i == 0:
                continue
            yield {
                'state': row.xpath('th[1]//text()').get(),
                'February 2023 rate': row.xpath('td[1]//text()').get(),
                'Historical High Date': row.xpath('td[2]//text()').get(),
                'Historical High Rate': row.xpath('td[3]//text()').get(),
                'Historical Low Date': row.xpath('td[4]//text()').get(),
                'Historical Low Rate': row.xpath('td[5]//text()').get(),
            }
            
            # Check if there is a website in the row and scrape it
            website_url = row.xpath('td[6]//a/@href').get()
            if website_url:
                yield scrapy.Request(response.urljoin(website_url), callback=self.parse_website)
        
        self.logger.info('Finished scraping')  # log when the spider is finished

    def parse_website(self, response):
        # Process the response from the additional website scraping
        # Extract the data you need from the response
        # You can use XPath or CSS selectors to extract specific elements
        
        # Example code: Extract the website title
        website_title = response.xpath('//title/text()').get()
        
        # Process the extracted data as needed
        # You can yield items or perform any other operations

        yield {
            'website_title': website_title,
            # Add more extracted data fields as necessary
        }
