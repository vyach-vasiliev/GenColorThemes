#!/usr/bin/env python3

import subprocess
import colorsys
import zipfile
import struct
import random
import math
import png
import json
import sys
import os


class Help:
    version = "0.2.3"
    name = "0.2.3"
    url = "http://github.com/vyach-vasiliev/gencolorthemes"


class Params:
    def __init__(self):
        self.theme_id = 'GenColorThemes-' + str(random.random()).split('.')[1]
        self.theme_name = ""
        self.theme_description = "Simple color theme"
        self.template_path_out = 'out'
        self.main_color = None
        self.main_color_hex = None
        self.text_color_hex = 'Auto'

    def checkParams(self, main_color, params):
        if main_color:
            params.main_color = main_color
        else:
            raise ValueError("Oops!  That was VALUE is empty <main_color>. Fix it and try again.")
        if type(params.main_color) == str:
            params.main_color = params.main_color.replace('#', '')
            params.main_color_hex = params.main_color
            if len(params.main_color) > 6 or len(params.main_color) < 6:
                raise ValueError("Oops!  That was no valid LENGTH <main_color> > 6 or < 6. Fix it and try again.")
            params.main_color = struct.unpack('BBB', bytes.fromhex(params.main_color))
        elif type(params.main_color) == tuple or type(params.main_color) == list:
            if len(params.main_color) > 3 or len(params.main_color) < 3:
                raise ValueError("Oops!  That was no valid VALUE <main_color> > 3 or < 3. Fix it and try again.")
        else:
            raise TypeError(
                "Oops!  That was no valid TYPE <main_color> - " + type(params.main_color) + " Fix it and try again.")
        return True, params


