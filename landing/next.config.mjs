/** @type {import('next').NextConfig} */
const MODAL_URL = process.env.MODAL_BACKEND_URL || "http://localhost:5000";
// PostHog EU region. Reverse-proxied through /ingest/* so adblockers
// (uBlock, AdGuard, Brave Shields) don't strip requests — they block
// *.posthog.com by default but leave first-party requests alone.
const POSTHOG_API    = "https://eu.i.posthog.com";
const POSTHOG_ASSETS = "https://eu-assets.i.posthog.com";

const nextConfig = {
  // skipTrailingSlashRedirect нужен для корректной работы PostHog API endpoints
  skipTrailingSlashRedirect: true,
  async rewrites() {
    return [
      // PostHog ingest — static assets и API endpoints. ВАЖНО: static ДО общего!
      { source: "/ingest/static/:path*", destination: `${POSTHOG_ASSETS}/static/:path*` },
      { source: "/ingest/:path*",        destination: `${POSTHOG_API}/:path*` },
      // Backend API (audio goes direct to Modal — bypasses 4MB Vercel edge limit)
      { source: "/api/:path*", destination: `${MODAL_URL}/api/:path*` },
    ];
  },
};

export default nextConfig;
