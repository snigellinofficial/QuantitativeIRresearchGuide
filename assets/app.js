/* ============================================================
   滚动高亮、进度条、移动端目录
   ============================================================ */
(function () {
  "use strict";

  var links = Array.prototype.slice.call(document.querySelectorAll(".toc a[href^='#']"));
  var targets = links.map(function (a) {
    var id = a.getAttribute("href").slice(1);
    return { link: a, el: document.getElementById(id) };
  }).filter(function (x) { return x.el; });

  var bar = document.getElementById("pbar");
  var sidebar = document.getElementById("sidebar");
  var menuBtn = document.getElementById("menuBtn");
  var ticking = false;

  function onScroll() {
    var y = window.scrollY || document.documentElement.scrollTop;
    var h = document.documentElement.scrollHeight - window.innerHeight;
    if (bar) bar.style.width = (h > 0 ? Math.min(100, (y / h) * 100) : 0) + "%";

    var best = null;
    for (var k = 0; k < targets.length; k++) {
      var top = targets[k].el.getBoundingClientRect().top;
      if (top - 90 <= 0) best = targets[k];
    }
    if (!best && targets.length) best = targets[0];
    links.forEach(function (a) { a.classList.remove("active"); });
    if (best) {
      best.link.classList.add("active");
      if (sidebar && sidebar.classList.contains("open") && window.innerWidth > 1080) {
        /* 桌面端不处理 */
      }
    }
    ticking = false;
  }

  window.addEventListener("scroll", function () {
    if (!ticking) { window.requestAnimationFrame(onScroll); ticking = true; }
  }, { passive: true });

  window.addEventListener("resize", onScroll);

  if (menuBtn && sidebar) {
    menuBtn.addEventListener("click", function () {
      sidebar.classList.toggle("open");
    });
    sidebar.addEventListener("click", function (e) {
      if (e.target.tagName === "A" && window.innerWidth <= 1080) {
        sidebar.classList.remove("open");
      }
    });
  }

  onScroll();

  /* 公式渲染完成后回到锚点，避免异步排版把深链接冲掉 */
  (function restoreHash() {
    var tries = 0;
    function attempt() {
      tries += 1;
      var mj = window.MathJax;
      if (mj && mj.startup && mj.startup.promise && mj.typesetPromise) {
        mj.startup.promise.then(function () {
          if (!location.hash) return;
          var el = document.getElementById(location.hash.slice(1));
          if (el) el.scrollIntoView();
          onScroll();
        }).catch(function () { /* 渲染失败时保持默认位置 */ });
        return;
      }
      if (tries < 60) setTimeout(attempt, 250);
    }
    attempt();
  })();
})();
