(function () {
  var tocStorageKey = "chemworld.toc.collapsed.v7";
  var primaryStorageKey = "chemworld.primary.collapsed.v7";
  var sectionStoragePrefix = "chemworld.section.collapsed.v7:";

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

  function currentHashId() {
    if (!window.location.hash) return "";
    try {
      return decodeURIComponent(window.location.hash.slice(1));
    } catch (error) {
      return window.location.hash.slice(1);
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

    function sectionToggles() {
      return Array.from(nav.querySelectorAll("input.md-toggle"));
    }

    function render(collapsed) {
      button.textContent = collapsed ? "全部展开" : "全部折叠";
      button.setAttribute("aria-expanded", collapsed ? "false" : "true");
      button.setAttribute("aria-label", collapsed ? "展开左侧全部目录分组" : "折叠左侧全部目录分组");
    }

    var collapsed = readFlag(primaryStorageKey);
    if (collapsed) {
      sectionToggles().forEach(function (toggle) {
        toggle.checked = false;
      });
    }
    render(collapsed);
    button.addEventListener("click", function (event) {
      event.preventDefault();
      event.stopPropagation();
      collapsed = !collapsed;
      sectionToggles().forEach(function (toggle) {
        toggle.checked = !collapsed;
      });
      writeFlag(primaryStorageKey, collapsed);
      render(collapsed);
    });
    title.appendChild(button);
  }

  function setupTocNavigation() {
    document.querySelectorAll("nav.md-nav--secondary").forEach(function (nav) {
      var list = nav.querySelector(":scope > [data-md-component='toc']");
      if (!list || nav.dataset.cwToc === "ready") return;
      nav.dataset.cwToc = "ready";

      var heading = document.createElement("div");
      heading.className = "cw-toc-heading";
      var label = document.createElement("span");
      label.textContent = "本页目录";
      var button = document.createElement("button");
      button.type = "button";
      button.className = "cw-outline-toggle";
      heading.appendChild(label);
      heading.appendChild(button);
      list.before(heading);

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
    });
  }

  function setupContentSections() {
    var content = document.querySelector(".md-content__inner.md-typeset");
    if (!content || content.dataset.cwSections === "ready") return;
    content.dataset.cwSections = "ready";

    Array.from(content.querySelectorAll(":scope > h2[id]")).forEach(function (heading) {
      var body = document.createElement("div");
      body.className = "cw-section-body";
      body.dataset.cwSectionFor = heading.id;
      while (heading.nextSibling && !(heading.nextSibling.nodeType === 1 && heading.nextSibling.tagName === "H2")) {
        body.appendChild(heading.nextSibling);
      }
      heading.after(body);
      heading.classList.add("cw-section-heading");

      var button = document.createElement("button");
      button.type = "button";
      button.className = "cw-section-toggle";
      var storageKey = sectionStoragePrefix + window.location.pathname + "#" + heading.id;
      var headingLabel = heading.textContent.trim();

      function render(collapsed) {
        body.hidden = collapsed;
        heading.classList.toggle("cw-section-collapsed", collapsed);
        button.textContent = collapsed ? "+" : "−";
        button.setAttribute("aria-expanded", collapsed ? "false" : "true");
        button.setAttribute("aria-controls", "cw-section-" + heading.id);
        button.setAttribute("aria-label", collapsed ? "展开“" + headingLabel + "”" : "折叠“" + headingLabel + "”");
      }

      body.id = "cw-section-" + heading.id;
      var hashId = currentHashId();
      var hashNode = hashId ? document.getElementById(hashId) : null;
      var hashTarget = hashNode && body.contains(hashNode);
      var collapsed = hashTarget ? false : readFlag(storageKey);
      render(collapsed);
      button.addEventListener("click", function (event) {
        event.preventDefault();
        event.stopPropagation();
        collapsed = !collapsed;
        writeFlag(storageKey, collapsed);
        render(collapsed);
      });
      heading.appendChild(button);
    });
  }

  function revealHashTarget() {
    var hashId = currentHashId();
    if (!hashId) return;
    var target = document.getElementById(hashId);
    var body = target && target.closest(".cw-section-body");
    if (!body || !body.hidden) return;
    var heading = document.getElementById(body.dataset.cwSectionFor);
    var button = heading && heading.querySelector(".cw-section-toggle");
    if (button) button.click();
  }

  function setup() {
    setupPrimaryNavigation();
    setupTocNavigation();
    setupContentSections();
    revealHashTarget();
  }

  window.addEventListener("hashchange", revealHashTarget);
  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(setup);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", setup);
  } else {
    setup();
  }
})();
