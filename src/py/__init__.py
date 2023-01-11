import re
from anki.utils import version_with_build
from aqt import mw, gui_hooks, QObject, QEvent, QShortcut, QKeySequence, QKeyCombination, qconnect, Qt

SHORTCUT = "Shortcut"

def strvercmp(left: str, right: str) -> int:
    """Compares semantic version strings.\n
    Returns:    left version is larger: >0
                right version is larger: <0
                versions are equal: 0"""
    import re
    pat = re.compile('^([0-9]+)\.?([0-9]+)?\.?([0-9]+)?([a-z]+)?([0-9]+)?$')
    l = pat.match(left).groups()
    r = pat.match(right).groups()
    for i in range(5):
        if l[i] != r[i]:
            if i == 3:
                return 1 if l[3] == None or (r[3] != None and l > r) else -1
            else:
                return 1 if r[i] == None or (l[i] != None and int(l[i]) > int(r[i])) else -1
    return 0


if tmp := re.match(r"^\s*((\d+\.)+\d+)", version_with_build()):
    ANKI_VER = tmp.group(1)
else:
    ANKI_VER = "2.1.0"

def close_sc(win, sc: str):
    win.keyPressEvent = lambda evt: super(win.__class__, win).keyPressEvent(evt)
    win.configure_window_close_shortcut = QShortcut(QKeySequence(sc), win)
    qconnect(win.configure_window_close_shortcut.activated, win.close)

# For < 2.1.56
class eat_escape_1(QObject):
    def eventFilter(self: object, obj: QObject, evt: QEvent):
        if evt.type() == QEvent.Type.ShortcutOverride and evt.keyCombination() == QKeyCombination(Qt.Key.Key_Escape):
            evt.accept()
            return True
        return False

# For ≥ 2.1.56
class eat_escape_2(QObject):
    escape = False
    def eventFilter(self: object, obj: QObject, evt: QEvent):
        if evt.type() == QEvent.Type.ShortcutOverride:
            if evt.keyCombination() == QKeyCombination(Qt.Key.Key_Escape):
                self.escape = True
                evt.accept()
                return True
            else:
                self.escape = False
                return False
        elif self.escape:
            if evt.type() == QEvent.Type.Close:
                self.escape = False
                evt.ignore()
                return True
        return False

CFG = mw.addonManager.getConfig(__name__)
if CFG.get(SHORTCUT, "escape").lower() != 'escape':
    gui_hooks.browser_menus_did_init.append(lambda win: close_sc(win, CFG[SHORTCUT]))
    gui_hooks.add_cards_did_init.append(lambda win: close_sc(win, CFG[SHORTCUT]))
    if strvercmp(ANKI_VER, "2.1.56") < 0:
        gui_hooks.editor_did_init.append(lambda ed: ed.parentWindow.installEventFilter(eat_escape_1(ed.parentWindow)))
    else:
        gui_hooks.editor_did_init.append(lambda ed: ed.parentWindow.installEventFilter(eat_escape_2(ed.parentWindow)))
