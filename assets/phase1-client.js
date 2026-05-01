(function () {
  function resolveApiBase() {
    const configured = (window.__THREADBORN_API_BASE || localStorage.getItem("threadborn_api_base") || "").replace(/\/$/, "");
    if (configured) {
      return configured;
    }
    const host = window.location.hostname;
    if (host === "appassets.androidplatform.net" || window.location.protocol === "file:") {
      return "https://threadborn.vercel.app";
    }
    return "";
  }

  const API_BASE = resolveApiBase();
  const QUEUE_KEY = "threadborn_sync_queue_v1";
  const FALLBACK_PROGRESS_KEY = "novelverse_reader_progress";
  const APP_SESSION_KEY = "threadborn_app_session";
  let csrfToken = "";
  let authUser = null;
  let bookmarkCache = [];
  let analyticsBuffer = [];
  let analyticsTimer = null;
  let syncTimer = null;
  let readerActiveSince = null;
  let authConfigMissing = false;

  function apiPath(path) {
    return `${API_BASE}${path}`;
  }

  function getAppMode() {
    return String(window.__THREADBORN_APP_MODE || localStorage.getItem("threadborn_app_mode") || "").trim().toLowerCase();
  }

  function buildAuthHeaders(headers = {}) {
    const next = Object.assign({ "Content-Type": "application/json" }, headers);
    const appMode = getAppMode();
    const appSession = localStorage.getItem(APP_SESSION_KEY) || "";
    if (appMode) {
      next["X-Threadborn-App-Mode"] = appMode;
      localStorage.setItem("threadborn_app_mode", appMode);
    }
    if (appSession) {
      next.Authorization = `Bearer ${appSession}`;
    }
    return next;
  }

  async function apiFetch(path, options = {}) {
    const headers = buildAuthHeaders(options.headers || {});
    if (csrfToken) {
      headers["X-CSRF-Token"] = csrfToken;
    }
    const response = await fetch(apiPath(path), Object.assign({}, options, {
      credentials: "include",
      headers
    }));
    let payload = {};
    try {
      payload = await response.json();
    } catch (error) {
      payload = { success: false, error: "Invalid response" };
    }
    if (!response.ok || !payload.success) {
      const err = new Error(payload.error || "Request failed");
      err.status = response.status || 500;
      throw err;
    }
    return payload.data;
  }

  function saveQueue(queue) {
    localStorage.setItem(QUEUE_KEY, JSON.stringify(queue));
  }

  function readQueue() {
    try {
      return JSON.parse(localStorage.getItem(QUEUE_KEY) || "[]");
    } catch (error) {
      return [];
    }
  }

  function enqueue(item) {
    const queue = readQueue();
    queue.push(Object.assign({ retries: 0 }, item));
    saveQueue(queue);
  }

  async function drainQueue() {
    const queue = readQueue();
    if (!queue.length || !authUser) {
      return;
    }
    const nextQueue = [];
    for (const item of queue) {
      try {
        if (item.type === "progress") {
          await apiFetch("/api/reader/progress", {
            method: "PUT",
            body: JSON.stringify(item.payload)
          });
        } else if (item.type === "bookmark") {
          await apiFetch("/api/reader/bookmarks", {
            method: "POST",
            body: JSON.stringify(item.payload)
          });
        } else if (item.type === "bookmark_delete") {
          await apiFetch("/api/reader/bookmarks", {
            method: "DELETE",
            body: JSON.stringify(item.payload)
          });
        } else if (item.type === "analytics") {
          await apiFetch("/api/reader/analytics", {
            method: "POST",
            body: JSON.stringify({ events: item.payload.events })
          });
        }
      } catch (error) {
        item.retries += 1;
        if (item.retries <= 7) {
          nextQueue.push(item);
        }
      }
    }
    saveQueue(nextQueue);
  }

  function toggleAuthNav() {
    const loggedIn = Boolean(authUser);
    const loginEl = document.getElementById("nav-login");
    const signupEl = document.getElementById("nav-signup");
    const profileEl = document.getElementById("nav-profile");
    const logoutEl = document.getElementById("nav-logout");
    const mLoginEl = document.getElementById("mobile-nav-login");
    const mSignupEl = document.getElementById("mobile-nav-signup");
    const mProfileEl = document.getElementById("mobile-nav-profile");
    const mLogoutEl = document.getElementById("mobile-nav-logout");
    [loginEl, signupEl, mLoginEl, mSignupEl].forEach(el => {
      if (el) {
        el.style.display = loggedIn ? "none" : "";
      }
    });
    [profileEl, logoutEl, mProfileEl, mLogoutEl].forEach(el => {
      if (el) {
        el.style.display = loggedIn ? "" : "none";
      }
    });
    if (typeof window.renderUserChip === "function") {
      window.renderUserChip();
    }
    const userName = document.getElementById("user-name");
    if (userName && authConfigMissing && !loggedIn) {
      userName.textContent = "Setup required";
    }
  }

  function getChapterMeta() {
    if (!window.chapters || !window.chapters[window.activeChapter]) {
      return null;
    }
    const chapter = window.chapters[window.activeChapter];
    return {
      novelId: "threadborn",
      volumeId: chapter.volume,
      chapterId: chapter.chapter,
      scrollPosition: Number(window.activePage || 0)
    };
  }

  async function syncProgressNow() {
    if (!authUser) {
      return;
    }
    const payload = getChapterMeta();
    if (!payload) {
      return;
    }
    try {
      await apiFetch("/api/reader/progress", {
        method: "PUT",
        body: JSON.stringify(payload)
      });
      const saveSummary = document.getElementById("reader-save-summary");
      if (saveSummary) {
        saveSummary.textContent = "Synced to account";
      }
    } catch (error) {
      enqueue({ type: "progress", payload });
    }
  }

  function addAnalyticsTick() {
    if (!authUser || readerActiveSince === null) {
      return;
    }
    const payload = getChapterMeta();
    if (!payload) {
      return;
    }
    const now = Date.now();
    const seconds = Math.max(1, Math.round((now - readerActiveSince) / 1000));
    readerActiveSince = now;
    analyticsBuffer.push({
      novelId: payload.novelId,
      volumeId: payload.volumeId,
      chapterId: payload.chapterId,
      timeSpent: seconds
    });
  }

  async function flushAnalytics() {
    if (!analyticsBuffer.length || !authUser) {
      return;
    }
    const events = analyticsBuffer.splice(0, analyticsBuffer.length);
    try {
      await apiFetch("/api/reader/analytics", {
        method: "POST",
        body: JSON.stringify({ events })
      });
    } catch (error) {
      enqueue({ type: "analytics", payload: { events } });
    }
  }

  function renderBookmarkSelect() {
    if (typeof window.mergeServerBookmarks === "function") {
      window.mergeServerBookmarks(bookmarkCache);
      return;
    }
    const select = document.getElementById("bookmark-jump");
    if (!select) {
      return;
    }
    const options = [`<option value="">Select a bookmark</option>`];
    bookmarkCache.forEach(bookmark => {
      const label = bookmark.label || `${bookmark.volume_id} • ${bookmark.chapter_id} • p${Math.floor(bookmark.scroll_position) + 1}`;
      options.push(`<option value="${bookmark.id}">${label}</option>`);
    });
    select.innerHTML = options.join("");
  }

  async function loadBookmarks() {
    if (!authUser) {
      if (typeof window.renderBookmarks === "function") {
        window.renderBookmarks();
      } else {
        bookmarkCache = [];
        renderBookmarkSelect();
      }
      return;
    }
    try {
      const data = await apiFetch("/api/reader/bookmarks?novelId=threadborn");
      bookmarkCache = data.bookmarks || [];
      renderBookmarkSelect();
    } catch (error) {
      // ignore
    }
  }

  window.addBookmarkFromReader = async function addBookmarkFromReader() {
    if (typeof window.createBookmark === "function") {
      window.createBookmark();
      return;
    }
    if (!authUser) {
      return;
    }
    const payload = getChapterMeta();
    if (!payload) {
      return;
    }
    const label = window.prompt("Bookmark label (optional)", "");
    try {
      await apiFetch("/api/reader/bookmarks", {
        method: "POST",
        body: JSON.stringify(Object.assign({}, payload, { label: label || "" }))
      });
      loadBookmarks();
    } catch (error) {
      alert("Could not save bookmark.");
    }
  };

  window.syncBookmarkToAccount = async function syncBookmarkToAccount(bookmark) {
    if (!authUser || !bookmark) {
      return;
    }
    const payload = {
      novelId: "threadborn",
      volumeId: bookmark.volumeId,
      chapterId: bookmark.chapterId,
      scrollPosition: Number(bookmark.pageIndex || 0),
      label: bookmark.label || ""
    };
    try {
      const data = await apiFetch("/api/reader/bookmarks", {
        method: "POST",
        body: JSON.stringify(payload)
      });
      if (data.bookmark && typeof window.mergeServerBookmarks === "function") {
        window.mergeServerBookmarks([data.bookmark]);
      }
      const status = document.getElementById("bookmark-status");
      if (status) {
        status.textContent = "Bookmark saved and synced.";
      }
    } catch (error) {
      enqueue({ type: "bookmark", payload });
      const status = document.getElementById("bookmark-status");
      if (status) {
        status.textContent = "Bookmark saved locally. Sync queued.";
      }
    }
  };

  window.deleteBookmarkFromAccount = async function deleteBookmarkFromAccount(bookmark) {
    if (!authUser || !bookmark || !bookmark.serverId) {
      return;
    }
    const payload = { id: bookmark.serverId };
    try {
      await apiFetch("/api/reader/bookmarks", {
        method: "DELETE",
        body: JSON.stringify(payload)
      });
    } catch (error) {
      enqueue({ type: "bookmark_delete", payload });
    }
  };

  async function syncLocalBookmarks() {
    if (!authUser || typeof window.readLocalBookmarks !== "function" || typeof window.mergeServerBookmarks !== "function") {
      return;
    }
    const localBookmarks = window.readLocalBookmarks();
    for (const bookmark of localBookmarks) {
      if (bookmark.synced || bookmark.serverId) {
        continue;
      }
      const payload = {
        novelId: "threadborn",
        volumeId: bookmark.volumeId,
        chapterId: bookmark.chapterId,
        scrollPosition: Number(bookmark.pageIndex || 0),
        label: bookmark.label || ""
      };
      try {
        const data = await apiFetch("/api/reader/bookmarks", {
          method: "POST",
          body: JSON.stringify(payload)
        });
        if (data.bookmark) {
          window.mergeServerBookmarks([data.bookmark]);
        }
      } catch (error) {
        enqueue({ type: "bookmark", payload });
      }
    }
  }

  window.jumpToBookmark = function jumpToBookmark(id) {
    if (!id) {
      return;
    }
    const bookmark = bookmarkCache.find(item => item.id === id);
    if (!bookmark || !window.chapters) {
      return;
    }
    const idx = window.chapters.findIndex(ch => ch.volume === bookmark.volume_id && ch.chapter === bookmark.chapter_id);
    if (idx >= 0 && typeof window.openChapter === "function") {
      window.openChapter(idx, Number(bookmark.scroll_position || 0));
    }
  };

  window.logoutUser = async function logoutUser() {
    try {
      await apiFetch("/api/auth/logout", { method: "POST", body: "{}" });
    } catch (error) {
      // ignore
    }
    authUser = null;
    csrfToken = "";
    localStorage.removeItem(APP_SESSION_KEY);
    localStorage.removeItem("threadborn_csrf_token");
    localStorage.removeItem("threadborn_user");
    toggleAuthNav();
  };

  async function hydrateAuth() {
    try {
      const data = await apiFetch("/api/auth/me", { method: "GET" });
      authUser = data.user;
      csrfToken = data.csrfToken || "";
      authConfigMissing = false;
      localStorage.setItem("threadborn_user", JSON.stringify({
        id: authUser.id,
        email: authUser.email,
        displayName: authUser.username,
        avatarUrl: authUser.avatarUrl,
        verified: authUser.verified,
        role: authUser.role
      }));
    } catch (error) {
      const isAuthError = error.status === 401 || error.status === 403;
      if (isAuthError) {
        authUser = null;
        csrfToken = "";
        localStorage.removeItem("threadborn_user");
        localStorage.removeItem("threadborn_csrf_token");
        localStorage.removeItem(APP_SESSION_KEY);
      } else {
        try {
          const cachedUser = localStorage.getItem("threadborn_user");
          if (cachedUser) {
            authUser = JSON.parse(cachedUser);
          }
        } catch (e) {}
      }
      authConfigMissing = String(error.message || "").includes("Missing DATABASE_URL");
    }
    toggleAuthNav();
    await syncLocalBookmarks();
    await loadBookmarks();
  }

  async function hydrateServerProgress() {
    if (!authUser || !window.chapters || !window.chapters.length) {
      return;
    }
    try {
      const data = await apiFetch("/api/reader/progress?novelId=threadborn", { method: "GET" });
      if (!data.progress) {
        return;
      }
      const chapterIndex = window.chapters.findIndex(ch =>
        ch.volume === data.progress.volume_id && ch.chapter === data.progress.chapter_id
      );
      if (chapterIndex >= 0) {
        window.activeChapter = chapterIndex;
        window.activePage = Math.max(0, Number(data.progress.scroll_position || 0));
        if (typeof window.updateResumeButton === "function") {
          window.updateResumeButton();
        }
        const saved = {
          chapter: chapterIndex,
          page: window.activePage,
          size: window.readerSize || 18,
          theme: window.readerTheme || "night"
        };
        localStorage.setItem(FALLBACK_PROGRESS_KEY, JSON.stringify(saved));
      }
    } catch (error) {
      // ignore
    }
  }

  function monkeyPatchReaderHooks() {
    if (typeof window.renderPage === "function") {
      const originalRenderPage = window.renderPage;
      window.renderPage = function patchedRenderPage() {
        originalRenderPage.apply(this, arguments);
        syncProgressNow();
      };
    }
    if (typeof window.openChapter === "function") {
      const originalOpenChapter = window.openChapter;
      window.openChapter = function patchedOpenChapter() {
        readerActiveSince = Date.now();
        originalOpenChapter.apply(this, arguments);
      };
    }
    if (typeof window.closeReader === "function") {
      const originalCloseReader = window.closeReader;
      window.closeReader = function patchedCloseReader() {
        addAnalyticsTick();
        flushAnalytics();
        readerActiveSince = null;
        originalCloseReader.apply(this, arguments);
      };
    }
  }

  function startBackgroundSync() {
    if (syncTimer) {
      clearInterval(syncTimer);
    }
    syncTimer = setInterval(() => {
      drainQueue();
      syncProgressNow();
    }, 12_000);
    if (analyticsTimer) {
      clearInterval(analyticsTimer);
    }
    analyticsTimer = setInterval(() => {
      addAnalyticsTick();
      flushAnalytics();
    }, 45_000);
    window.addEventListener("online", drainQueue);
  }

  window.addEventListener("load", async () => {
    monkeyPatchReaderHooks();
    await hydrateAuth();
    await hydrateServerProgress();
    startBackgroundSync();
  });
})();
