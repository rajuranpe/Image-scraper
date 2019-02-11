# writing images
import requests, time
from bs4 import BeautifulSoup as bs

class Downloader():

    # add random lengthed delay to prevent high traffic and blocking
    def delayLoop(self):
        for i in range(1, 5):
            time.sleep(i)


    # download the page to do parsing
    def parser(url):
        page = requests.get(url, timeout=5)
        soup = bs(page.text, 'html.parser')
        return soup


    # modify url for the next page
    def generatePageNum(n, url):
        if n == 1:
            return url
        if n > 1:
            urln = url.replace(firstPageNotation, multiPageNotationPre + str(n) + MultiPageNotationPost) #pageindex
            print(urln)
            return urln


    # check, if the page has content. This way it is possible to both check the number of pages with content,
    # and see if the tags had none in the first place
    def testNextPage(url, n):
        url = generatePageNum(n, url)
        soup = parser(url)
        if soup.find(endOfContentTag,  text=endOfContentMes):
            print("No more content.")
            return "end"
        print(n)
        return url

    # site as an object, which inherits this class and gives it's specific html-tags
    def download(url, site, searchTags):

        # TODO
        # sorting, rating, show statistics, set maximum download amount, change download directory in the GUI
        # add sites
        # on each image, test if it has a larger resolution variation, and according to settings notify it or pass

        firstPageUrl = url
        n = 1
        x = 0

        #loop for all the pages and image pages they containt
        while True:
            try:
                url = testNextPage(firstPageUrl, n)
                if url == "end":
                    print("End of content.")
                    break
                soup = parser(url)
                existing_images = soup.findAll(siteTag, attrs=siteAttrs) # locate all elements on the page with tag
                for image in existing_images:
                    try:
                        tags = image[mainPageTag]
                        url1 = site.getUrl() + tags
                        page = requests.get(url1, timeout=5)
                        soppa = bs(page.text, 'html.parser')
                        imgPage = soppa.find(imgTag, attrs=imgAttrs)
                        urln = imgPage['src']
                        print(urln)
                        response = requests.get(urln, timeout=5)
                        if response.status_code == 200:
                            with open(searchTags + " " + str(x) + '.jpg', 'wb') as w:
                                w.write(requests.get(urln, timeout=10).content)
                                w.close()
                                x += 1
                                delayLoop()
                    except ValueError:
                        pass
                n += 1
            except requests.ConnectionError as e:
                print("Connection Error.")
                print(str(e))
            except requests.Timeout as e:
                print("Timeout Error.")
                print(str(e))
            except requests.RequestException as e:
                print("General Error.")
                print(str(e))
            except KeyboardInterrupt:
                print("The program has been closed.")