class Chromium:
    def __init__(self):
        self.template_manifest = {
            "name": "GenColorThemes",
            "description": "Simple color theme.",
            "default_locale": "en",

            "theme": {
                "colors": {
                    "bookmark_text": [63, 18, 14],
                    "frame": [39, 174, 96],
                    "ntp_header": [192, 57, 43],
                    "ntp_link": [63, 19, 19],
                    "ntp_link_underline": [63, 19, 19],
                    "ntp_text": [51, 35, 35],
                    "tab_background_text": [50, 0, 0],
                    "tab_text": [50, 0, 0],
                    "toolbar": [247, 242, 242]
                },
                "images": {
                    "theme_frame": "images/theme_frame.png",
                    "theme_tab_background": "images/theme_tab_background.png",
                    "theme_tab_background_incognito": "images/theme_tab_background.png",
                    "theme_toolbar": "images/theme_toolbar.png"
                }
            },

            "update_url": "http://clients2.google.com/service/update2/crx",
            "manifest_version": 2,
            "version": "2"
        }
        self.template_locale = {
            'de': ['De Name', 'De Desc'],
            'en': ['En Name', 'En Desc'],
            'ru': ['Ru Имя', 'Ru Описание'],
            'es': ['', ''],
            'hi': ['', ''],
            'it': ['', ''],
            'pl': ['', ''],
            'ro': ['', ''],
            'th': ['', ''],
            'uk': ['', ''],
            'zh_CN': ['', ''],
            'zh_TW': ['', '']
        }
        self.template_images = {
            'theme_frame': '',
            'theme_tab_background': '',
            'theme_toolbar': '',
        }
        self.browser_path = ''
        self.zip = None
        self.params = None

    def create(self, main_color, params):
        print("Starting create Chromium theme...")
        result_check = Params().checkParams(main_color, params)
        if result_check[0]:
            self.params = result_check[1]
            if len(self.params.theme_name) > 0:
                self.template_manifest['name'] = self.template_manifest['name'] + '_' + params.theme_name
                params.theme_name = '/' + self.template_manifest['name']
            if len(self.params.theme_description) > 0:
                self.template_manifest['description'] = self.params.theme_description
            # Creating all directories
            if not os.path.exists(
                                    self.params.template_path_out + self.params.theme_name + '/Chromium-like/resources/images/'):
                # os.makedirs(params.template_path_out)
                os.makedirs(self.params.template_path_out + self.params.theme_name + '/Chromium-like/resources/images/')
            self._gen_colors(self.params.main_color)
            self._create_manifest()
            self._create_images()
            self._create_locales(self.template_locale)
            self._create_crx()
            if self.zip:
                _create_zip(self.params.theme_name + '.zip',
                            self.params.template_path_out + self.params.theme_name + '/Chromium-like/resources/',
                            self.params.template_path_out + self.params.theme_name + '/Chromium-like/'
                            )

        print('Chromium theme created. Thank you! :)')

    def _gen_colors(self, general_color_rgb):
        general_color_hsv = _rgb2hsv(general_color_rgb[0], general_color_rgb[1], general_color_rgb[2])

        theme_frame = general_color_rgb

        theme_tab_background = _hsv2rgb(general_color_hsv[0], 20, 90)

        theme_toolbar = _hsv2rgb(general_color_hsv[0], 2, 95)

        bookmark_text = _hsv2rgb(general_color_hsv[0], general_color_hsv[1], general_color_hsv[2] - 50)

        frame = general_color_rgb
        ntp_header = general_color_rgb

        ntp_link = _hsv2rgb(general_color_hsv[0], general_color_hsv[1] - 8, general_color_hsv[2] - 50)

        ntp_link_underline = _hsv2rgb(general_color_hsv[0], general_color_hsv[1] - 8, general_color_hsv[2] - 50)

        ntp_text = _hsv2rgb(0, general_color_hsv[1], general_color_hsv[2])
        ntp_text = [ntp_text[0] - 140, ntp_text[1], ntp_text[2]]

        tab_background_text = _hsv2rgb(general_color_hsv[0], 100, general_color_hsv[2] - 50)

        tab_text = _hsv2rgb(general_color_hsv[0], 100, general_color_hsv[2] - 50)

        toolbar = _hsv2rgb(general_color_hsv[0], 2, 95)

        # write to template_manifest
        self.template_manifest['theme']['colors']['bookmark_text'] = bookmark_text
        self.template_manifest['theme']['colors']['frame'] = frame
        self.template_manifest['theme']['colors']['ntp_header'] = ntp_header
        self.template_manifest['theme']['colors']['ntp_link'] = ntp_link
        self.template_manifest['theme']['colors']['ntp_link_underline'] = ntp_link_underline
        self.template_manifest['theme']['colors']['ntp_text'] = ntp_text
        self.template_manifest['theme']['colors']['tab_background_text'] = tab_background_text
        self.template_manifest['theme']['colors']['tab_text'] = tab_text
        self.template_manifest['theme']['colors']['toolbar'] = toolbar
        # write to template_images
        self.template_images['theme_frame'] = theme_frame
        self.template_images['theme_tab_background'] = theme_tab_background
        self.template_images['theme_toolbar'] = theme_toolbar

    def _create_manifest(self):
        self.template_manifest_json = json.dumps(self.template_manifest, sort_keys=True)

        f = open(self.params.template_path_out + self.params.theme_name + '/Chromium-like/resources/manifest.json', 'w')
        f.write(self.template_manifest_json)
        f.close()
        print('Create manifest.json success.')

    def _create_images(self):
        """ Example: 3x2 image
            list([ (R,G,B), (R,G,B), (R,G,B) ],
                 [ (R,G,B), (R,G,B), (R,G,B) ])
             a = [1, 2, 3]
             [[a]*3]*2
        """
        theme_frame_px = [[self.template_images['theme_frame']] * 1] * 50
        theme_tab_background_px = [[self.template_images['theme_tab_background']] * 1] * 30
        theme_toolbar_px = [[self.template_images['theme_toolbar']] * 1] * 120

        png.from_array(theme_frame_px, 'RGB').save(
            self.params.template_path_out + self.params.theme_name + '/Chromium-like/resources/images/theme_frame.png')
        png.from_array(theme_tab_background_px, 'RGB').save(
            self.params.template_path_out + self.params.theme_name + '/Chromium-like/resources/images/theme_tab_background.png')
        png.from_array(theme_toolbar_px, 'RGB').save(
            self.params.template_path_out + self.params.theme_name + '/Chromium-like/resources/images/theme_toolbar.png')
        print('Create images success.')

    def _create_locales(self, tmp_locale):
        """ Structure out file (NOTE: Passes locale with empty fields.)

        path: _locales/<lang_code>/messages.json
        body:
        {
          "appName": {
            "message": template_locale[0]
          },
          "appDesc": {
            "message": template_locale[1]
          }
        }
        """

        template_messages = {
            "appName": {
                "message": ""
            },
            "appDesc": {
                "message": ""
            }
        }

        print('Create locales files process...')
        # check empty tmp_locale

        if not os.path.exists(
                                self.params.template_path_out + self.params.theme_name + '/Chromium-like/resources/_locales'):
            os.makedirs(self.params.template_path_out + self.params.theme_name + '/Chromium-like/resources/_locales')
        for item in tmp_locale:
            if len(tmp_locale[item][0]) == 0 or len(tmp_locale[item][1]) == 0:
                print('\tPasses locale [' + item + ']. Is empty.')
                continue
            template_messages['appName']['message'] = tmp_locale[item][0]
            template_messages['appDesc']['message'] = tmp_locale[item][1]
            template_messages_json = json.dumps(template_messages, sort_keys=True)

            if not os.path.exists(
                                            self.params.template_path_out + self.params.theme_name + '/Chromium-like/resources/_locales/' + item):
                os.makedirs(
                    self.params.template_path_out + self.params.theme_name + '/Chromium-like/resources/_locales/' + item)

            f = open(
                self.params.template_path_out + self.params.theme_name + '/Chromium-like/resources/_locales/' + item + '/messages.json',
                'w')
            f.write(template_messages_json)
            f.close()
            print('\tCreate locale [' + item + '] success.')
        print('Create locales files success.')

    def _create_crx(self):
        print('Creating .CRX process...')
        abs_path = os.path.abspath(self.params.template_path_out + self.params.theme_name + '/Chromium-like/resources/')
        abs_path = abs_path.replace('\\', '/') + '/'
        appdata = os.getenv('APPDATA')
        appdata = appdata.split('\\')
        appdata = appdata[:len(appdata) - 1]
        appdata = '\\'.join(appdata)

        if self.browser_path:
            folder_chrome = self.browser_path
            if not os.path.exists(folder_chrome):
                raise FileNotFoundError("Folder not found: ", folder_chrome)
        else:
            folder_chrome = appdata + '/Local/Google/Chrome/Application'
            if not os.path.exists(folder_chrome):
                folder_chrome = appdata + '/Local/Google/Chrome SxS/Application'
            else:
                raise FileNotFoundError('Folder Chrome-browser not found. Please select your directory.')
        try:
            retcode = subprocess.call(
                '"' + folder_chrome + '/chrome" --pack-extension="' + abs_path + '" --no-message-box', shell=True)
        except OSError as e:
            print(sys.stderr, "\tExecution failed:", e)
        finally:
            old_file_crx = self.params.template_path_out + self.params.theme_name + '/Chromium-like/' + self.params.theme_name + '.crx'
            old_file_pem = self.params.template_path_out + self.params.theme_name + '/Chromium-like/' + self.params.theme_name + '.pem'
            if os.path.exists(old_file_crx):
                os.remove(old_file_crx)
            if os.path.exists(old_file_pem):
                os.remove(old_file_pem)
            os.rename(self.params.template_path_out + self.params.theme_name + '/Chromium-like/resources.crx',
                      self.params.template_path_out + self.params.theme_name + '/Chromium-like/' + self.params.theme_name + '.crx')
            os.rename(self.params.template_path_out + self.params.theme_name + '/Chromium-like/resources.pem',
                      self.params.template_path_out + self.params.theme_name + '/Chromium-like/' + self.params.theme_name + '.pem')
            print('Creating .CRX success')


