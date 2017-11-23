

var TabController = {

    currentTabIndex: 1,

    getTabById: function (id) {
        return document.getElementById("tab" + id);
    },

    set currentTab(index) {
        if (index == TabController.currentTabIndex) return;
        TabController.getTabById(index).style.transform = "translateX(" + ((index > TabController.currentTabIndex) ? "100" : "-100") + "vw)";
        TabController.getTabById(index).style.display = "block";
        setTimeout(function () {
            TabController.getTabById(TabController.currentTabIndex).style.transform = "translateX(" + ((index > TabController.currentTabIndex) ? "-100" : "100") + "vw)";
            TabController.getTabById(index).style.transform = "translateX(0vw)";
            setTimeout(function () {
                TabController.getTabById(TabController.currentTabIndex).style.display = "none";
                TabController.currentTabIndex = index;
            }, 300)
        }, 50)
    }
}