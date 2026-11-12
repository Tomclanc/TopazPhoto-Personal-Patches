import QtQuick
import WonderUI

Item {
    id: controller
    objectName: "TopazMicaController"
    visible: false
    required property var targetWindow
    required property var agent
    required property var titleItem
    property bool ready: false
    property bool micaEnabled: false
    property bool dark: WonderStyle.darkMode
    property var decoratedWelcome: null

    onDarkChanged: if (ready) agent.setWindowAttribute("dark-mode", dark)

    function findWelcome(item) {
        if (!item) return null;
        if (typeof item.browseImages === "function" && typeof item.openSampleImage === "function"
                && typeof item.openRecentFile === "function") return item;
        if (item.children) {
            for (var i = 0; i < item.children.length; ++i) {
                var result = findWelcome(item.children[i]);
                if (result) return result;
            }
        }
        return null;
    }

    function clearPageBackgrounds(item) {
        if (!item) return;
        if (item.color !== undefined && Qt.colorEqual(item.color, WonderStyle.color.pageBkg))
            item.color = "transparent";
        if (item.children) for (var i = 0; i < item.children.length; ++i)
            clearPageBackgrounds(item.children[i]);
    }

    function decorateWelcome() {
        if (!micaEnabled) return;
        var welcome = findWelcome(targetWindow.contentItem);
        if (welcome && welcome !== decoratedWelcome && welcome.children.length > 0) {
            // Only the welcome drop zone; photo previews and edit panels keep their original colors.
            clearPageBackgrounds(welcome.children[0]);
            decoratedWelcome = welcome;
        }
    }

    function initialize() {
        micaEnabled = agent.setWindowAttribute("mica", true);
        agent.setWindowAttribute("dark-mode", dark);
        ready = true;
        if (micaEnabled) {
            targetWindow.color = "transparent";
            targetWindow.background = null;
            titleItem.color = "transparent";
            decorateWelcome();
        } else {
            targetWindow.color = Qt.binding(function() { return WonderStyle.color.pageBkg; });
        }
        console.log("Topaz Mica controller:", micaEnabled, "dark:", dark);
    }
    Component.onCompleted: Qt.callLater(initialize)
    Timer { interval: 1200; repeat: true; running: controller.micaEnabled; onTriggered: controller.decorateWelcome() }
}
