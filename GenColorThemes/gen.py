#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess, colorsys, zipfile, struct, random, math, json, sys, os, configparser
from PIL import Image


class Help:
    version = "0.2.4"
    name = "GenColorThemes"
    url = "http://github.com/vyach-vasiliev/GenColorThemes"


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
            # params.main_color = struct.unpack('BBB', bytes.fromhex(params.main_color))
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
        self.files_params = [
            ['theme_frame.png', 1, 50],
            ['theme_tab_background.png', 1, 30],
            ['theme_toolbar.png', 1, 120],
        ]

    def create_theme(self, main_color, params):
        print("-"*50)
        print("Starting create Chromium theme...")
        result_check = Params().checkParams(main_color, params)
        if result_check[0]:
            self.params = result_check[1]
            if len(self.params.theme_name) > 0:
                self.template_manifest['name'] = self.template_manifest['name'] + '_' + params.theme_name
                # params.theme_name = '/' + self.template_manifest['name']
            if len(self.params.theme_description) > 0:
                self.template_manifest['description'] = self.params.theme_description

            # Set all directories
            out_path = self.params.template_path_out + '/' + self.params.theme_name + '/Chromium-like/'
            out_path_folder_theme = out_path + 'resources/'
            out_path_folder_theme_images = out_path_folder_theme + 'images/'
            out_path_folder_theme_locales = out_path_folder_theme + '_locales/'

            if not os.path.exists(out_path_folder_theme): os.makedirs(out_path_folder_theme)

            if isinstance(self.params.main_color, str):
                general_color_rgb = _hex2rgb(self.params.main_color)
            else:
                general_color_rgb = self.params.main_color
            self._gen_colors(general_color_rgb)
            print('+++ out_path', out_path)
            self._create_manifest(out_path)

            if not os.path.exists(out_path_folder_theme_images): os.makedirs(out_path_folder_theme_images)
            _create_images(self.params.main_color, self.files_params, out_path_folder_theme)

            self._create_locales(self.template_locale, out_path_folder_theme_locales)
            self._create_crx(out_path)
            if self.zip:
                _create_zip(self.params.theme_name + '.zip',
                    out_path + 'resources/',
                    out_path
                )

        print('Chromium theme created. Thank you! :)')
        print("-"*50)

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

    def _create_manifest(self, out_path):
        self.template_manifest_json = json.dumps(self.template_manifest, sort_keys=True)

        f = open(out_path + '/resources/manifest.json', 'w')
        f.write(self.template_manifest_json)
        f.close()
        print('Create manifest.json success.')

    def _create_locales(self, tmp_locale, out_path_folder_theme_locales):
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

        if not os.path.exists(out_path_folder_theme_locales):
            os.makedirs(out_path_folder_theme_locales)
        for item in tmp_locale:
            if len(tmp_locale[item][0]) == 0 or len(tmp_locale[item][1]) == 0:
                print('\tPasses locale [' + item + ']. Is empty.')
                continue
            template_messages['appName']['message'] = tmp_locale[item][0]
            template_messages['appDesc']['message'] = tmp_locale[item][1]
            template_messages_json = json.dumps(template_messages, sort_keys=True)

            if not os.path.exists(out_path_folder_theme_locales + item):
                os.makedirs(out_path_folder_theme_locales + item)

            f = open(out_path_folder_theme_locales + item + '/messages.json', 'w')
            f.write(template_messages_json)
            f.close()
            print('\tCreate locale [' + item + '] success.')
        print('Create locales files success.')

    def _create_crx(self, out_path):
        print('Creating .CRX process...')
        abs_path = os.path.abspath(out_path + '/resources/')
        abs_path = abs_path.replace('\\', '/') + '/'
        appdata = os.getenv('APPDATA')
        appdata = appdata.split('\\')
        appdata = appdata[:len(appdata) - 1]
        appdata = '\\'.join(appdata)

        if self.browser_path:
            folder_chrome = self.browser_path
            if not os.path.exists(folder_chrome):
                try:
                    raise FileNotFoundError("Folder not found: ", folder_chrome)
                except:
                    raise os.error('Error: check browser path', folder_chrome)
        else:
            folder_chrome = appdata + '/Local/Google/Chrome/Application'
            if not os.path.exists(folder_chrome):
                folder_chrome = appdata + '/Local/Google/Chrome SxS/Application'
            else:
                try:
                    raise FileNotFoundError('Folder Chrome-browser not found. Please select your directory.')
                except:
                    raise os.error('Error: check browser path', folder_chrome)
        try:
            commad_line = '"' + folder_chrome + '/chrome" --pack-extension="' + abs_path + '" --no-message-box'
            retcode = subprocess.call(commad_line, shell=True)
        except OSError as e:
            print(sys.stderr, "\tExecution failed:", e)
        finally:
            old_file_crx = out_path + self.params.theme_name + '.crx'
            old_file_pem = out_path + self.params.theme_name + '.pem'
            if os.path.exists(old_file_crx):
                os.remove(old_file_crx)
            if os.path.exists(old_file_pem):
                os.remove(old_file_pem)

            new_file_crx = out_path + '/resources.crx'
            new_file_pem = out_path + '/resources.pem'
            created_crx_ok, created_pem_ok = False, False
            if os.path.exists(new_file_crx):
                os.rename(out_path + 'resources.crx',
                    out_path + self.params.theme_name + '.crx')
                created_crx_ok = True
            else: print('Ops. Not found "resources.crx" file. Try another Python version.')
            if os.path.exists(new_file_pem):
                os.rename(out_path + '/resources.pem',
                    out_path + self.params.theme_name + '.pem')
                created_pem_ok = True
            else: print('Ops. Not found "resources.pem" file. Try another Python version.')
            if created_crx_ok and created_pem_ok: print('Creating .CRX and .PEM files success')
            else: print('Creating .CRX or .PEM files failed. Sorry. Please, try again!')


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

    def create_theme(self, main_color, params):
        print("-"*50)
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

            main_rgb = _hex2rgb(self.params.main_color)
            _color_text_res = _get_color_text(self.params.text_color_hex, main_rgb)
            self.template_install = self.template_install.replace('%color_text%', _color_text_res[0])
            self.template_install = self.template_install.replace('%color_accent%', '#' + self.params.main_color_hex)
            self.template_install = self.template_install.replace('"%background_color%"',
                                                                  '#' + self.params.main_color_hex)
            self.template_install = self.template_install.replace('%header_url%',
                                                                  'http://www.example.com/firefox/personas/01/header.jpg')
            self.template_install = self.template_install.replace('%footer_url%',
                                                                  'http://www.example.com/firefox/personas/01/footer.jpg')
            self.template_install = self.template_install.replace('"%_locales%"', json.dumps(self._locales))

            out_path = self.params.template_path_out + '/' + self.params.theme_name + '/FireFox-like/'
            if not os.path.exists(out_path):
                os.makedirs(out_path)

            f = open(out_path + 'install_theme.html', 'w', encoding="UTF-8")
            f.write(self.template_install)
            f.close()
            print('FireFox theme created. Thank you! :)')
            print("-"*50)


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

    def create_theme(self, main_color, params):
        print("-"*50)
        print("Starting create Maxthon theme...")
        result_check = Params().checkParams(main_color, params)
        if result_check[0]:
            self.params = result_check[1]
            self.template_config['color'] = '#' + str(self.params.main_color_hex)
            main_rgb = _hex2rgb(self.params.main_color)
            print('self.params.main_color', main_rgb)
            _color_text_res, _tone = _get_color_text(self.params.text_color_hex, main_rgb)
            print("_color_text_res", _color_text_res, _tone)
            if _tone:
                if _tone == 'light':
                    self.template_config['isdark'] = '0'
                elif _tone == 'dark':
                    self.template_config['isdark'] = '1'

            # out_path = self.params.template_path_out + self.params.theme_name + '/Maxthon/'
            out_path = self.params.template_path_out + '/' + self.params.theme_name + '/Maxthon/'
            out_path_folder_theme = out_path + self.params.theme_name
            if not os.path.exists(out_path):
                os.makedirs(out_path)

            a = '[Share]' + '\r\n'
            for item in self.template_config:
                a += item + '=' + self.template_config[item] + '\n'
            _create_zip(self.params.theme_name + '.mxskin',
                        out_path=out_path, only_string=a)
            print('Maxthon theme created. Thank you! :)')
            print("-"*50)

