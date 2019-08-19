# CONFIG

# Adaptable part of the config
EXPORT_BASE_PATH = "./teufelsturm_txt/"
NR_OF_THREADS = 8
EXPORT_PHOTOS = True

# Do not change this secton
BASE_URL = "http://teufelsturm.de/m/"
PHOTO_BASE_URL = "http://teufelsturm.de/img/fotos/"
GIPFEL_URL = BASE_URL + "gipfelsuche.php"
GIPFEL_URL_PARAMS = {"start": 1, "anzahl": 1500}
GRADING_TRANSFORM = {"arrow-right.gif": "o", "arrow-downright.gif": "-", "arrow-downright2.gif": "--",
                     "arrow-downright3.gif": "---", "arrow-upright.gif": "+", "arrow-upright2.gif": "++", "arrow-upright3.gif": "+++"}
