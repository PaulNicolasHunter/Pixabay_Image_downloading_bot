from robobrowser import RoboBrowser  # a module solely based upon BeautifulSoup and requests
import urllib.request
from urllib.parse import urljoin

browser = RoboBrowser(parser='html5lib')


class PixaBay:
	def __init__(self, picsof, howmany, place=''):
		self.picsof = picsof  # what images you want
		self.howmany = howmany  # how many pics you want
		self.place = place  # file in where all pics will be saved
		self.imgNumber = 0  # an counter to count the number of images
		self.links = list()  # a list to store all hrefs
		self.pagenum = 1

	def searchIn(self):
		"""opening the website and inserting the query"""

		browser.open('https://pixabay.com/')  # open the website

		search = browser.get_form(action='/en/photos/')  # find the form

		search.fields['q'].value = self.picsof  # fill the form

		browser.submit_form(search)  # submit the form

		return self.getHref()

	def getHref(self):  # get the href of the final image from the thumbnail image

		if str(browser.url)[
			-1] == '=' and self.imgNumber != 0:  # if the number of pages ended i.e. to remain duplicacy of images
			return self.getImages()

		link = browser.find_all('div', {'class': 'item'})

		for hrefs in link:
			thumb_img_url = urljoin(browser.url, hrefs.a.get(
				'href'))  # joining the href with the url i.e. 'https://pixabay.com/' + href

			self.links.append(thumb_img_url)
			self.imgNumber += 1

			if self.imgNumber == self.howmany:
				return self.getImages()

			elif hrefs == link[-1]:  # open another page if the number of images exceeds in current page
				self.pagenum += 1
				self.openNew()

	def openNew(self):
		browser.open(
			'https://pixabay.com/en/photos/?min_height=&image_type=&cat=&q=Wolfs&min_width=&pagi=' + str(self.pagenum))

		return self.getHref()  # calling the getHref to get hrefs again till the numbers are satisfied

	def getImages(self):

		img = 1
		for link in self.links:
			browser.open(link)

			final_image = browser.find('div', {'id': 'media_container'})

			src = final_image.img.get('src')  # finding the src
			filename = self.place + self.picsof + '_' + str(img) + '.jpeg'
			urllib.request.urlretrieve(src, filename=filename)  # saving the file

			img += 1  # incrimenting the name


topic = input(
	'Enter the topic, number of images you want and Destination where you want images to be saved(optional) separated by a space\n').split()

if len(topic) == 2:

	RetrieveImages = PixaBay(topic[0], int(topic[1]))
	RetrieveImages.searchIn()

elif len(topic) == 3:
	RetrieveImages = PixaBay(topic[0], int(topic[1]), str(topic[2].encode('unicode_escape')).replace(r'\\\\', r'\\'))
	RetrieveImages.searchIn()

else:
	print('Wrong number of arguments')
