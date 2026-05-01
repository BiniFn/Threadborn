const pool = require("../lib/api/db");
const { allowCors, success, fail } = require("../lib/api/http");
const { parseJsonBody } = require("../lib/api/request");
const { requireSession, validateCsrf } = require("../lib/api/auth");

module.exports = async (req, res) => {
  if (allowCors(req, res)) {
    return;
  }

  try {
    await pool.ensureMigrations();

    // GET: Fetch active polls for a given language
    if (req.method === "GET") {
      const lang = req.query.lang || "en";
      const { rows: polls } = await pool.query(
        "select id, question, created_at from polls where is_active = true and lang = $1 order by created_at desc",
        [lang]
      );

      for (const poll of polls) {
        const { rows: options } = await pool.query(
          "select id, option_text, votes from poll_options where poll_id = $1 order by id asc",
          [poll.id]
        );
        poll.options = options;
      }

      return success(res, { polls });
    }

    // POST: Vote on a poll
    if (req.method === "POST") {
      const body = await parseJsonBody(req);
      const optionId = String(body.optionId || "");
      if (!optionId) return fail(res, 400, "Missing option ID");

      await pool.query(
        "update poll_options set votes = votes + 1 where id = $1",
        [optionId]
      );
      
      return success(res, { voted: true });
    }

    // Must be logged in as owner for PUT and DELETE
    const session = await requireSession(req, res, fail);
    if (!session) return;
    
    if (session.role !== "owner") {
      return fail(res, 403, "Only the owner can modify polls");
    }

    if (!validateCsrf(req, session)) {
      return fail(res, 403, "Invalid CSRF token");
    }

    // PUT: Create a new poll
    if (req.method === "PUT") {
      const body = await parseJsonBody(req);
      const question = String(body.question || "").trim();
      const lang = String(body.lang || "en").trim();
      const options = Array.isArray(body.options) ? body.options : [];

      if (!question || options.length < 2) {
        return fail(res, 400, "Poll must have a question and at least 2 options");
      }

      const { rows } = await pool.query(
        "insert into polls (question, lang, is_active) values ($1, $2, true) returning id",
        [question, lang]
      );
      const pollId = rows[0].id;

      for (const opt of options) {
        await pool.query(
          "insert into poll_options (poll_id, option_text, votes) values ($1, $2, 0)",
          [pollId, String(opt).trim()]
        );
      }

      return success(res, { created: true, pollId });
    }

    // DELETE: Remove a poll
    if (req.method === "DELETE") {
      const body = await parseJsonBody(req);
      const id = String(body.id || "");
      if (!id) return fail(res, 400, "Missing poll ID");

      await pool.query("delete from polls where id = $1", [id]);
      return success(res, { deleted: true });
    }

    return fail(res, 405, "Method not allowed");
  } catch (error) {
    return fail(res, 500, "Failed to manage polls");
  }
};
