import re

with open('assets/phase1-client.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace loadDashboardConfig and saveDashboardConfig
new_funcs = '''  window.getDashboardLang = function() {
    const isJp = window.location.pathname.indexOf('-jp') !== -1;
    let baseLang = isJp ? "ja" : "en";
    const select = document.getElementById("dashboard-target-lang");
    if (select) {
      baseLang = select.value;
    }
    return baseLang;
  };

  window.loadDashboardConfig = async function loadDashboardConfig() {
    try {
      const lang = window.getDashboardLang();
      const isJp = window.location.pathname.indexOf('-jp') !== -1;
      const displayLang = isJp ? "ja" : "en";
      
      const data = await apiFetch(`/api/dashboard?action=config&lang=${displayLang}`);
      
      const notifBanner = document.getElementById("global-announcement-banner");
      if (data.notification) {
        notifBanner.innerHTML = `<strong>BiniFn:</strong> ${data.notification}`;
        notifBanner.style.display = "";
      } else {
        if(notifBanner) notifBanner.style.display = "none";
      }

      const cdBanner = document.getElementById("global-countdown-banner");
      if (data.countdown && data.countdown.target_date) {
        document.getElementById("global-countdown-title").textContent = data.countdown.title;
        cdBanner.style.display = "";

        if (window._cdInterval) clearInterval(window._cdInterval);
        window._cdInterval = setInterval(() => {
          const target = new Date(data.countdown.target_date).getTime();
          const now = new Date().getTime();
          const distance = target - now;
          if (distance < 0) {
            document.getElementById("global-countdown-timer").textContent = "RELEASED";
            return;
          }
          const days = Math.floor(distance / (1000 * 60 * 60 * 24));
          const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
          const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
          const seconds = Math.floor((distance % (1000 * 60)) / 1000);
          document.getElementById("global-countdown-timer").textContent = `${days}d ${hours}h ${minutes}m ${seconds}s`;
        }, 1000);
      } else {
        if(cdBanner) cdBanner.style.display = "none";
      }

      // If owner dashboard is visible, populate inputs with the selected lang config
      const dashboardView = document.getElementById("view-dashboard");
      if (dashboardView && dashboardView.classList.contains("active")) {
        const ownerData = await apiFetch(`/api/dashboard?action=config&lang=${lang}`);
        const notifInput = document.getElementById("dashboard-announcement");
        if (notifInput) notifInput.value = ownerData.notification || "";
        
        const cdTitleInput = document.getElementById("dashboard-countdown-title");
        const cdDateInput = document.getElementById("dashboard-countdown-date");
        if (cdTitleInput) cdTitleInput.value = (ownerData.countdown && ownerData.countdown.title) || "";
        if (cdDateInput) cdDateInput.value = (ownerData.countdown && ownerData.countdown.target_date) || "";
      }

      loadPolls();
    } catch (e) { }
  };

  window.saveDashboardConfig = async function saveDashboardConfig() {
    try {
      const lang = window.getDashboardLang();
      const notification = document.getElementById("dashboard-announcement").value;
      const title = document.getElementById("dashboard-countdown-title").value;
      const target_date = document.getElementById("dashboard-countdown-date").value;
      
      await apiFetch(`/api/dashboard?action=config&lang=${lang}`, {
        method: "PUT",
        body: JSON.stringify({ notification, countdown: { title, target_date } })
      });
      alert("Dashboard config saved!");
      loadDashboardConfig();
    } catch (e) {
      alert("Failed to save config: " + e.message);
    }
  };

  window.clearDashboardAnnouncement = function() {
    document.getElementById("dashboard-announcement").value = "";
  };

  window.clearDashboardTimer = function() {
    document.getElementById("dashboard-countdown-title").value = "";
    document.getElementById("dashboard-countdown-date").value = "";
  };

  // Polls Logic
  window.loadPolls = async function loadPolls() {
    try {
      const isJp = window.location.pathname.indexOf('-jp') !== -1;
      const displayLang = isJp ? "ja" : "en";
      const data = await apiFetch(`/api/polls?lang=${displayLang}`);
      
      const container = document.getElementById("global-polls-container");
      if (!container) return;

      let html = "";
      (data.polls || []).forEach(poll => {
        let optsHtml = "";
        poll.options.forEach(opt => {
          const votedKey = `voted_poll_${poll.id}`;
          const isVoted = localStorage.getItem(votedKey) === opt.id;
          const hasVotedAny = !!localStorage.getItem(votedKey);
          
          optsHtml += `
            <div class="poll-option ${isVoted ? 'voted' : ''}" onclick="votePoll('${poll.id}', '${opt.id}')" style="${hasVotedAny ? 'cursor:default;' : ''}">
              <span>${opt.option_text}</span>
              <span class="votes">${opt.votes}</span>
            </div>
          `;
        });
        html += `
          <div class="poll-card" id="poll-${poll.id}">
            <h3><strong>BiniFn:</strong> ${poll.question}</h3>
            <div class="poll-options">
              ${optsHtml}
            </div>
          </div>
        `;
      });
      container.innerHTML = html;

      // Populate dashboard active polls if owner
      const dashList = document.getElementById("dashboard-active-polls-list");
      if (dashList) {
        const lang = window.getDashboardLang();
        const ownerData = await apiFetch(`/api/polls?lang=${lang}`);
        let dashHtml = "";
        (ownerData.polls || []).forEach(poll => {
          dashHtml += `
            <div style="background:#222; padding:10px; margin-bottom:10px; border-radius:4px; border:1px solid #444;">
              <strong>${poll.question}</strong>
              <div class="poll-admin-controls">
                <button class="btn-clear" onclick="deletePoll('${poll.id}')">Delete Poll</button>
              </div>
            </div>
          `;
        });
        dashList.innerHTML = dashHtml;
      }
    } catch (e) { }
  };

  window.votePoll = async function votePoll(pollId, optionId) {
    const votedKey = `voted_poll_${pollId}`;
    if (localStorage.getItem(votedKey)) return; // Already voted

    try {
      await apiFetch("/api/polls", {
        method: "POST",
        body: JSON.stringify({ optionId })
      });
      localStorage.setItem(votedKey, optionId);
      loadPolls();
    } catch (e) {
      console.error("Vote failed", e);
    }
  };

  window.createPoll = async function createPoll() {
    try {
      const lang = window.getDashboardLang();
      const question = document.getElementById("dashboard-poll-question").value;
      const optsNodes = document.querySelectorAll(".dashboard-poll-opt");
      const options = Array.from(optsNodes).map(n => n.value).filter(v => v.trim() !== "");

      if (!question || options.length < 2) {
        alert("Please enter a question and at least 2 options.");
        return;
      }

      await apiFetch("/api/polls", {
        method: "PUT",
        body: JSON.stringify({ question, lang, options })
      });
      
      document.getElementById("dashboard-poll-question").value = "";
      optsNodes.forEach(n => n.value = "");
      alert("Poll created!");
      loadPolls();
    } catch (e) {
      alert("Failed to create poll: " + e.message);
    }
  };

  window.deletePoll = async function deletePoll(pollId) {
    if (!confirm("Are you sure you want to delete this poll?")) return;
    try {
      await apiFetch("/api/polls", {
        method: "DELETE",
        body: JSON.stringify({ id: pollId })
      });
      alert("Poll deleted.");
      loadPolls();
    } catch (e) {
      alert("Failed to delete poll: " + e.message);
    }
  };
'''

start = js.find('  window.loadDashboardConfig = async function loadDashboardConfig() {')
end = js.find('  window.loadDashboardArt = async function loadDashboardArt() {')

if start != -1 and end != -1:
    js = js[:start] + new_funcs + js[end:]
    with open('assets/phase1-client.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Replaced JS functions.")
else:
    print("Could not find start/end points.")
