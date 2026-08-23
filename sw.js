/*
 * PRISM-Edge service worker — the site itself is offline-first.
 * Cache-first for static assets; network fallback. Version bump
 * invalidates old caches on deploy.
 */
const CACHE = "prism-edge-v3";
const ASSETS = [
  "./",
  "index.html",
  "demo/index.html",
  "favicon.svg",
  "manifest.json"
];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  if (e.request.method !== "GET") return;
  const url = new URL(e.request.url);
  // Navigations & JSON: network-first so deploys are visible immediately,
  // falling back to cache only when offline (the whole point of this site).
  const networkFirst =
    e.request.mode === "navigate" || url.pathname.endsWith(".json");
  if (networkFirst){
    e.respondWith(
      fetch(e.request)
        .then((resp) => {
          if (resp.ok && url.origin === self.location.origin){
            const copy = resp.clone();
            caches.open(CACHE).then((c) => c.put(e.request, copy));
          }
          return resp;
        })
        .catch(() => caches.match(e.request).then((hit) => hit || caches.match("index.html")))
    );
    return;
  }
  // Static assets: cache-first.
  e.respondWith(
    caches.match(e.request).then(
      (hit) =>
        hit ||
        fetch(e.request).then((resp) => {
          if (resp.ok && url.origin === self.location.origin){
            const copy = resp.clone();
            caches.open(CACHE).then((c) => c.put(e.request, copy));
          }
          return resp;
        })
    )
  );
});
