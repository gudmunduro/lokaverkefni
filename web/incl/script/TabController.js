

var TabController = {

    currentTabIndex: 1,

    changeToTabIndex: 0,

    tabChanegTimer: null,

    getTabById: function (id) {
        return document.getElementById("tab" + id);
    },

    set currentTab(index) {
        if (index == TabController.currentTabIndex) return;
        if (TabController.tabChanegTimer != null) {
            return
        }
        TabController.getTabById(index).style.transform = "translateX(" + ((index > TabController.currentTabIndex) ? "100" : "-100") + "vw)";
        TabController.getTabById(index).style.display = "block";
        setTimeout(function () {
            TabController.getTabById(TabController.currentTabIndex).style.transform = "translateX(" + ((index > TabController.currentTabIndex) ? "-100" : "100") + "vw)";
            TabController.getTabById(index).style.transform = "translateX(0vw)";
            TabController.tabChanegTimer = setTimeout(function () {
                TabController.getTabById(TabController.currentTabIndex).style.display = "none";
                TabController.currentTabIndex = index;
                TabController.tabChanegTimer = null
            }, 300)
        }, 50)
    }
}