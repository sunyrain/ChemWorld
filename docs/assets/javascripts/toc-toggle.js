(function () {
  var tocStorageKey = "chemworld.toc.collapsed";
  var sidebarStorageKey = "chemworld.sidebar.collapsed";

  function getStoredCollapsed(storageKey) {
    try {
      return window.localStorage.getItem(storageKey) === "1";
    } catch (error) {
      return false;
    }
  }

  function setStoredCollapsed(storageKey, value) {
    try {
      window.localStorage.setItem(storageKey, value ? "1" : "0");
    } catch (error) {
      return;
    }
  }

  function applyButtonState(target, button, collapsed, className, labels) {
    target.classList.toggle(className, collapsed);
    button.setAttribute("aria-expanded", collapsed ? "false" : "true");
    button.setAttribute("title", collapsed ? labels.expand : labels.collapse);
    button.setAttribute("aria-label", collapsed ? labels.expand : labels.collapse);
    button.textContent = collapsed ? "+" : "-";
  }

  function setupTocToggle() {
    var tocNavs = document.querySelectorAll("nav.md-nav--secondary");
    tocNavs.forEach(function (nav) {
      var title = nav.querySelector(".md-nav__title");
      var list = nav.querySelector("[data-md-component='toc']");

      if (!title || !list || nav.dataset.cwTocToggle === "ready") {
        return;
      }

      nav.dataset.cwTocToggle = "ready";
      title.classList.add("cw-toc-title");

      var button = document.createElement("button");
      button.type = "button";
      button.className = "cw-outline-toggle cw-toc-toggle";

      title.appendChild(button);

      applyButtonState(nav, button, getStoredCollapsed(tocStorageKey), "cw-toc-collapsed", {
        collapse: "收起目录",
        expand: "展开目录"
      });

      button.addEventListener("click", function (event) {
        event.preventDefault();
        event.stopPropagation();

        var collapsed = !nav.classList.contains("cw-toc-collapsed");
        setStoredCollapsed(tocStorageKey, collapsed);
        applyButtonState(nav, button, collapsed, "cw-toc-collapsed", {
          collapse: "收起目录",
          expand: "展开目录"
        });
      });
    });
  }

  function setupPrimarySidebarToggle() {
    var sidebars = document.querySelectorAll(".md-sidebar--primary");
    sidebars.forEach(function (sidebar) {
      var nav = sidebar.querySelector("nav.md-nav--primary");
      var title = sidebar.querySelector("nav.md-nav--primary > .md-nav__title");
      var list = sidebar.querySelector("nav.md-nav--primary > .md-nav__list");

      if (!nav || !title || !list || sidebar.dataset.cwSidebarToggle === "ready") {
        return;
      }

      sidebar.dataset.cwSidebarToggle = "ready";
      title.classList.add("cw-sidebar-title");

      var button = document.createElement("button");
      button.type = "button";
      button.className = "cw-outline-toggle cw-sidebar-toggle";

      title.appendChild(button);

      applyButtonState(sidebar, button, getStoredCollapsed(sidebarStorageKey), "cw-sidebar-collapsed", {
        collapse: "收起左侧导航",
        expand: "展开左侧导航"
      });

      button.addEventListener("click", function (event) {
        event.preventDefault();
        event.stopPropagation();

        var collapsed = !sidebar.classList.contains("cw-sidebar-collapsed");
        setStoredCollapsed(sidebarStorageKey, collapsed);
        applyButtonState(sidebar, button, collapsed, "cw-sidebar-collapsed", {
          collapse: "收起左侧导航",
          expand: "展开左侧导航"
        });
      });
    });
  }

  function setupChemWorldToggles() {
    setupTocToggle();
    setupPrimarySidebarToggle();
  }

  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(setupChemWorldToggles);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", setupChemWorldToggles);
  } else {
    setupChemWorldToggles();
  }
})();
