import os
import requests
import urllib.request
import sys
from multiprocessing.pool import ThreadPool
from threading import Lock
from config import BASE_URL, PHOTO_BASE_URL, GIPFEL_URL, GIPFEL_URL_PARAMS, EXPORT_BASE_PATH, GRADING_TRANSFORM, NR_OF_THREADS, EXPORT_PHOTOS


# define helper
def dir_existend(path):
    return os.path.exists(path)


def mkdir(path):
    try:
        os.makedirs(path)
    except Exception as e:
        print("error creating path %s" % path)


def create_nomedia_file(path):
    file_path = os.path.join(path, ".nomedia")
    open(file_path, 'a').close()


lock = Lock()


def parse_summit(summit_soup):
    summit_title = summit_soup.find("h3").text
    region_title = summit_soup.find("p").text
    count_routes = summit_soup.find("span").text
    route_url = summit_soup.find("a")["href"]

    region_path = os.path.join(
        EXPORT_BASE_PATH, region_title)

    lock.acquire()
    if not dir_existend(region_path):
        mkdir(region_path)
    lock.release()

    summit_dir_name = "%s_%s" % (summit_title, count_routes)
    summit_path = os.path.join(region_path, summit_dir_name)
    mkdir(summit_path)

    # parsing routes
    full_summit_url = BASE_URL + route_url
    try:
        routes_data = requests.get(full_summit_url)
        routes_soup = BeautifulSoup(routes_data.text, "html.parser")
    except Exception:
        print("could not get summit: %s" % full_summit_url)
        print("skipping summit")
        return

    for route_soup in routes_soup.findAll("li"):
        route_title = route_soup.find("strong").text.replace(
            " ", "_").replace("/", "-")
        difficulty = route_soup.find("p").text.split(
            "\xa0")[-1].strip().replace("/", "-")
        overall_rating = GRADING_TRANSFORM.get(
            route_soup.find("img")["src"].split("/")[-1], "?")
        count_ratings = route_soup.find("span").text.strip()
        rating_url = route_soup.find("a")["href"]

        route_file_extension = ".txt"
        route_file_name = "[%s]_%s_%s_(%s)" % (
            difficulty, overall_rating, route_title, count_ratings)
        route_path = os.path.join(
            summit_path, route_file_name+route_file_extension)

        # add file content header
        route_file_content = "%s\n\n\n" % route_file_name.replace("_", " ")

        full_route_url = BASE_URL + rating_url
        try:
            ratings_data = requests.get(full_route_url)
            ratings_soup = BeautifulSoup(ratings_data.text, "html.parser")
        except Exception:
            print("could not get route: %s" % full_route_url)
            print("skipping route")
            continue

        for rating_soup in ratings_soup.findAll("li"):
            try:
                tmp_rating_header = rating_soup.find("small").text.strip()
                rating_date = tmp_rating_header[-10:]
                rating_author = tmp_rating_header[0:-10]
                rating_text = rating_soup.find("div").text
                rating_opinion = rating_soup.find(
                    "strong").text if rating_soup.find("strong") else "?"

                route_file_content += ">>> %s | %s | %s\n%s~~~~~~\n\n" % (
                    rating_author, rating_date, rating_opinion, rating_text)
            except Exception as e:
                print("failed to get rating...skip")
                continue

        # write ratings to file
        with open(route_path, "w", encoding="utf-8")as f:
            f.write(route_file_content)

        # check whether there are photos
        if EXPORT_PHOTOS:
            photo_path = os.path.join(summit_path, route_file_name+"__photos")
            for photo_soup in ratings_soup.select("center > a > img"):
                if not dir_existend(photo_path):
                    mkdir(photo_path)
                    create_nomedia_file(photo_path)
                full_photo_number = "%04d" % (int(photo_soup["src"][-8:-4])-1)
                photo_name = "pic%s.jpg" % full_photo_number
                full_photo_url = PHOTO_BASE_URL+photo_name
                try:
                    urllib.request.urlretrieve(
                        full_photo_url, os.path.join(photo_path, photo_name))
                except Exception as e:
                    print("can not get photo %s" % full_photo_url)
    return


if __name__ == "__main__":

    threadPool = ThreadPool(processes=NR_OF_THREADS)
    threads = []
    summits_data = requests.post(GIPFEL_URL, params=GIPFEL_URL_PARAMS)
    summits_soup = BeautifulSoup(summits_data.text, "html.parser")

    # getting summit data
    for summit_soup in summits_soup.findAll("li"):
        thread = threadPool.apply_async(
            parse_summit, (summit_soup,))
        threads.append(thread)

    # joining threads
    for thread in threads:
        thread.get()

    print("~~~~~DONE~~~~~~")
