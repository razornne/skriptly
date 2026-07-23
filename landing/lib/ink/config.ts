// Studio app config (/app). Values mirror modal_app.py.

// API goes straight to Modal, bypassing the Vercel proxy: Vercel Edge has a
// ~4MB body limit on proxied requests, and audio uploads routinely exceed it.
// CORS is open on the Flask side. Point this at your own deployed backend.
export const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:5000";

// Public client-side Supabase keys (safe to expose, access is gated by RLS).
// Set these in your own Supabase project — see .env.example.
export const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL || "";
export const SUPABASE_ANON_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || "";

export const SUPPORTED_LANGUAGES = [
  { value: "", label: "Auto" },
  { value: "en", label: "EN" },
  { value: "ru", label: "RU" },
  { value: "uk", label: "UK" },
  { value: "pl", label: "PL" },
] as const;
