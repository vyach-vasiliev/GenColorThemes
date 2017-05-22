# GenColorThemes
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/vyach-vasiliev/GenColorThemes/master/LICENSE)
[![Chrome](https://img.shields.io/badge/Chrome-20+-40A977.svg)](https://www.google.com/chrome/)
[![FireFox](https://img.shields.io/badge/FireFox-30+-FF931F.svg)](https://mozilla.org/firefox)
[![Maxthon](https://img.shields.io/badge/Maxthon-3+-6B96C6.svg)](http://maxthon.com/)
[![Opera Presto](https://img.shields.io/badge/Opera-Presto-F84646.svg)](http://opera.com/)
[![Opera Blink](https://img.shields.io/badge/Opera-Blink-F84688.svg)](http://opera.com/)
[![Support me](https://img.shields.io/badge/Support_me-PayPal-33cc33.svg)](https://www.paypal.me/wencelsaus/3)

Generating simple color themes for browsers. Works on **Python 2.7+** and **3.4+**

---
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

---
### Supported apps

- [x] **Chromium-like** (Windows, Mac OS, Linux):
    - [x] [360 Browser](http://www.360safe.com/) *(5+)*
    - [x] [Baidu Spark Browser](baidu.com) *(30+)*
    - [x] [Blisk Browser](https://blisk.io/) *(0.3+)*
    - [x] [Cent Browser](https://www.centbrowser.com/)
    - [x] [Chromium Browser](https://www.chromium.org/getting-involved/download-chromium) *(20+)*
    - [x] [Citrio Browser](http://citrio.com/)
    - [x] [Comodo Dragon Browser](https://browser.comodo.com/) *(30+)*
    - [x] [Comodo Dragon](https://www.comodo.com/home/browsers-toolbars/browser.php) *(20+)*
    - [x] [CoolNovo Browser](https://ru.wikipedia.org/wiki/CoolNovo) (project is closed)
    - [x] [Coowon Browser](http://coowon.com/) (project is closed)
    - [x] [Cốc Cốc Browser](https://coccoc.com/) *(40+)*
    - [x] [Epic Privacy Browser](https://www.epicbrowser.com/) *(2013+)*
    - [x] [Google Chrome Browser](https://www.google.com/chrome/) *(20+)*
    - [x] [Google Chrome Canary Browser](https://www.google.com/chrome/browser/canary.html) *(20+)*
    - [x] [Iridium Browser](https://iridiumbrowser.de/) *(30+)*
    - [x] [Opera Blink](http://opera.com/) (Only background image)
    - [x] [Opera Presto](http://opera.com/) *(+18)*
    - [x] [SRWare Iron Browser](https://www.srware.net/en/software_srware_iron.php) *(20+)*
    - [x] [Slimjet Browser](https://www.slimjet.com/) *(10+)*
    - [x] [Torch Web Browser](https://torchbrowser.com/)
    - [ ] Not tested
        - [UC Browser](https://www.ucweb.com/)


- [x] **FireFox-like** (Windows, Mac OS, Linux):
    - [x] [Comodo IceDragon Browser](https://browser.comodo.com/) *(30+)*
    - [x] [Mozilla Firefox Browser](https://mozilla.org/firefox) *(30+)*
    - [x] [Mozilla SeaMonkey Browser](http://seamonkey-project.org/) *(2+)*
    - [x] [Mozilla Thunderbird Email-client](https://mozilla.org/thunderbird) *(30+)*
    - [x] [Pale Moon Browser](https://www.palemoon.org/) *(20+)*
    - [x] [Tor Browser](https://www.torproject.org/projects/torbrowser.html) *(3+)*
    - [x] etc.


- [x] **Other apps** (Windows, Mac OS, Linux):
    - [x] [Maxthon](http://maxthon.com/) *(3+)*


* ***Not-supported apps:***
     * [Amigo](http://amigo.mai.ru/)
     * [Komodo Edit](http://komodoide.com/komodo-edit)
     * [Komodo IDE](http://www.komodoide.com/)
     * [Vivaldi](https://vivaldi.com/)
     * [Yandex Browser](https://browser.yandex.com/) (No longer supported. Internal setting.)
     * No support for skins
         * [Brave](https://www.brave.com/)
         * [Internet Explorer](http://microsoft.com/ie)
         * [Midori](http://www.midori-browser.org/)
         * [Mozilla Sunbird](https://www.mozilla.org/en-US/projects/calendar/)
         * [Safari](https://apple.com/safari)
         * [Sleipnir](http://www.fenrir-inc.com/jp/sleipnir/)


---
### How to use
```python
import GenColorThemes.gen as gct
p = gct.Params()
p.theme_name = "Test theme"
p.theme_description = "Test description"
ch = gct.Chromium().create('#27ae60', p)
```

### Output structure

    out/
    ├──  Chromium-like/
    │    ├──  resources/
    │    │    ├──  _locales/
    │    │    │    └──  ... (<lang_code>/messages.json)
    │    │    ├──  images/
    │    │    │    └──  ... (*.png)
    │    │    └──  manifest.json
    │    ├──  name-theme.crx
    │    ├──  name-theme.pem
    │    └──  name-theme.zip (option)
    │
    ├──  FireFox-like
    │    └──  name-theme/
    │         └── install.html
    ├──  Maxthon
    │    └──  name-theme.mxskin
    ├──  Opera-Blink
    │    ├──  name-theme/
    │    │    ├──  opera.ini
    │    │    └──  persona.ini
    │    └──  name-theme.zip
    │
    ├──  Opera-Presto
    │    ├──  name-theme/
    │    │    ├──  opera.ini
    │    │    └──  persona.ini
    │    └──  name-theme.zip
    └──  Slim
         ├──  name-theme/
         │    ├──  skin.ini
         │    └──  ... (*.bmp)
         └──  name-theme.zip

### More
**Create an additional .zip archive:**
```python
ch = gct.Chromium()
ch.zip = True
```
**Another Chrome-browser path:**
```python
ch = gct.Chromium()
ch.browser_path = 'C:\\Google\\Chrome\\Application'
```
**Another Out-folder path:**
```python
p.template_path_out = 'out'
```
**Edit manifest.json:**

*everything except - ch.template_manifest ['theme']*

```python
ch = gct.Chromium()
ch.template_manifest['default_locale'] = 'en'
ch.template_manifest['version'] = '2'
...
```
---
### License
**[MIT License](https://opensource.org/licenses/MIT "Text license")**
or see the [LICENSE file](/LICENSE)

[Why you need a license?](/LICENSE_INFO.md)

### Beer?
[Support me](https://www.paypal.me/wencelsaus/3) or  just write what you would like to add to the program.

I will always be happy with your feedback. Do not be shy, write to me!