class OperaBlink:
    def __init__(self):
        self.persona_config = {
            'Info': {
                'name': '',
                'author': 'GenColorTheme',
                'version': '2', # for themes Opera v18+
            },
            'Start Page': {
                'background': '',
                'position': 'center bottom',
            },
            'Web UI Pages': {
                'background': '',
                'position': 'center bottom'
            }
        }
        self.meta_config = {
            'Metadata': {
                'Catalog URL': Help().url
            }
        }
        self.params = None
        self.files_params = [
            ['theme_backgrond.png', 50, 50],
        ]

    def create_theme(self, main_color, params):
        print("-"*50)
        print("Starting create OperaBlink theme...")
        result_check = Params().checkParams(main_color, params)
        if result_check[0]:
            self.params = result_check[1]
            if self.params.theme_name:
                self.persona_config['Info']['name'] = self.params.theme_name
            else:
                self.persona_config['Info']['name'] = self.params.theme_id

            self.persona_config['Start Page']['background'] = 'theme_backgrond.png'
            self.persona_config['Web UI Pages']['background'] = 'theme_backgrond.png'

            out_path = self.params.template_path_out + '/' + self.params.theme_name + '/Opera-Blink/'
            out_path_folder_theme = out_path + self.params.theme_name

            if not os.path.exists(out_path_folder_theme):
                os.makedirs(out_path_folder_theme)

            _create_images(self.params.main_color, self.files_params, out_path_folder_theme)

            config = configparser.ConfigParser()
            for item in self.persona_config:
                config[item] = self.persona_config[item]
            with open(out_path_folder_theme+'/persona.ini', 'w+') as configfile:
                config.write(configfile)
            config.clear()

            for item in self.meta_config:
                config[item] = self.meta_config[item]
            with open(out_path_folder_theme+'/opera.ini', 'w+') as configfile:
                config.write(configfile)


            _create_zip(self.params.theme_name + '.zip',
                        out_path=out_path, in_path=out_path_folder_theme)
            print('OperaBlink theme created. Thank you! :)')
            print("-"*50)


