# Deck icons, add icons to the deck window in Anki
# Copyright (C) 2025  Léo Picat

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import *
# import hooks
from aqt import gui_hooks
# import aqt to access the function to add css files
import aqt
# import BeautifulSoup to manipulate html
import bs4 as bs
# to load css
from typing import Any, Optional

# give access permission
mw.addonManager.setWebExports(__name__, r'.+\.(css|png)')
addon_package = mw.addonManager.addonFromModule(__name__)
# base_url for deck icons
base_url_deckIcons = f'/_addons/{addon_package}/user_files'
# base_url for css files
base_url_css = f'/_addons/{addon_package}/deck_icons.css'

# load css
def addCss(web_content: aqt.webview.WebContent, context: Optional[Any]) -> None:
     if isinstance(context, aqt.deckbrowser.DeckBrowser):
         web_content.css.append(base_url_css)

gui_hooks.webview_will_set_content.append(addCss)


# add icons, correct tree size
def addDeckIcons(deck_browser, content) -> None:
    
    # get content tree and convert it to a manipulable class
    contentSoup = bs.BeautifulSoup(content.tree, features="html.parser")
    
    ## ADD ICONS ##
    # extract the part related to decks' names
    DecksHTML = contentSoup.find_all("a", class_="deck")
    # extract decks' names
    DecksNames = [i.contents[0] for i in DecksHTML]
    
    i=0
    for deck in contentSoup.find_all("td", class_="decktd"):
        # create the icon adress
        iconAdress = "{}/{}.png".format(base_url_deckIcons, DecksNames[i])
        defaultIconAdress = "{}/../default.png".format(base_url_deckIcons)

        # create a new cell to add next to the deck name
        newCell = contentSoup.new_tag("td")
        # create a tag for the icon to insert in the new cell
        newIcon = contentSoup.new_tag("img", src=iconAdress, **{'class':'deckIcons', 'onerror': 'this.onerror=null; this.src="'+ defaultIconAdress +'"'})
        # add the icon in the new cell
        newCell.append(newIcon)
        # insert the new cell before the deck name
        deck.insert_before(newCell)
        i += 1
    
    ## FIX COLSPAN ##
    # because we had a cell for the icon, the header is not sized properly
    # extract header row and the cell in which the colspan is specified
    header = contentSoup.find_all("tr")[0].find_all("th")[0]
    header.attrs["colspan"] = "6"
    
    # replace the content.tree with the modified content.tree
    content.tree = str(contentSoup)

gui_hooks.deck_browser_will_render_content.append(addDeckIcons)
    
