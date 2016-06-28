# GenColorThemes [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/vyach-vasiliev/GenColorThemes/master/LICENSE) [![Chrome](https://img.shields.io/badge/Chrome-20+-40A977.svg)](https://atom.io) [![FireFox](https://img.shields.io/badge/FireFox-30+-FF931F.svg)](https://atom.io) [![FireFox](https://img.shields.io/badge/Maxthon-3+-6B96C6.svg)](https://atom.io) [![FireFox](https://img.shields.io/badge/Opera-soon-F84646.svg)](https://atom.io)

Generating simple color themes for browsers.
## Preview
##### Google Chrome (Emerland)
![Google Chrome][1]
##### Mozilla FireFox (Pomegrante)
![Mozilla FireFox][2]
##### Maxthon (Wetasphalt)
![Maxthon][3]

[1]: Preview/google_chrome.png "Необязательный титул"
[2]: Preview/mozilla-ff.png "Необязательный титул"
[3]: Preview//maxthon.png "Необязательный титул"
## Supported

**Chromium-like (Windows, Mac OS, Linux):**
* Chromium *(20+)*
* Google Chrome *(20+)*
* Comodo Dragon *(20+)*
* SRWare Iron *(20+)*
* Yandex Browser *(30+)*
* etc.


**FireFox-like (Windows, Mac OS, Linux):**
* Mozilla Firefox *(30+)*
* Mozilla SeaMonkey *(30+)*
* Mozilla Thunderbird *(30+)*
* Sunbird
* Komodo IDE
* Komodo Edit
* etc.

**Other apps:**
* Maxthon *(3+)*

***Not-supported browsers:***
 * *Vivaldi*
 * *Opera*
 * *Amigo*

## How to use
    p = gct.Params()
    p.theme_name = "Test theme"
    p.theme_description = "Test description"
    ch = gct.Chromium().create('#27ae60', p)
## Out
    out/
    |- Chromium-like/
      |- name-theme/
        |- resources/
           |-  _locales/
               |--  ... (<lang_code>/messages.json)
           |-  images/
               |--  ... (*.png)
           |-  manifest.json
        |- name-theme.crx
        |- name-theme.pem
        |- name-theme.zip (option)
    |- FireFox-like
        |- name-theme/
           |- install.html
    |- Maxthon
       |- name-theme.mxskin

## More
**Create an additional .zip archive:**

    ch = gct.Chromium()
    ch.zip = True
**Another Chrome-browser path:**

    ch = gct.Chromium()
    ch.browser_path = 'C:\\Google\\Chrome\\Application'
**Another Out-folder path:**

    p.template_path_out = 'out'
**Edit manifest.json:**

*everything except - ch.template_manifest ['theme']*

    ch = gct.Chromium()
    ch.template_manifest['default_locale'] = 'en'
    ch.template_manifest['version'] = '2'
    ...

## License
**[MIT License](https://opensource.org/licenses/MIT "Text license")**