class FireFox:
    def __init__(self):
        self._locales = {
            'en-US': {
                'title_html': 'Install theme',
                'develop_witch': 'Made witch',
                'theme_title': 'theme title',
                'description': 'description',
                'preview': 'preview',
                'install': 'install'
            },
            'ru-RU': {
                'title_html': 'Установка темы',
                'develop_witch': 'Сделано с',
                'theme_title': 'название темы',
                'description': 'описание',
                'preview': 'предпросмотр',
                'install': 'установить'
            }
        }
        self.template_install = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title id="title_html"></title><style>@import url(https://fonts.googleapis.com/css?family=Roboto:300); body{background: "%background_color%"; font-family: "Roboto", sans-serif;}.page{padding: 2em 0 0; margin: auto;}.form{position: relative; z-index: 1; background: #fff; max-width: 20em; margin: 0 auto 7em; padding: 4em 4em 2em; text-align: center;}.form input{outline: 0; background: #f2f2f2; width: 100%; border: 0; margin: 0 0 1em; padding: 1em; box-sizing: border-box; font-size: 1em;}.form button{text-transform: uppercase; outline: 0; background: #3498db; width: 100%; border: 0; padding: 1em; color: #fff; font-size: 1em; -webkit-transition: all 0.3 ease; transition: all 0.3 ease; cursor: pointer; margin-top: 0.5em;}.form button:hover, .form button:active, .form button:focus{/*background: #F499A2;*/ background: #35b9ff;}.form .install{text-transform: uppercase; outline: 0; background: #48D991; width: 100%; border: 0; padding: 1em; color: #fff; font-size: 1em; -webkit-transition: all 0.3 ease; transition: all 0.3 ease; cursor: pointer; margin-top: 0.5em;}.form .install:hover, .form .install:active, .form .install:focus{background: #56f49e;}.form .message{margin: 1em 0 0; color: #999; font-size: 0.7em;}.form .message a{color: #48D991; text-decoration: none;}.form .app_url{}h3#develop_witch:after{content: "❤"; margin: 7px; color: #FF6666;}</style></head><body><div class="page"> <div class="form"> <h1>%theme_name%</h1> <h3 id="develop_witch"></h3> <h3><a href="//github.com/vyach-vasiliev/gencolorthemes" style="border-bottom: 1px dotted;text-decoration: none;">Script Generate Flat Colors Themes (via GitHub)</a></h3> <form> <input id="theme_title" type="text" placeholder="" value="%theme_title%"/> <input id="description" type="text" placeholder="" value="%description%"/> <button id="preview" onmouseover="setTheme(this, PREVIEW);" onmouseout="setTheme(this, RESET_PREVIEW);"> Preview</button> <button id="install" class="install" onclick="setTheme(this, INSTALL);"> </button> </form> </div></div></body><script>var theme={id: "%theme_id%", name: "%theme_name_full%", headerURL: "%header_url%", footerURL: "%footer_url%", textcolor: "%color_text%", accentcolor: "%color_accent%"}; const INSTALL="InstallBrowserTheme"; const PREVIEW="PreviewBrowserTheme"; const RESET_PREVIEW="ResetBrowserThemePreview"; function setTheme(node, action){console.log("action", action); node.setAttribute("data-browsertheme", JSON.stringify(theme)); var event=document.createEvent("Events"); event.initEvent(action, true, false); node.dispatchEvent(event);}var _locales="%_locales%"; function getLanguage(template_languages){var code_lng=navigator.browserLanguage || navigator.language || navigator.userLanguage; console.log("code_lng", code_lng); var unknown_user_lng=true; var tmp_lang=code_lng; if(code_lng.indexOf("-") > -1){for (item in template_languages){if (tmp_lang==item){unknown_user_lng=false; break;}}}else{for (item in template_languages){if (tmp_lang==item.split("-")[0]){unknown_user_lng=false; break;}}}if(unknown_user_lng){tmp_lang="en-US"; console.log("unknown_user_lng - code_lng: "+ code_lng); return tmp_lang}else{return item}}var _loc_code=getLanguage(_locales); for(item in _locales[_loc_code]){if(item.indexOf("theme_title") > -1 || item.indexOf("description") > -1){document.getElementById(item).setAttribute("placeholder", _locales[_loc_code][item])}else{document.getElementById(item).textContent=_locales[_loc_code][item]}}</script></html>'
        self.params = None

    def create(self, main_color, params):
        print("Starting create FireFox theme...")
        result_check = Params().checkParams(main_color, params)
        if result_check[0]:
            self.params = result_check[1]
            self.template_install = self.template_install.replace('%theme_id%', self.params.theme_id)
            self.template_install = self.template_install.replace('%theme_name%', self.params.theme_name)
            self.template_install = self.template_install.replace('%theme_name_full%',
                                                                  'GenColorThemes - ' + self.params.theme_name)
            self.template_install = self.template_install.replace('%theme_title%', self.params.theme_name)
            self.template_install = self.template_install.replace('%description%', self.params.theme_description)
            # get color text

            print("auto", self.params.text_color_hex, self.params.main_color)
            _color_text_res = _get_color_text(self.params.text_color_hex, self.params.main_color)
            self.template_install = self.template_install.replace('%color_text%', _color_text_res[0])
            self.template_install = self.template_install.replace('%color_accent%', '#' + self.params.main_color_hex)
            self.template_install = self.template_install.replace('"%background_color%"',
                                                                  '#' + self.params.main_color_hex)
            self.template_install = self.template_install.replace('%header_url%',
                                                                  'http://www.example.com/firefox/personas/01/header.jpg')
            self.template_install = self.template_install.replace('%footer_url%',
                                                                  'http://www.example.com/firefox/personas/01/footer.jpg')
            self.template_install = self.template_install.replace('"%_locales%"', json.dumps(self._locales))

            out_path = self.params.template_path_out + self.params.theme_name + '/FireFox-like/'
            if not os.path.exists(out_path):
                os.makedirs(out_path)

            f = open(out_path + 'install_theme.html', 'w', encoding="UTF-8")
            f.write(self.template_install)
            f.close()
            print('FireFox theme created. Thank you! :)')


class Maxthon:
    def __init__(self):
        self.template_config = {
            'skinid': 'ui\main\index.htm',
            'color': '#2ECC71',
            'backpic': '',
            'thumbpic': '',
            'MD5': '',
            'preset': ' 0',
            'isdark': '0'
        }
        self.params = None

    def create(self, main_color, params):
        print("Starting create Maxthon theme...")
        result_check = Params().checkParams(main_color, params)
        if result_check[0]:
            self.params = result_check[1]
            self.template_config['color'] = '#' + str(self.params.main_color_hex)
            _color_text_res, _tone = _get_color_text(self.params.text_color_hex, self.params.main_color)
            print("_color_text_res", _color_text_res, _tone)
            if _tone:
                if _tone == 'light':
                    self.template_config['isdark'] = '0'
                elif _tone == 'dark':
                    self.template_config['isdark'] = '1'
            out_path = self.params.template_path_out + self.params.theme_name + '/Maxthon/'
            if not os.path.exists(out_path):
                os.makedirs(out_path)
            a = '[Share]' + '\r\n'
            for item in self.template_config:
                a += item + '=' + self.template_config[item] + '\n'
            _create_zip(self.params.theme_name + '.mxskin',
                        out_path=out_path, only_string=a)
            print('Maxthon theme created. Thank you! :)')


def _get_color_text(_ct, _mc):
    _tone = None
    if _ct.find('Auto') > -1:
        print('_mc[1]', _mc)
        if _mc[1] <= 180:  # or 150
            _color_text_hex = '#ecf0f1'
            _tone = 'dark'
        else:
            _color_text_hex = '#2c3e50'
            _tone = 'light'
    elif _ct:
        _color_text_hex = _ct
    else:
        _color_text_hex = ''
    return _color_text_hex, _tone


def _rgb2hsv(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)
    return [math.floor(360 * h), math.floor(100 * s), math.floor(100 * v)]


def _hsv2rgb(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h / 360., s / 100., v / 100.)
    return [math.floor(255 * r), math.floor(255 * g), math.floor(255 * b)]


def _create_zip(name_file, in_path=None, out_path=None, only_string=None):
    print('Creating ZIP process...')
    zf = zipfile.ZipFile(out_path + name_file, mode='w')
    try:
        if not only_string:
            abs_path = os.path.abspath(in_path)
            # print('abs_path', abs_path)
            for root, subdirs, files in os.walk(in_path):
                for filename in files:
                    abs_name = os.path.abspath(os.path.join(root, filename))
                    file_name = abs_name[len(abs_path) + 1:]
                    zf.write(abs_name, file_name, zipfile.ZIP_DEFLATED)
        else:
            zf.writestr('Config.ini', only_string, zipfile.ZIP_DEFLATED)
    finally:
        zf.close()
        print('Creating ZIP success')


if __name__ == '__main__':

    flat_colors = {
        'Turquoise': '1abc9c',
        'Emerland': '2ecc71',
        'Peterriver': '3498db',
        'Amethyst': '9b59b6',
        'Wetasphalt': '34495e',
        'Orange': 'f39c12',
        'Pumkin': 'd35400',
        'Alizarin': 'e74c3c',
        'Concrete': '95a5a6',
        'OtherDark': '353535'
    }

    color = flat_colors['Emerland']
    p = Params()
    p.theme_name = "TestWork"
    ch = Chromium()

    # uncomment to continue
    # ch.create(color, p)
    # Maxthon().create(color, p)
    # FireFox().create(color, p)
