from lxml import html
import requests
import httplib2
from BeautifulSoup import BeautifulSoup, SoupStrainer
import sys
from time import sleep

# Global variables
artist_list = []
song_list = []
file = open('input.txt', 'w')
lyrics = []

# Main function
def main():
	read_artist_list()
	for artist in artist_list:
		crawl_song_list()
	file.close()

# Read artist list from a file list.dat inside the directory and append to artist_list[]
def read_artist_list():
	list = open('list.dat', 'r')
	for line in list:
		artist_list.append(line.strip())
	list.close()

# Crawls through every artist's page and retrieves valid song links.
def crawl_song_list():
	for artist in artist_list:
		http = httplib2.Http()
		status, response = http.request('http://lyrics.wikia.com/wiki/' + artist)

		# For each link in the provided website:
		for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
		    if link.has_key('href'):
		        save = link['href']
		        try:
		        	if str(save[6]) == artist[0] and str(save[7]) == artist[1]:
		        		song_list.append(save) # Append them to song_list
		        except IndexError as err:
		        	pass
		scrape_lyrics(artist)

# Retrieve the lyrics from the list of links in song_list based on lyricbox element.
def scrape_lyrics(artist):
	print("Retrieving lyrics all " + artist + " lyrics and storing in input.txt.")
	for i in range(len(song_list)):

		# Display percent done.
		percent_done = (100 * i) / len(song_list)
		sys.stdout.write('\r')
		sys.stdout.write(str(percent_done) + "%")
		sys.stdout.flush()
		# sleep(0.25)

		try:
			page = requests.get('http://lyrics.wikia.com' + song_list[i])
			tree = html.fromstring(page.content)
			lyrics = tree.xpath('//div[@class="lyricbox"]/text()')
			
			for verses in lyrics:
				file.write(verses + '\n')
			file.write('\n\n')

		except:
			pass

	print("Done with " + artist + ".")


# Run main
main()
