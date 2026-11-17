/*
 * SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
(() => {
  function init() {
    const topic = document.getElementById('acc-accuracy');
    const nav = topic?.querySelector('.evaluation-study-links');
    if (!nav) return;
    const reader = topic.querySelector('.evaluation-study-reader');
    const sideTopics = window.matchMedia('(min-width: 1100px)');
    const tabs = [...nav.querySelectorAll('a[href^="#"]')];
    const panels = tabs.map(tab => targetOf(tab.hash));
    if (!tabs.length || panels.some(panel => !panel?.matches('.evaluation-study') || !topic.contains(panel))) return;
    let current = 0;
    let scrollFrame = 0;

    function targetOf(hash) {
      if (!hash || hash === '#') return null;
      try { return document.getElementById(decodeURIComponent(hash.slice(1))); }
      catch (_) { return null; }
    }

    function indexOf(target) {
      return target ? panels.findIndex(panel => panel === target || panel.contains(target)) : -1;
    }

    function openDetails(target) {
      for (let details = target.closest('details'); details; details = details.parentElement?.closest('details')) details.open = true;
    }

    // A study's own fragment lands above the tabs, including during app.js's
    // initial layout stabilization. Descendant fragments keep their own target.
    function updateLanding() {
      const contentTop = reader ? reader.getBoundingClientRect().top + (parseFloat(getComputedStyle(reader).paddingTop) || 0) : panels[current].getBoundingClientRect().top;
      const offset = Math.max(0, contentTop - topic.getBoundingClientRect().top);
      topic.style.setProperty('--evaluation-study-offset', `${offset}px`);
      nav.setAttribute('aria-orientation', sideTopics.matches ? 'vertical' : 'horizontal');
    }

    function revealTab(tab) {
      const box = nav.getBoundingClientRect();
      const rect = tab.getBoundingClientRect();
      if (rect.left < box.left) nav.scrollLeft -= box.left - rect.left;
      else if (rect.right > box.right) nav.scrollLeft += rect.right - box.right;
    }

    function select(index, focus = false) {
      current = index;
      tabs.forEach((tab, i) => {
        tab.setAttribute('aria-selected', String(i === index));
        tab.tabIndex = i === index ? 0 : -1;
        panels[i].hidden = i !== index;
      });
      if (reader) reader.scrollTop = 0;
      updateLanding();
      revealTab(tabs[index]);
      if (focus) tabs[index].focus({ preventScroll: true });
    }

    function keepTabsVisible() {
      const rect = nav.getBoundingClientRect();
      const top = (parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop) || 0) + 8;
      if (rect.top < top || rect.bottom > window.innerHeight - 8) {
        topic.scrollIntoView({ block: 'start', behavior: 'instant' });
      }
    }

    function activate(index, focus = false) {
      cancelAnimationFrame(scrollFrame);
      select(index, focus);
      if (location.hash !== tabs[index].hash) history.pushState(null, '', tabs[index].hash);
      keepTabsVisible();
    }

    function followHash(scroll = true) {
      cancelAnimationFrame(scrollFrame);
      const target = targetOf(location.hash);
      const index = indexOf(target);
      if (index < 0) {
        if (!location.hash || target === topic) select(0);
        return;
      }
      select(index);
      openDetails(target);
      if (scroll) scrollFrame = requestAnimationFrame(() => {
        (target === panels[index] ? topic : target).scrollIntoView({ block: 'start', behavior: 'instant' });
      });
    }

    nav.setAttribute('role', 'tablist');
    nav.setAttribute('aria-orientation', 'horizontal');
    tabs.forEach((tab, index) => {
      if (!tab.id) tab.id = `${panels[index].id}-tab`;
      tab.setAttribute('role', 'tab');
      tab.setAttribute('aria-controls', panels[index].id);
      tab.removeAttribute('aria-current');
      panels[index].setAttribute('role', 'tabpanel');
      panels[index].setAttribute('aria-labelledby', tab.id);
      panels[index].tabIndex = 0;
    });
    topic.classList.add('is-study-switcher');
    select(Math.max(0, indexOf(targetOf(location.hash))));

    nav.addEventListener('keydown', event => {
      const index = tabs.indexOf(event.target);
      if (index < 0 || event.altKey || event.ctrlKey || event.metaKey) return;
      let next;
      if (event.key === 'ArrowRight' || (sideTopics.matches && event.key === 'ArrowDown')) next = (index + 1) % tabs.length;
      else if (event.key === 'ArrowLeft' || (sideTopics.matches && event.key === 'ArrowUp')) next = (index + tabs.length - 1) % tabs.length;
      else if (event.key === 'Home') next = 0;
      else if (event.key === 'End') next = tabs.length - 1;
      else if (event.key === ' ') next = index;
      else return;
      event.preventDefault();
      activate(next, true);
    });

    // Reveal a study before the browser or another script scrolls to any of
    // its fragments. Ordinary modified clicks retain native link behavior.
    document.addEventListener('click', event => {
      if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      const link = event.target.closest('a[href]');
      if (!link || link.hasAttribute('download') || (link.target && link.target !== '_self')) return;
      const url = new URL(link.href, location.href);
      if (url.origin !== location.origin || url.pathname !== location.pathname || url.search !== location.search) return;
      const target = targetOf(url.hash);
      const index = indexOf(target);
      if (index < 0) return;
      if (target === panels[index]) {
        event.preventDefault();
        activate(index, nav.contains(link));
      } else {
        select(index);
        openDetails(target);
      }
    }, true);

    // Capture runs before app.js's existing fragment listener. Initializing
    // during deferred execution also precedes its DOMContentLoaded scroll.
    window.addEventListener('hashchange', () => followHash(), true);
    window.addEventListener('popstate', () => followHash(), true);
    document.addEventListener('DOMContentLoaded', () => followHash(false), { capture: true, once: true });
    window.addEventListener('resize', updateLanding, { passive: true });
    if ('ResizeObserver' in window) new ResizeObserver(updateLanding).observe(topic);
    followHash(false);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { capture: true, once: true });
  else init();
})();
