const crypto = require("crypto");
const { Pool } = require("pg");

const pool = new Pool({
  connectionString: process.env.DATABASE_URL
});

function parseJsonBody(req) {
  return new Promise((resolve, reject) => {
    let body = "";
    req.on("data", chunk => {
      body += chunk;
      if (body.length > 1_000_000) {
        reject(new Error("Request body too large"));
      }
    });
    req.on("end", () => {
      try {
        resolve(body ? JSON.parse(body) : {});
      } catch (error) {
        reject(new Error("Invalid JSON body"));
      }
    });
    req.on("error", reject);
  });
}

function makePasswordHash(rawPassword) {
  const salt = crypto.randomBytes(16);
  const key = crypto.scryptSync(rawPassword, salt, 64);
  return `scrypt$${salt.toString("hex")}$${key.toString("hex")}`;
}

module.exports = async (req, res) => {
  if (req.method !== "POST") {
    res.statusCode = 405;
    res.setHeader("Content-Type", "application/json");
    res.end(JSON.stringify({ error: "Method not allowed" }));
    return;
  }

  if (!process.env.DATABASE_URL) {
    res.statusCode = 503;
    res.setHeader("Content-Type", "application/json");
    res.end(JSON.stringify({ error: "Missing DATABASE_URL environment variable" }));
    return;
  }

  try {
    const body = await parseJsonBody(req);
    const email = String(body.email || "").trim().toLowerCase();
    const password = String(body.password || "");
    const displayName = String(body.displayName || "").trim();
    const avatarDataUrl = String(body.avatarDataUrl || "").trim();

    if (!email || !password || !displayName) {
      res.statusCode = 400;
      res.setHeader("Content-Type", "application/json");
      res.end(JSON.stringify({ error: "Display name, email and password are required" }));
      return;
    }

    const existing = await pool.query("select id from users where lower(email) = $1 limit 1", [email]);
    if (existing.rows.length) {
      res.statusCode = 409;
      res.setHeader("Content-Type", "application/json");
      res.end(JSON.stringify({ error: "Email already registered" }));
      return;
    }

    const passwordHash = makePasswordHash(password);
    const insert = await pool.query(
      "insert into users (email, password_hash, display_name, avatar_url) values ($1, $2, $3, $4) returning id, email, display_name, avatar_url",
      [email, passwordHash, displayName, avatarDataUrl || null]
    );

    const user = insert.rows[0];
    res.statusCode = 201;
    res.setHeader("Content-Type", "application/json");
    res.end(JSON.stringify({
      ok: true,
      user: {
        id: user.id,
        email: user.email,
        displayName: user.display_name || displayName,
        avatarUrl: user.avatar_url || avatarDataUrl || ""
      }
    }));
  } catch (error) {
    res.statusCode = 500;
    res.setHeader("Content-Type", "application/json");
    res.end(JSON.stringify({ error: "Signup failed", details: error.message }));
  }
};
