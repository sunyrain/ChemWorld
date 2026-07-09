(function () {
  function siteRoot() {
    var path = window.location.pathname;
    var enIndex = path.indexOf("/en/");

    if (enIndex >= 0) {
      return path.slice(0, enIndex + 1);
    }

    if (path.endsWith("/en")) {
      return path.slice(0, -2);
    }

    var logo = document.querySelector(".md-header__button.md-logo, .md-logo");
    if (logo && logo.href) {
      return new URL(logo.href, window.location.origin).pathname;
    }

    var parts = path.split("/").filter(Boolean);
    if (parts.length > 1) {
      return "/" + parts[0] + "/";
    }
    return "/";
  }

  function addLanguageSwitch() {
    if (document.querySelector(".cw-floating-language-switch")) {
      return;
    }

    var root = siteRoot();
    var zhUrl = new URL(root, window.location.origin);
    var enUrl = new URL(root.replace(/\/$/, "/en/"), window.location.origin);
    var isEnglish = window.location.pathname.indexOf("/en/") >= 0 || window.location.pathname.endsWith("/en");

    var switcher = document.createElement("nav");
    switcher.className = "cw-floating-language-switch";
    switcher.setAttribute("aria-label", "Language switch");

    var zh = document.createElement("a");
    zh.href = zhUrl.href;
    zh.textContent = "中文";
    zh.className = isEnglish ? "" : "is-active";
    zh.setAttribute("aria-label", "切换到中文");

    var en = document.createElement("a");
    en.href = enUrl.href;
    en.textContent = "EN";
    en.className = isEnglish ? "is-active" : "";
    en.setAttribute("aria-label", "Switch to English");

    switcher.appendChild(zh);
    switcher.appendChild(en);
    document.body.appendChild(switcher);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", addLanguageSwitch);
  } else {
    addLanguageSwitch();
  }
})();
