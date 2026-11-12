// Offline support for German Daily Review. Built by scripts/make.py.
const VERSION = 'gr-__VERSION__';
const FILES = __FILES__;

self.addEventListener('install', e => {
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k !== VERSION && k !== 'fonts').map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin === location.origin) {
    if (req.mode === 'navigate') {
      // Newest page when online, saved page when offline
      e.respondWith(fetch(req, {cache: 'no-store'}).catch(() => caches.match(req, {ignoreSearch: true}).then(r => r || caches.match('./')).then(r => r || caches.match('index.html'))));
      return;
    }
    // single-word recordings aren't saved up front; keep each one after its first play so it works offline
    e.respondWith(caches.match(req, {ignoreSearch: true}).then(r => r || fetch(req).then(res => {
      if (res.ok && url.pathname.includes('/audio/')) { const copy = res.clone(); caches.open(VERSION).then(c => c.put(req, copy)); }
      return res;
    })));
    return;
  }
  if (url.hostname.endsWith('fonts.googleapis.com') || url.hostname.endsWith('fonts.gstatic.com')) {
    e.respondWith(caches.open('fonts').then(c => c.match(req).then(r => r || fetch(req).then(res => { c.put(req, res.clone()); return res; }))));
  }
});
