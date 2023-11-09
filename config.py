
globalConfig = {
    'mancera': 'MAN9209143V1',
    'title': 'PRO FUT',
    'description': 'Inventario para profut',
    'footerLeft': '',
    'footerRight': '',
    'home': 'portal_view.mainView'
}

pageConfig = {
    'title': 'PAGE_TITLE',
    'subtitle': 'PAGE_SUBTITLE',
    'detail': "Additional Detail",
    'description': "PAGE_DESCRIPTION_FOR THIS_CONTEXT"
}

flashMessages = [
    ("danger", "Mensaje Danger"),
    ("warning", "Mensaje Warning"),
    ("success", "Mensaje Success"),
    ("info", "Mensaje Info"),
]


def getSessionDefaults(session):
    customer = "SANDOR RODAS"
    sidebar = True  # customer != None

    return customer, sidebar
