from bs4 import BeautifulSoup
import requests, os

breast_size = 'a'
page_number = 1
url = "https://www.pornhub.com/pornstars?cup={}&breasttype=natural&page={}".format(breast_size, page_number)

#"https://www.pornhub.com/pornstars?cup={}&breasttype=natural&page={}".format(breast_size, page_number)
req = requests.get(url)
soup = BeautifulSoup(req.content, "html.parser")
pron_stars = soup.find_all(class_="pornstarLi")
porn_stars_names = [res['href'] for res in soup.find_all(class_="js-mxp")] # In roies case : class = r'label-card-head-flex'


def extract_porn_star_images(porn_star_name: str):
    print(porn_star_name)
    url_porn_star_page = r"https://www.pornhub.com{}".format(porn_star_name)
    url_porn_star_photos = url_porn_star_page + '/photos'
    req = requests.get(url_porn_star_photos)
    # TODO check request
    find_porn_star_albums(req)
    print('debug_extract porn_star_images')


def find_porn_star_albums(porn_star_photos_url: requests.models.Response):
    soup = BeautifulSoup(porn_star_photos_url.content, "html.parser")
    porn_star_albums_soup_list = soup.find_all(class_="photoAlbumListBlock")
    porn_star_albums_link_list = []
    for porn_star_album in porn_star_albums_soup_list:
        possible_href_list = porn_star_album.find_all('a')
        for possible_href in possible_href_list:
            if 'href' in possible_href.attrs:
                porn_star_albums_link_list.append(r"https://www.pornhub.com{}".format(possible_href['href']))
    
    images_link = get_imgs_link(porn_star_albums_link_list)
    download_images(images_link)
    print('debug find porn star albums')
    return porn_star_albums_link_list

def get_imgs_link(porn_star_albums:list):
    for album in porn_star_albums:
        res = requests.get(album)
        soup = BeautifulSoup(res.content, "html.parser")
        all_pictures_list = soup.find_all(class_="js_lazy_bkg")
        pictures_jpg_links_list = []
        for picture_soup in all_pictures_list:
            if 'data-bkg' in picture_soup.attrs:
                pictures_jpg_links_list.append (picture_soup['data-bkg'])
    return pictures_jpg_links_list

def download_images(imgs2download: list):
    k = 0
    for img_link in imgs2download:
        k += 1
        download_img(img_link,breast_size + str(k), 'jpg')

def download_img (Img_Src_URL , Img_Name,Img_type="png"):
    res = requests.get(Img_Src_URL)
    res.raise_for_status()
    imageFile = open(os.path.join( os.path.basename(str(Img_Name)+'.'+str(Img_type))), 'wb') # img name
    for chunk in res.iter_content(100000):
        imageFile.write(chunk)
    imageFile.close()

extract_porn_star_images(porn_stars_names[0])

print('debug!')
