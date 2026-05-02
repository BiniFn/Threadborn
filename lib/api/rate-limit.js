// NOTE: On Vercel serverless, each function instance has its own in-process Map.
// This provides best-effort rate limiting within a warm instance.
// For persistent cross-instance rate limiting, use an external store (e.g. Upstash Redis).
const buckets = new Map();

function takeRateLimitToken(key, limit = 20, windowMs = 60_000) {
  const now = Date.now();

  // Prune expired buckets to prevent unbounded memory growth
  if (buckets.size > 500) {
    for (const [k, v] of buckets) {
      if (now > v.resetAt) {
        buckets.delete(k);
      }
    }
  }

  const bucket = buckets.get(key) || { count: 0, resetAt: now + windowMs };
  if (now > bucket.resetAt) {
    bucket.count = 0;
    bucket.resetAt = now + windowMs;
  }
  bucket.count += 1;
  buckets.set(key, bucket);
  return bucket.count <= limit;
}

module.exports = { takeRateLimitToken };
