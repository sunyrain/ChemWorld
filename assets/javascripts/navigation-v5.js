(function () {
  var tocStorageKey = "chemworld.toc.collapsed.v5";

  function readFlag(key) {
    try {
      return window.localStorage.getItem(key) === "1";
    } catch (error) {
      return false;
    }
  }

  function writeFlag(key, value) {
    try {
      window.localStorage.setItem(key, value ? "1" : "0");
    } catch (error) {
      return;
    }
  }

  function setupPrimaryNavigation() {
    var nav = document.querySelector("nav.md-nav--primary");
    if (!nav || nav.dataset.cwNavigation === "ready") return;

    var title = nav.querySelector(":scope > .md-nav__title");
    if (!title) return;

    nav.dataset.cwNavigation = "ready";
    var button = document.createElement("button");
    button.type = "button";
    button.className = "cw-nav-collapse";
    button.textContent = "全部折叠";
    button.setAttribute("aria-label", "折叠左侧全部目录分组");

    button.addEventListener("click", function (event) {
      event.preventDefault();
      event.stopPropagation();
      nav.querySelectorAll("input.md-toggle").forEach(function (toggle) {
        toggle.checked = false;
      });
      button.textContent = "已折叠";
      window.setTimeout(function () {
        button.textContent = "全部折叠";
      }, 900);
    });

    title.appendChild(button);
  }

  function setupTocNavigation() {
    document.querySelectorAll("nav.md-nav--secondary").forEach(function (nav) {
      var title = nav.querySelector(".md-nav__title");
      var list = nav.querySelector("[data-md-component='toc']");
      if (!title || !list || nav.dataset.cwToc === "ready") return;

      nav.dataset.cwToc = "ready";
      var button = document.createElement("button");
      button.type = "button";
      button.className = "cw-outline-toggle";

      function render(collapsed) {
        nav.classList.toggle("cw-toc-collapsed", collapsed);
        button.textContent = collapsed ? "+" : "−";
        button.setAttribute("aria-expanded", collapsed ? "false" : "true");
        button.setAttribute("aria-label", collapsed ? "展开页内目录" : "折叠页内目录");
      }

      render(readFlag(tocStorageKey));
      button.addEventListener("click", function (event) {
        event.preventDefault();
        event.stopPropagation();
        var collapsed = !nav.classList.contains("cw-toc-collapsed");
        writeFlag(tocStorageKey, collapsed);
        render(collapsed);
      });
      title.appendChild(button);
    });
  }

  function setup() {
    setupPrimaryNavigation();
    setupTocNavigation();
  }

  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(setup);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", setup);
  } else {
    setup();
  }
})();
