# Project Context

- Threadborn deploys on the Vercel Hobby plan, so keep serverless API code consolidated in `api/index.js`. Do not add new files under `api/` unless the user explicitly changes this rule.

# Architecture Decisions

- Add new backend routes by registering them inside the existing `api/index.js` router and reuse shared helpers from `lib/api/*`.

