from aqt import mw, gui_hooks, QObject, QEvent, QShortcut, QKeySequence, QKeyCombination, qconnect, Qt

SHORTCUT = "Shortcut"

def close_sc(win, sc: str):
    win.keyPressEvent = lambda evt: super(win.__class__, win).keyPressEvent(evt)
    win.configure_window_close_shortcut = QShortcut(QKeySequence(sc), win)
    qconnect(win.configure_window_close_shortcut.activated, win.close)

class eat_escape(QObject):
    def eventFilter(self: object, obj: QObject, evt: QEvent):
        if evt.type() == QEvent.Type.ShortcutOverride and evt.keyCombination() == QKeyCombination(Qt.Key.Key_Escape):
            evt.accept()
            return True
        return False

CFG = mw.addonManager.getConfig(__name__)
if CFG[SHORTCUT].lower() != 'escape':
    gui_hooks.browser_menus_did_init.append(lambda win: close_sc(win, CFG[SHORTCUT]))
    gui_hooks.add_cards_did_init.append(lambda win: close_sc(win, CFG[SHORTCUT]))
    gui_hooks.editor_did_init.append(lambda ed: ed.parentWindow.installEventFilter(eat_escape(ed.parentWindow)))
