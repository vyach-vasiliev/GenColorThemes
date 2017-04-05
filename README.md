# GenColorThemes
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/vyach-vasiliev/GenColorThemes/master/LICENSE) [![Chrome](https://img.shields.io/badge/Chrome-20+-40A977.svg)](https://www.google.com/chrome/) [![FireFox](https://img.shields.io/badge/FireFox-30+-FF931F.svg)](https://mozilla.org/firefox) [![Maxthon](https://img.shields.io/badge/Maxthon-3+-6B96C6.svg)](http://maxthon.com/) [![Opera Presto](https://img.shields.io/badge/Opera-Presto-F84646.svg)](http://opera.com/) [![Opera Blink](https://img.shields.io/badge/Opera-Blink-F84688.svg)](http://opera.com/) [![Support me](https://img.shields.io/badge/Support_me-PayPal-33cc33.svg)](https://www.paypal.me/wencelsaus/3)

Generating simple color themes for browsers. Works on **Python 2.7+** and **3.4+**
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

### Supported

* **Chromium-like** (Windows, Mac OS, Linux):
    * [360 Browser](http://www.360safe.com/) *(5+)*
    * [Baidu Spark Browser](baidu.com) *(30+)*
    * [Blisk Browser](https://blisk.io/) *(0.3+)*
    * [Cent Browser](https://www.centbrowser.com/)
    * [Chromium Browser](https://www.chromium.org/getting-involved/download-chromium) *(20+)*
    * [Citrio Browser](http://citrio.com/)
    * [Comodo Dragon Browser](https://browser.comodo.com/) *(30+)*
    * [Comodo Dragon](https://www.comodo.com/home/browsers-toolbars/browser.php) *(20+)*
    * [CoolNovo Browser](https://ru.wikipedia.org/wiki/CoolNovo) (project is closed)
    * [Coowon Browser](http://coowon.com/) (project is closed)
    * [Cốc Cốc Browser](https://coccoc.com/) *(40+)*
    * [Epic Privacy Browser](https://www.epicbrowser.com/) *(2013+)*
    * [Google Chrome Browser](https://www.google.com/chrome/) *(20+)*
    * [Google Chrome Canary Browser](https://www.google.com/chrome/browser/canary.html) *(20+)*
    * [Iridium Browser](https://iridiumbrowser.de/) *(30+)*
    * [Opera Blink](http://opera.com/) (Only background image)
    * [Opera Presto](http://opera.com/) *(+18)*
    * [SRWare Iron Browser](https://www.srware.net/en/software_srware_iron.php) *(20+)*
    * [Slimjet Browser](https://www.slimjet.com/) *(10+)*
    * [Torch Web Browser](https://torchbrowser.com/)
    * Not tested
        * [UC Browser](https://www.ucweb.com/)


* **FireFox-like** (Windows, Mac OS, Linux):
    * [Comodo IceDragon Browser](https://browser.comodo.com/) *(30+)*
    * [Mozilla Firefox Browser](https://mozilla.org/firefox) *(30+)*
    * [Mozilla SeaMonkey Browser](http://seamonkey-project.org/) *(2+)*
    * [Mozilla Thunderbird Email-client](https://mozilla.org/thunderbird) *(30+)*
    * [Pale Moon Browser](https://www.palemoon.org/) *(20+)*
    * [Tor Browser](https://www.torproject.org/projects/torbrowser.html) *(3+)*
    * etc.


* **Other apps** (Windows, Mac OS, Linux):
    * [Maxthon](http://maxthon.com/) *(3+)*


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



### How to use
    p = gct.Params()
    p.theme_name = "Test theme"
    p.theme_description = "Test description"
    ch = gct.Chromium().create('#27ae60', p)
### Output structure

    out/
    ├──  Chromium-like/
    │    ├──  name-theme/
    │    │    ├──  resources/
    │    │    │    ├──  _locales/
    │    │    │    │    └──  ... (<lang_code>/messages.json)
    │    │    │    ├──  images/
    │    │    │    │    └──  ... (*.png)
    │    │    │    └──  manifest.json
    │    │    ├── name-theme.crx
    │    │    ├── name-theme.pem
    │    │    └── name-theme.zip (option)
    ├──  FireFox-like
    │    └──  name-theme/
    │         └── install.html
    └──  Maxthon
         └──  name-theme.mxskin

### More
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

### License
**[MIT License](https://opensource.org/licenses/MIT "Text license")**
or see the [LICENSE file](..blob//master/LICENSE)

[Why you need a license?](..blob//master/LICENSE_INFO.md)

### Beer?
[Support me](https://www.paypal.me/wencelsaus/3) or  just write what you would like to add to the program.

I will always be happy with your feedback. Do not be shy, write to me!