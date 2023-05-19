import scrapy
import csv
import datetime
class GenericTableSpider(scrapy.Spider):
    name = 'generic_table'

    def start_requests(self):
        url = input("Enter website URL: ")
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        self.logger.debug(response.text)  # print the page source to check if it's correct

        # Extract the header names from the first row of the table
        headers = []
        for header in response.xpath('//table[@class="regular"]//tr'):
            headers.append(header.xpath('th[1]//text()').get())

        # Loop through each row of the table
        for i, row in enumerate(response.xpath('//table[@class="regular"]//tr')):
            # Skip the header row
            if i == 0:
                continue

            # Extract the data from each column of the row
            data = {}
            for j, cell in enumerate(row.xpath('td')):
                data[headers[j]] = cell.xpath('.//text()').get()

            yield data

        self.logger.info('Finished scraping')

        # Write the data to a CSV file
        date_time = datetime.datetime.now()
        filename = 'table_data'+str(date_time)+'.csv'
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            for data in response.xpath('//table[@class="regular"]//tr[position()>1]'):
                writer.writerow({headers[j]: cell.xpath('.//text()').get() for j, cell in enumerate(data.xpath('td'))})
        self.logger.info('Saved data to {}'.format(filename))
