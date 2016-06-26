import GenColorThemes.gen as gct

if __name__ == "__main__":
    color = '#27ae60'
    p = gct.Params()
    p.theme_name = "Test theme"
    p.theme_description = "Test description"
    ch = gct.Chromium()
    ch.create(color, p)
    gct.FireFox().create(color, p)
    gct.Maxthon().create(color, p)