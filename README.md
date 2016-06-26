# GenColorThemes
*Generating simple color themes for browsers.*

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

## Preview
image
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
    gct.theme_description = 'Description'
**Another Out-folder path:**

    p.template_path_out = 'out'
**Edit manifest.json:**

*everything except - ch.template_manifest **\[\'theme\'\]***

    ch = gct.Chromium()
    ch.template_manifest['default_locale'] = 'en'
    ch.template_manifest['version'] = '2'
    ...

## License
**[MIT License](https://opensource.org/licenses/MIT "Text license")**
