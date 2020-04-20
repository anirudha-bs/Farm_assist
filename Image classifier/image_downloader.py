from google_images_download import google_images_download   #importing the library

response = google_images_download.googleimagesdownload()   #class instantiation

arguments = {"keywords":"alluvial soil field","limit":100,"print_urls":True,"chromedriver":"/home/anirudha/chromedriver_linux64/chromedriver"}   #creating list of arguments
paths = response.download(arguments)   #passing the arguments to the function

