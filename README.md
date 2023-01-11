# Window close shortcut

Allows customization of the shortcut (which defaults to escape) to close the browser and add notes windows. Set shortcut in addon configuration (default Shift+Escape).

Note that this installs an event filter on WebEngineView that discards the default Escape shortcut. This in turn results in Escape key press events now reaching the WebEngineView (i.e. it is possible to add eventListeners for Escape in JS).

## Changelog

- 2023-01-11 Support 2.1.56 browser/add windows (2.1.56 changed the window base class from QDialog to QMainWindow)