class OperaPresto:
    def __init__(self):
        self.persona_config = {
            'Info': {
                'name': '',
                'author': 'GenColorTheme',
                'version': '1', # for themes Opera < 18 version
            },
            # uncomment for edit
            # 'Options': {
            #     'Tint Color': '#3e6da9',
            #     'Colorize Color': '#3e6da9',
            # },
            'Window Image': {
                'Type': 'BestFit', # BestFit or BoxTile
                'Background': ''
            },
            'Clear elements': {
                'Speed Dial Widget Blank Skin': '1', # BestFit or BoxTile
                'Speed Dial Widget Skin': '1'
            }
        }
        self.meta_config = {
            'Metadata': {
                'Catalog URL': Help().url
            }
        }
        self.params = None
        self.files_params = [
            ['theme_backgrond.bmp', 50, 50],
        ]

    def create_theme(self, main_color, params):
        print("-"*50)
        print("Starting create OperaPresto theme...")
        result_check = Params().checkParams(main_color, params)
        if result_check[0]:
            self.params = result_check[1]
            if self.params.theme_name:
                self.persona_config['Info']['name'] = self.params.theme_name
            else:
                self.persona_config['Info']['name'] = self.params.theme_id

            self.persona_config['Window Image']['Background'] = 'theme_backgrond.png'

            out_path = self.params.template_path_out + '/' + self.params.theme_name + '/Opera-Presto/'
            out_path_folder_theme = out_path + self.params.theme_name

            if not os.path.exists(out_path_folder_theme):
                os.makedirs(out_path_folder_theme)

            _create_images(self.params.main_color, self.files_params, out_path_folder_theme)

            config = configparser.ConfigParser()
            for item in self.persona_config:
                config[item] = self.persona_config[item]
            with open(out_path_folder_theme+'/persona.ini', 'w+') as configfile:
                config.write(configfile)
            config.clear()

            for item in self.meta_config:
                config[item] = self.meta_config[item]
            with open(out_path_folder_theme+'/opera.ini', 'w+') as configfile:
                config.write(configfile)


            _create_zip(self.params.theme_name + '.zip',
                        out_path=out_path, in_path=out_path_folder_theme)
            print('OperaPresto theme created. Thank you! :)')
            print("-" * 50)

