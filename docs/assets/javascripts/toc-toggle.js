(function () {
  var storageKey = "chemworld.toc.collapsed";

  function getStoredCollapsed() {
    try {
      return window.localStorage.getItem(storageKey) === "1";
    } catch (error) {
      return false;
    }
  }

  function setStoredCollapsed(value) {
    try {
      window.localStorage.setItem(storageKey, value ? "1" : "0");
    } catch (error) {
      return;
    }
  }

  function applyState(nav, button, collapsed) {
    nav.classList.toggle("cw-toc-collapsed", collapsed);
    button.setAttribute("aria-expanded", collapsed ? "false" : "true");
    button.setAttribute("title", collapsed ? "展开目录" : "收起目录");
    button.setAttribute("aria-label", collapsed ? "展开目录" : "收起目录");
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
      button.className = "cw-toc-toggle";

      title.appendChild(button);

      applyState(nav, button, getStoredCollapsed());

      button.addEventListener("click", function (event) {
        event.preventDefault();
        event.stopPropagation();

        var collapsed = !nav.classList.contains("cw-toc-collapsed");
        setStoredCollapsed(collapsed);
        applyState(nav, button, collapsed);
      });
    });
  }

  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(setupTocToggle);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", setupTocToggle);
  } else {
    setupTocToggle();
  }
})();
