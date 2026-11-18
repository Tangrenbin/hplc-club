(function () {
  "use strict";

  /* ==========================================================================
   * 1. Homepage Directory Instant Filter & Tabs
   * ========================================================================== */
  function initDirectoryFilter(root) {
    var shell = root.querySelector(".dir-shell");
    if (!shell || shell.dataset.dirBound === "1") return;
    shell.dataset.dirBound = "1";

    var input = shell.querySelector("#dir-filter-input");
    var kbd = shell.querySelector("#dir-filter-kbd");
    var tabs = Array.prototype.slice.call(shell.querySelectorAll(".dir-tab"));
    var chips = Array.prototype.slice.call(shell.querySelectorAll(".dir-chip"));
    var rows = Array.prototype.slice.call(shell.querySelectorAll(".dir-row"));
    var countEl = shell.querySelector("#dir-result-count");
    var emptyEl = shell.querySelector("#dir-empty");
    var resetBtn = shell.querySelector("#dir-reset-btn");

    var state = {
      group: "all",
      region: "all",
      query: ""
    };

    var total = rows.length;

    function applyFilter() {
      var tokens = state.query
        .toLowerCase()
        .trim()
        .split(/\s+/)
        .filter(Boolean);

      var visibleCount = 0;
      rows.forEach(function (row) {
        var matchGroup = state.group === "all" || row.dataset.group === state.group;
        var matchRegion = state.region === "all" || row.dataset.region === state.region;
        var hay = row.dataset.search || "";
        var matchQuery =
          tokens.length === 0 ||
          tokens.every(function (t) {
            return hay.indexOf(t) !== -1;
          });

        var show = matchGroup && matchRegion && matchQuery;
        row.hidden = !show;
        if (show) {
          visibleCount += 1;
          var idxEl = row.querySelector(".dir-row__idx");
          if (idxEl) {
            idxEl.textContent = visibleCount < 10 ? "0" + visibleCount : String(visibleCount);
          }
        }
      });

      if (countEl) {
        var filtered = state.group !== "all" || state.region !== "all" || tokens.length > 0;
        countEl.textContent = filtered
          ? "匹配 " + visibleCount + " / " + total + " 篇文档"
          : "共 " + total + " 篇文档";
      }

      if (emptyEl) {
        emptyEl.hidden = visibleCount > 0;
      }
      if (kbd) {
        kbd.hidden = Boolean(input && input.value.length > 0);
      }
    }

    tabs.forEach(function (tab) {
      tab.addEventListener("click", function () {
        state.group = tab.dataset.filterGroup || "all";
        tabs.forEach(function (t) {
          t.classList.toggle("is-active", t === tab);
        });
        applyFilter();
      });
    });

    chips.forEach(function (chip) {
      chip.addEventListener("click", function () {
        var clickedRegion = chip.dataset.filterRegion || "all";
        if (clickedRegion !== "all" && state.region === clickedRegion) {
          state.region = "all";
        } else {
          state.region = clickedRegion;
        }
        chips.forEach(function (c) {
          c.classList.toggle("is-active", (c.dataset.filterRegion || "all") === state.region);
        });
        applyFilter();
      });
    });

    if (input) {
      input.addEventListener("input", function () {
        state.query = input.value || "";
        applyFilter();
      });
      input.addEventListener("keydown", function (e) {
        if (e.key === "Escape") {
          input.value = "";
          state.query = "";
          applyFilter();
          input.blur();
        }
      });
    }

    if (resetBtn) {
      resetBtn.addEventListener("click", function () {
        state.group = "all";
        state.region = "all";
        state.query = "";
        if (input) input.value = "";
        tabs.forEach(function (t) {
          t.classList.toggle("is-active", t.dataset.filterGroup === "all");
        });
        chips.forEach(function (c) {
          c.classList.toggle("is-active", c.dataset.filterRegion === "all");
        });
        applyFilter();
      });
    }
  }

  /* Global '/' shortcut for homepage filter */
  document.addEventListener("keydown", function (e) {
    if (e.key !== "/" || e.ctrlKey || e.metaKey || e.altKey) return;
    var active = document.activeElement;
    if (
      active &&
      (active.tagName === "INPUT" ||
        active.tagName === "TEXTAREA" ||
        active.isContentEditable)
    ) {
      return;
    }
    var dirInput = document.getElementById("dir-filter-input");
    if (dirInput) {
      e.preventDefault();
      dirInput.focus();
      dirInput.select();
    }
  });

  /* ==========================================================================
   * 2. Document Image Figures, Auto-Grid & Lightbox Preview
   * ========================================================================== */
  var lightboxEl = null;
  var lbState = {
    images: [],
    index: 0
  };

  function ensureLightbox() {
    if (lightboxEl) return lightboxEl;
    var el = document.createElement("div");
    el.className = "club-lightbox";
    el.setAttribute("role", "dialog");
    el.setAttribute("aria-modal", "true");
    el.setAttribute("aria-label", "图片放大预览");
    el.hidden = true;
    el.innerHTML =
      '<div class="club-lightbox__backdrop" data-lb-close="1"></div>' +
      '<div class="club-lightbox__stage">' +
      '  <div class="club-lightbox__topbar">' +
      '    <span class="club-lightbox__counter" id="club-lb-counter">1 / 1</span>' +
      '    <div class="club-lightbox__actions">' +
      '      <a class="club-lightbox__btn" id="club-lb-open-raw" href="#" target="_blank" rel="noopener" title="在新标签页查看原图">原图 ↗</a>' +
      '      <button type="button" class="club-lightbox__btn club-lightbox__close" data-lb-close="1" aria-label="关闭预览">✕ ESC</button>' +
      "    </div>" +
      "  </div>" +
      '  <div class="club-lightbox__BodyWrap">' +
      '    <button type="button" class="club-lightbox__nav club-lightbox__nav--prev" id="club-lb-prev" aria-label="上一张">‹</button>' +
      '    <div class="club-lightbox__canvas" data-lb-close="1">' +
      '      <img class="club-lightbox__img" id="club-lb-img" alt="" />' +
      "    </div>" +
      '    <button type="button" class="club-lightbox__nav club-lightbox__nav--next" id="club-lb-next" aria-label="下一张">›</button>' +
      "  </div>" +
      '  <div class="club-lightbox__caption" id="club-lb-caption"></div>' +
      "</div>";

    document.body.appendChild(el);

    el.addEventListener("click", function (e) {
      var target = e.target;
      if (target && target.dataset && target.dataset.lbClose === "1") {
        closeLightbox();
      }
    });

    el.querySelector("#club-lb-prev").addEventListener("click", function (e) {
      e.stopPropagation();
      stepLightbox(-1);
    });

    el.querySelector("#club-lb-next").addEventListener("click", function (e) {
      e.stopPropagation();
      stepLightbox(1);
    });

    document.addEventListener("keydown", function (e) {
      if (!lightboxEl || lightboxEl.hidden) return;
      if (e.key === "Escape") {
        e.preventDefault();
        closeLightbox();
      } else if (e.key === "ArrowLeft") {
        e.preventDefault();
        stepLightbox(-1);
      } else if (e.key === "ArrowRight") {
        e.preventDefault();
        stepLightbox(1);
      }
    });

    lightboxEl = el;
    return el;
  }

  function renderLightboxSlide() {
    if (!lightboxEl || !lbState.images.length) return;
    var item = lbState.images[lbState.index];
    var imgEl = lightboxEl.querySelector("#club-lb-img");
    var capEl = lightboxEl.querySelector("#club-lb-caption");
    var countEl = lightboxEl.querySelector("#club-lb-counter");
    var rawLink = lightboxEl.querySelector("#club-lb-open-raw");
    var prevBtn = lightboxEl.querySelector("#club-lb-prev");
    var nextBtn = lightboxEl.querySelector("#club-lb-next");

    imgEl.src = item.src;
    imgEl.alt = item.alt || "";
    capEl.textContent = item.alt || "";
    capEl.hidden = !item.alt;
    countEl.textContent = lbState.index + 1 + " / " + lbState.images.length;
    rawLink.href = item.src;

    var multi = lbState.images.length > 1;
    prevBtn.hidden = !multi;
    nextBtn.hidden = !multi;
  }

  function openLightbox(images, index) {
    var lb = ensureLightbox();
    lbState.images = images;
    lbState.index = index;
    renderLightboxSlide();
    lb.hidden = false;
    document.documentElement.classList.add("club-lb-lock");
  }

  function stepLightbox(delta) {
    if (!lbState.images.length) return;
    lbState.index =
      (lbState.index + delta + lbState.images.length) % lbState.images.length;
    renderLightboxSlide();
  }

  function closeLightbox() {
    if (!lightboxEl) return;
    lightboxEl.hidden = true;
    document.documentElement.classList.remove("club-lb-lock");
  }

  function isSingleImageParagraph(el) {
    if (!el || el.tagName !== "P") return false;
    var children = Array.prototype.filter.call(el.childNodes, function (n) {
      return !(n.nodeType === 3 && !n.textContent.trim());
    });
    return (
      children.length === 1 &&
      children[0].nodeType === 1 &&
      (children[0].tagName === "IMG" || children[0].classList.contains("club-figure"))
    );
  }

  function enhanceArticleMedia(root) {
    var article = root.querySelector(".md-content__inner");
    if (!article || article.querySelector(".dir-shell") || article.dataset.mediaEnhanced === "1") {
      return;
    }
    article.dataset.mediaEnhanced = "1";

    /* Split paragraphs that mix multiple images and .log links (e.g. Fujian 26-1) */
    var paragraphs = Array.prototype.slice.call(article.querySelectorAll("p"));
    paragraphs.forEach(function (p) {
      var imgs = Array.prototype.slice.call(p.querySelectorAll("img"));
      if (imgs.length < 2) return;

      var links = Array.prototype.slice.call(p.querySelectorAll("a"));
      var grid = document.createElement("div");
      grid.className = "club-img-grid";

      imgs.forEach(function (img) {
        grid.appendChild(img);
      });

      p.parentNode.insertBefore(grid, p);

      if (links.length > 0) {
        var attachBar = document.createElement("div");
        attachBar.className = "club-attach-bar";
        links.forEach(function (a) {
          attachBar.appendChild(a);
        });
        p.parentNode.insertBefore(attachBar, p);
      }

      if (!p.textContent.trim() && p.querySelectorAll("img, a").length === 0) {
        p.remove();
      }
    });

    /* Group 2+ consecutive single-image <p> elements into a clean 2-col gallery grid */
    var children = Array.prototype.slice.call(article.children);
    var run = [];
    function flushRun() {
      if (run.length >= 2) {
        var grid = document.createElement("div");
        grid.className = "club-img-grid";
        run[0].parentNode.insertBefore(grid, run[0]);
        run.forEach(function (pEl) {
          var img = pEl.querySelector("img");
          if (img) grid.appendChild(img);
          pEl.remove();
        });
      }
      run = [];
    }

    children.forEach(function (el) {
      if (isSingleImageParagraph(el)) {
        run.push(el);
      } else {
        flushRun();
      }
    });
    flushRun();

    /* Wrap every content image in a figure card with caption & bind lightbox */
    var rawImgs = Array.prototype.slice.call(article.querySelectorAll("img"));
    var pageImages = [];

    rawImgs.forEach(function (img) {
      var src = img.getAttribute("src") || "";
      if (!src || img.closest(".emojione, .twemoji")) return;

      img.setAttribute("loading", "lazy");

      var altText = (img.getAttribute("alt") || "").trim();
      var wrapper = document.createElement("span");
      wrapper.className = "club-figure";
      img.parentNode.insertBefore(wrapper, img);
      wrapper.appendChild(img);

      if (altText) {
        var cap = document.createElement("span");
        cap.className = "club-figcaption";
        cap.textContent = altText;
        wrapper.appendChild(cap);
      }

      var itemIndex = pageImages.length;
      pageImages.push({
        src: img.src || src,
        alt: altText
      });

      wrapper.addEventListener("click", function () {
        /* Refresh resolved img.src at click time */
        pageImages[itemIndex].src = img.currentSrc || img.src || src;
        openLightbox(pageImages, itemIndex);
      });
    });

    /* Style standalone .log links as attachment chips */
    var logLinks = Array.prototype.slice.call(article.querySelectorAll('a[href$=".log"], a[href*=".log?"]'));
    logLinks.forEach(function (a) {
      a.classList.add("club-log-link");
      if (!a.getAttribute("target")) {
        a.setAttribute("target", "_blank");
        a.setAttribute("rel", "noopener");
      }
    });
  }

  function boot(root) {
    var scope = root || document;
    closeLightbox();
    initDirectoryFilter(scope);
    enhanceArticleMedia(scope);
  }

  if (typeof window.document$ !== "undefined" && window.document$.subscribe) {
    window.document$.subscribe(function (doc) {
      boot(doc || document);
    });
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      boot(document);
    });
  } else {
    boot(document);
  }
})();