class Slim:
    def __init__(self):
        # documentation: https://www.slimbrowser.net/en/webhelp/skin.htm
        self.persona_config = {
            'general': {
                'Name': '',
                'Author': 'GenColorTheme',
                'CapTextColor': '',        # Specify the caption text color by RGB value.
                # 'CapRect': '18,5,-200,25', # left, top, right, bottom (If you don't use sys.bmp)
                'CapRect': '39,5,-200,25', # left, top, right, bottom (If you use sys.bmp)
                'SysPos': '10,5',           # left, top (If you use sys.bmp)
                'TabSelTextColor': '',     # text color of the selected tab on tab bar
                'TabTextColor': '',        # text color of unselected tabs on tab bar.
                'MenuTextColor': '',       # Specify the menu text color by RGB value.
                'StatusBarBackColor': '',  # Specify the back ground color of the status bar by RGB value.
                # 'SystemIcon': 'true',      # This option has a default value of true. If you want to use sys.bmp as the image for the system button, you should specify: SystemIcon=false.
            },
        }
        # would be as height in top.bmp
        self.params = None

        ''' Rule files params: [<file name>, <width>, <height> ]
            example:  ['background.png', 12, 220] -> drawing point -> output file: background.png, width: 12px; height: 220px
        '''
        self.files_params = [
            ['barback.bmp', 6, 220],
            ['bottom.bmp', 198, 8],
            ['bottomleft.bmp', 123, 8],
            ['bottomright.bmp', 123, 8],
            ['expbarback.bmp', 16, 16],
            ['left.bmp', 8, 72],
            ['lefttop.bmp', 8, 96],
            ['leftbottom.bmp', 8, 96],
            ['right.bmp', 8, 72],
            ['righttop.bmp', 8, 72],
            ['rightbottom.bmp', 8, 96],
            ['top.bmp', 205, 25],
            ['topleft.bmp', 128, 50],
            ['topright.bmp', 128, 50],
        ]

        ''' Rule bits map: [ [<width start>, <width end>], [<height start>, <height end>] ]
            example:  [ [10, 12], [14, 15] ] -> drawing point -> w: 10, 11, 12; h: 14, 15
        '''
        self.square_map = [
            [[7, 8], [7, 12]],  # left
            [[7, 15], [7, 8]],  # top
            [[14, 15], [7, 12]],  # right
            [[7, 15], [13, 14]],  # bottom
        ]

        self.sys_map = [
            [[7, 7], [5, 9]],  # left
            [[8, 9], [4, 10]],  # left 2
            [[10, 12], [2, 2]],  # top x3
            [[9, 13], [3, 3]],  # top x5
            [[15, 15], [5, 9]],  # right
            [[13, 14], [4, 10]],  # right 2
            [[10, 12], [4, 8]],  # center
            # [[10, 12], [9, 10]], # center bottom 2 (uncomment to close hole in center)
            [[8, 14], [11, 11]],  # bottom
            [[9, 13], [12, 12]],  # bottom 1
            [[9, 13], [13, 13]],  # bottom 2
            [[9, 13], [14, 14]],  # bottom 3
            [[10, 12], [15, 15]],  # bottom 4
            [[10, 12], [17, 17]],  # bottom 5
            [[10, 12], [18, 18]],  # bottom empty 1
            [[10, 12], [19, 19]],  # bottom 6
            [[10, 12], [20, 20]],  # bottom 7
            [[8, 8], [10, 10]],  # dot bottom left
            [[14, 14], [10, 10]],  # dot bottom right

        ]

        self.cross_map = [
            # left down line (starting from the upper border)
            [[5, 5], [6, 6]],
            [[6, 6], [7, 7]],
            [[7, 7], [8, 8]],
            [[8, 8], [9, 9]],
            [[9, 9], [10, 10]],
            [[10, 10], [11, 11]],
            [[11, 11], [12, 12]],
            [[12, 12], [13, 13]],
            [[13, 13], [14, 14]],
            [[14, 14], [15, 15]],
            [[15, 15], [16, 16]],
            [[16, 16], [17, 17]],

            # left up line (starting from the upper border)
            [[7, 7], [4, 4]],
            [[8, 8], [5, 5]],
            [[9, 9], [6, 6]],
            [[10, 10], [7, 7]],
            [[11, 11], [8, 8]],
            [[12, 12], [9, 9]],
            [[13, 13], [10, 10]],
            [[14, 14], [11, 11]],
            [[15, 15], [12, 12]],
            [[16, 16], [13, 13]],
            [[17, 17], [14, 14]],
            [[18, 18], [15, 15]],

            # right down line (starting from the upper border)
            [[18, 18], [6, 6]],
            [[17, 17], [7, 7]],
            [[16, 16], [8, 8]],
            [[15, 15], [9, 9]],
            [[14, 14], [10, 10]],
            [[13, 13], [11, 11]],
            [[12, 12], [12, 12]],
            [[11, 11], [13, 13]],
            [[10, 10], [14, 14]],
            [[9, 9], [15, 15]],
            [[8, 8], [16, 16]],
            [[7, 7], [17, 17]],

            # right up line (starting from the upper border)
            [[16, 16], [4, 4]],
            [[15, 15], [5, 5]],
            [[14, 14], [6, 6]],
            [[13, 13], [7, 7]],
            [[12, 12], [8, 8]],
            [[11, 11], [9, 9]],
            [[10, 10], [10, 10]],
            [[9, 9], [11, 11]],
            [[8, 8], [12, 12]],
            [[7, 7], [13, 13]],
            [[6, 6], [14, 14]],
            [[5, 5], [15, 15]],

            # just dot
            [[6, 6], [5, 5]],  # tom left
            [[17, 17], [5, 5]],  # top right
            [[6, 6], [16, 16]],  # bottom left
            [[17, 17], [16, 16]],  # bottom right
        ]

        self.line_map = [
            [[7, 17], [9, 10]],  # left
        ]


    def create_theme(self, main_color, params):
        print("-"*50)
        print("Starting create Slim  theme...")
        result_check = Params().checkParams(main_color, params)
        if result_check[0]:
            self.params = result_check[1]
            if self.params.theme_name:
                self.persona_config['general']['Name'] = self.params.theme_name
            else:
                self.persona_config['general']['Name'] = self.params.theme_id

            self.persona_config['general']['CapTextColor'] = '255,255,255'
            self.persona_config['general']['MenuTextColor'] = '0,0,0'
            self.persona_config['general']['TabTextColor'] = '255,255,255'
            self.persona_config['general']['StatusBarBackColor'] = '255,255,255'

            out_path = self.params.template_path_out + '/' + self.params.theme_name + '/Slim/'
            out_path_folder_theme = out_path + self.params.theme_name + '/'

            if not os.path.exists(out_path_folder_theme):
                os.makedirs(out_path_folder_theme)

            self.files_params_bm = {
                # mask state: 1- visible, 2- hover, 3-keydown, 4- keyup
                'max.bmp': [
                    [self.square_map, (21, 21), main_color, (0, 0, 0)],
                    [self.square_map, (21, 21), main_color, (255, 255, 255)],
                    [self.square_map, (21, 21), main_color, (0, 0, 0)],
                    [self.square_map, (21, 21), main_color, (0, 0, 0)]
                ],
                'min.bmp': [
                    [self.line_map, (21, 21), main_color, (0, 0, 0)],
                    [self.line_map, (21, 21), main_color, (255, 255, 255)],
                    [self.line_map, (21, 21), main_color, (0, 0, 0)],
                    [self.line_map, (21, 21), main_color, (0, 0, 0)]
                ],
                'close.bmp': [
                    [self.cross_map, (21, 21), main_color, (0, 0, 0)],
                    [self.cross_map, (21, 21), main_color, (255, 255, 255)],
                    [self.cross_map, (21, 21), main_color, (0, 0, 0)],
                    [self.cross_map, (21, 21), main_color, (0, 0, 0)]
                ],
                'sys.bmp': [
                    [self.sys_map, (21, 21), main_color, (0, 0, 0)],
                    [self.sys_map, (21, 21), main_color, (255, 255, 255)],
                    [self.sys_map, (21, 21), main_color, (0, 0, 0)],
                    [self.sys_map, (21, 21), main_color, (0, 0, 0)]
                ]
            }

            _create_images(self.params.main_color, self.files_params, out_path_folder_theme)
            _create_images(self.params.main_color, self.files_params_bm, out_path_folder_theme, is_bits_map=True)

            config = configparser.ConfigParser()
            for item in self.persona_config:
                config[item] = self.persona_config[item]
            with open(out_path_folder_theme+'/skin.ini', 'w+') as configfile:
                config.write(configfile)
            config.clear()

            _create_zip(self.params.theme_name + '.zip',
                        out_path=out_path, in_path=out_path_folder_theme)
            print('Slim theme created. Thank you! :)')
            print("-" * 50)


