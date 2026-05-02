const { allowCors, success, fail } = require("../../lib/api/http");
const { getClientIp } = require("../../lib/api/request");
const { takeRateLimitToken } = require("../../lib/api/rate-limit");
const { destroySession } = require("../../lib/api/auth");

module.exports = async (req, res) => {
  if (allowCors(req, res)) {
    return;
  }
  if (req.method !== "POST") {
    fail(res, 405, "Method not allowed");
    return;
  }
  if (!takeRateLimitToken(`logout:${getClientIp(req)}`, 10, 60_000)) {
    fail(res, 429, "Too many requests");
    return;
  }
  await destroySession(req, res);
  success(res, { loggedOut: true });
};
