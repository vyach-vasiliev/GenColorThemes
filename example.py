import GenColorThemes.gen as gct

if __name__ == "__main__":
    color = '#27ae60'
    p = gct.Params()
    p.theme_name = "Test theme"
    p.theme_description = "Test description"
    ch = gct.Chromium()

    ch.create_theme(color, p)
    # or
    # gct.Chromium().create_theme(color, p)

    ''' Or short variant '''
    # gct.FireFox().create_theme(color, p)
    # gct.Maxthon().create_theme(color, p)
    # gct.FireFox().create_theme(color, p)
    # gct.OperaBlink().create_theme(color, p)
    # gct.OperaPresto().create_theme(color, p)
    # gct.Slim().create_theme(color, p)