def _create_images(main_color, files_params, out_path_images, is_bits_map=False):
    ''' Rule files params: [<file name>, <width>, <height> ]
        example:  ['background.png', 12, 220] -> drawing point -> output file: background.png, width: 12px; height: 220px

        or for generate image:
        [<bits map>, (<width>, <height>), <background color>, <point color>]

        Rule <bits map>: [ [<width start>, <width end>], [<height start>, <height end>] ]
        example:  [ [10, 12], [14, 15] ] -> drawing point -> w: 10, 11, 12; h: 14, 15
    '''
    def _generate_image(figure_lines, wh, background_color=(255, 255, 255), point_color=(0, 0, 0)):
        '''

        :param figure_lines: As files params or as bits map
        :param background_color: As tuple. list or string - (255, 255, 255), '123fff', '#123fff'
        :param point_color: As tuple. list or string - (255, 255, 255), '123fff', '#123fff'
        :return: True
        '''
        w, h = wh
        img = Image.new('RGB', (w, h), background_color)
        pixels = img.load()  # create the pixel map
        for item in figure_lines:
            ws, hs = item
            ws_start = ws[0] - 1
            ws_end = ws[1]
            # if ws[0] == ws[1]:
            #     ws_end = ws[1]+1
            hs_start = hs[0] - 1
            hs_end = hs[1]
            # if hs[0] == hs[1]:
            #     hs_end = hs[1]+1
            for w in range(ws_start, ws_end):
                for h in range(hs_start, hs_end):
                    pixels[w, h] = point_color
        return img

    if not '#' in main_color:
        main_color = '#' + main_color

    if not is_bits_map:
        for item in files_params:
            file_name, w, h = item
            # print item
            img = Image.new('RGB', (w, h), main_color)
            img.save(out_path_images + file_name)
    else:
        for img_name in files_params:
            x_offset = 0
            new_im = Image.new('RGB', (84, 21))

            # print img_name
            for im in files_params[img_name]:
                bits_map, size, bk_color, pt_color = im
                if not '#' in bk_color and not isinstance(bk_color, list) and not isinstance(bk_color, tuple):
                    bk_color = '#' + bk_color
                if not '#' in bk_color and not isinstance(pt_color, list) and not isinstance(pt_color, tuple):
                    pt_color = '#' + pt_color
                im_gen = _generate_image(bits_map, size, bk_color, pt_color)
                new_im.paste(im_gen, (x_offset, 0))
                x_offset += im_gen.size[0]
            new_im.save(out_path_images + img_name)

    print('Create images success')
    return True

def _get_color_text(_ct, _mc):
    _tone = None
    if _ct.find('Auto') > -1:
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

def _hex2rgb(hex):
    hex = hex.lstrip('#')
    hlen = len(hex)
    return tuple(int(hex[i:i + hlen // 3], 16) for i in range(0, hlen, hlen // 3))

def _rgb2hex(rgb):
    return "#{0:02x}{1:02x}{2:02x}".format(rgb(0), rgb(1), rgb(2))

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

    ''' Color library of your choice '''
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

    # color = flat_colors['Emerland']
    # color = flat_colors['Pumkin']
    # color = 'cc2eb1'
    color = 'ff822e'
    p = Params()
    p.theme_name = "TestWork"
    ch = Chromium()

    ''' Uncomment to continue creating '''
    # ch.create_theme(color, p)

    ''' Or short variant '''
    # Maxthon().create_theme(color, p)
    # Chromium().create_theme(color, p)
    # FireFox().create_theme(color, p)
    # OperaBlink().create_theme(color, p)
    # OperaPresto().create_theme(color, p)
    # Slim().create_theme(color, p)
