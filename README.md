#Teufelsturm TXT
A scraper for the local climbing forum of Elbsandstein "teufelsturm.de". The script gets all rout ratings and saves them in txt file grouped by sectors and summits. This means that you can access your own offline version of Teufelsturm on your own smartphone even without Internet access. The pictures of the routes can also be saved.

## Usage

If necessary adapt the adaptable parts of the config file:

```
EXPORT_BASE_PATH = "./teufelsturm_txt/"
NR_OF_THREADS = 8
EXPORT_PHOTOS = True
```

Run the Scaper:

```
python scraper.py
```

Copy the folder `teufelsturm_txt` to your smartphone.
