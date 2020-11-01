"""
AUTHOR: ENRICO PERSICO, 2020

HOW TO RUN SPIDER:
INSTALL PYTHON
GO TO TERMINAL
RUN COMMAND 'pip install pandas'
RUN COMMAND 'pip install scrapy'
ENTER YOUR USER AGENT IN user_agent VARIABLE, IF YOU DON'T KNOW IT SEE 'https://www.whatismybrowser.com/detect/what-is-my-user-agent'   
SWITCH TO 'linkFinder' FOLDER IN TERMINAL
RUN COMMAND "scrapy crawl prospectProfiles -o output/unfiltered_output.csv"
DOING THIS WILL PRODUCE A CSV CALLED "output.csv" IN THE OUTPUT FOLDER WITH A LIST OF NAMES AND LINKS
COPY "output.csv" TO 'profileScraper' FOLDER FOR NEXT STEP

"""
import scrapy
import pandas

user_agent = "USER AGENT"
file_list = [
    "user_information/all_fields.csv", 
    "user_information/name_and_affiliation.csv", 
    "user_information/name_and_country.csv", 
    "user_information/name.csv"
]

class ProspectprofilesSpider(scrapy.Spider):
    # mandatory values
    name = 'prospectProfiles'
    allowed_domains = ['www.bing.com/']
    # initial generator that yields requests; and when they're fulfilled, the response will be parsed by the parse generator below
    def start_requests(self):
        # generator that yields requests according to its file name parameter
        def yield_link_for_file(file_name: str):
            # read encoded csv into parsable pandas data
            data = pandas.read_csv(file_name, encoding='latin')
            # turns pandas data into list containing name, affiliation, and country of origin according to file name
            name_list = list(data.name)
            if file_name == file_list[0]:
                affiliation_list = list(data.affiliation)
                country_list = list(data.country)
            elif file_name == file_list[1]:
                affiliation_list = list(data.affiliation)
            elif file_name == file_list[2]:
                country_list = list(data.country)

            for i in range(len(name_list)):
                # creates search_input based according to its file name
                if file_name == file_list[0]:
                    search_input = str(name_list[i]) + ' ' + str(affiliation_list[i]) + ' ' + str(country_list[i])
                elif file_name == file_list[1]:
                    search_input = str(name_list[i]) + ' ' + str(affiliation_list[i])
                elif file_name == file_list[2]:
                    search_input = str(name_list[i]) + ' ' + str(country_list[i])
                else:
                    search_input = str(name_list[i])
                # for each input in the list, it replaces the spaces with pluses, allowing the new string to be inserted directly into the url
                search_input = str(search_input.replace(' ', '+'))
                # yields request
                yield scrapy.Request(url=f'https://www.bing.com/search?q=site%3Alinkedin.com%2Fin%2F+%27{search_input}%27&count=100', callback=self.parse, headers={
                    'User-Agent': user_agent
                })

        # yields request to parse function with search_input planted in the url, along with a special user agent
        for file_name in file_list:
            # calls yield_link_for_file generator for each file
            yielded_links = yield_link_for_file(file_name)
            for request in yielded_links:
                # yields request to parse function with search_input planted in the url, along with a user agent to mask its script identity
                yield request
        
        
    def parse(self, response):
        # initialize lists
        profile_name = []
        profile_links = []
        # gets all links as 'a' tag HTML objects in results page
        results = response.xpath('//main/ol/li/h2/a')
        # gets keywords from url by fixing up the request url so that the program can just use the split function to get the keywords
        search_value = response.request.url.replace('https://www.bing.com/search?q=site%3Alinkedin.com%2Fin%2F+%27','').replace('%27&count=100','').replace('%20',' ')
        keywords = search_value.split('+')
        # For each keyword, it checks whether its the first or second keyword, or in the case of a middle name, 
        # not an all caps word like we would expect from affiliation or country of origin. 
        # This is for the purposes of limiting the first column in the output file to just the name.
        for keyword in keywords:
            if (not keyword.isupper() or keyword == keywords[0]) or keyword == keywords[1]:
                profile_name.append(keyword)
        # creates profile_name based on keyword
        profile_name = ' '.join(profile_name).replace('+', ' ')
        # checks results to see whether they are reliable links
        for result in results:
            # gets link and header as HTML child objects of the results
            link = result.xpath('.//@href').get()
            header = result.xpath('.//text()').get()
            # checks whether the result is a link
            if profile_name.lower() in header.lower() and 'linkedin.com' in link:
                profile_links.append(link)
        # yields name to the output file
        for profile in profile_links:
            yield{'name': profile_name, 'link': profile}
        # Checks whether name is the last one of a particular list. If it is, then it yields three blank lines to the output file.
        for file_name in file_list:
            # read encoded csv into parsable pandas data
            data = pandas.read_csv(file_name, encoding='latin')
            # turns pandas data into list containing name, affiliation, and country of origin according to file name
            name_list = list(data.name)
            # Checks whether name is the last one of a particular list. If it is, then it yields three blank lines to the output file.
            if profile_name == name_list[-1]:
                yield{'name': '', 'link': ''}
                yield{'name': '', 'link': ''}
                yield{'name': '', 'link': ''}
        
    
