css_to_append = """

/* Dashboard & Global Banners */
.global-banner {
  background: linear-gradient(135deg, rgba(20,20,30,0.9) 0%, rgba(30,20,40,0.9) 100%);
  border: 1px solid rgba(138, 43, 226, 0.4);
  color: #fff;
  padding: 12px 16px;
  text-align: center;
  font-weight: 500;
  margin-bottom: 16px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.4);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  animation: fade-in 0.3s ease-out;
}

.poll-card {
  background: rgba(20,20,20,0.8);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.poll-card h3 {
  margin-top: 0;
  margin-bottom: 12px;
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.25rem;
  color: #fff;
}

.poll-option {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  margin-bottom: 8px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.poll-option:hover {
  background: rgba(138, 43, 226, 0.2);
  border-color: rgba(138, 43, 226, 0.5);
}

.poll-option.voted {
  background: rgba(138, 43, 226, 0.3);
  border-color: rgba(138, 43, 226, 0.8);
}

.poll-option span.votes {
  font-family: 'Space Mono', monospace;
  font-size: 0.85rem;
  color: #aaa;
}

.poll-admin-controls {
  margin-top: 12px;
  text-align: right;
}

.btn-clear {
  background: transparent;
  border: 1px solid rgba(255, 50, 50, 0.6);
  color: #ff6b6b;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.2s;
}

.btn-clear:hover {
  background: rgba(255, 50, 50, 0.1);
}

.input-row {
  display: flex;
  gap: 8px;
  align-items: center;
  margin-bottom: 12px;
}
.input-row input {
  flex: 1;
  margin-bottom: 0 !important;
}
"""

with open('global.css', 'a') as f:
    f.write(css_to_append)

print("CSS appended to global.css")
