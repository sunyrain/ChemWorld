(function () {
  var tocStorageKey = "chemworld.toc.collapsed.v2";
  var primaryNavStorageKey = "chemworld.primaryNav.open.v1";

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

  function readStoredOpenSections() {
    try {
      var raw = window.localStorage.getItem(primaryNavStorageKey);
      return raw ? JSON.parse(raw) : null;
    } catch (error) {
      return null;
    }
  }

  function writeStoredOpenSections(sectionIds) {
    try {
      window.localStorage.setItem(primaryNavStorageKey, JSON.stringify(sectionIds));
    } catch (error) {
      return;
    }
  }

  function getPrimarySectionToggles() {
    var nav = document.querySelector("nav.md-nav--primary");
    var list = nav ? nav.querySelector(".md-nav__list") : null;

    if (!list) {
      return [];
    }

    return Array.prototype.slice.call(list.children)
      .map(function (item) {
        return Array.prototype.slice.call(item.children).find(function (child) {
          return child.matches && child.matches("input.md-nav__toggle[id^='__nav_']");
        });
      })
      .filter(Boolean);
  }

  function savePrimaryNavigationState() {
    var openIds = getPrimarySectionToggles()
      .filter(function (input) {
        return input.checked;
      })
      .map(function (input) {
        return input.id;
      });

    writeStoredOpenSections(openIds);
  }

  function restorePrimaryNavigationState() {
    var stored = readStoredOpenSections();
    var toggles = getPrimarySectionToggles();

    if (!stored || toggles.length === 0) {
      return;
    }

    toggles.forEach(function (input) {
      var item = input.closest(".md-nav__item");
      var isActiveBranch = item && item.classList.contains("md-nav__item--active");
      input.checked = stored.indexOf(input.id) !== -1 || isActiveBranch;
    });
  }

  function setupPrimaryNavigationPersistence() {
    var nav = document.querySelector("nav.md-nav--primary");
    var toggles = getPrimarySectionToggles();

    if (!nav || toggles.length === 0) {
      return;
    }

    restorePrimaryNavigationState();
    window.setTimeout(restorePrimaryNavigationState, 0);

    toggles.forEach(function (input) {
      if (input.dataset.cwNavPersist === "ready") {
        return;
      }

      input.dataset.cwNavPersist = "ready";
      input.addEventListener("change", savePrimaryNavigationState);
    });

    nav.querySelectorAll("a.md-nav__link").forEach(function (link) {
      if (link.dataset.cwNavPersist === "ready") {
        return;
      }

      link.dataset.cwNavPersist = "ready";
      link.addEventListener("click", savePrimaryNavigationState);
    });
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

  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(function () {
      setupTocToggle();
      setupPrimaryNavigationPersistence();
    });
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      setupTocToggle();
      setupPrimaryNavigationPersistence();
    });
  } else {
    setupTocToggle();
    setupPrimaryNavigationPersistence();
  }

  window.addEventListener("beforeunload", savePrimaryNavigationState);
})();
