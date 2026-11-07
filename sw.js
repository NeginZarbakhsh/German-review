// Offline support for German Daily Review. Built by scripts/make.py.
const VERSION = 'gr-608ad1ea23';
const FILES = ["./", "index.html", "manifest.json", "icon-180.png", "icon-192.png", "icon-512.png", "icon-maskable-512.png", "audio/02d3543a_n.mp3", "audio/02d3543a_s.mp3", "audio/07b595ff_n.mp3", "audio/07b595ff_s.mp3", "audio/0998e93d_n.mp3", "audio/0998e93d_s.mp3", "audio/0c5e7833_n.mp3", "audio/0c5e7833_s.mp3", "audio/0c607794_n.mp3", "audio/0c607794_s.mp3", "audio/13a91a92_n.mp3", "audio/13a91a92_s.mp3", "audio/15d55d08_n.mp3", "audio/15d55d08_s.mp3", "audio/188f7740_n.mp3", "audio/188f7740_s.mp3", "audio/1d8d2fd0_n.mp3", "audio/1d8d2fd0_s.mp3", "audio/1ecfdb80_n.mp3", "audio/1ecfdb80_s.mp3", "audio/2a357b0d_n.mp3", "audio/2a357b0d_s.mp3", "audio/2a8f72d1_n.mp3", "audio/2a8f72d1_s.mp3", "audio/35d03aba_n.mp3", "audio/35d03aba_s.mp3", "audio/37a6259c_n.mp3", "audio/37a6259c_s.mp3", "audio/37ab88fd_n.mp3", "audio/37ab88fd_s.mp3", "audio/41a71d2d_n.mp3", "audio/41a71d2d_s.mp3", "audio/46190b1d_n.mp3", "audio/46190b1d_s.mp3", "audio/46d66112_n.mp3", "audio/46d66112_s.mp3", "audio/4c0d5d15_n.mp3", "audio/4c0d5d15_s.mp3", "audio/4e413d7c_n.mp3", "audio/4e413d7c_s.mp3", "audio/4ee27f66_n.mp3", "audio/4ee27f66_s.mp3", "audio/4fdb7d53_n.mp3", "audio/4fdb7d53_s.mp3", "audio/522b906e_n.mp3", "audio/522b906e_s.mp3", "audio/53d24305_n.mp3", "audio/53d24305_s.mp3", "audio/54c22cfe_n.mp3", "audio/54c22cfe_s.mp3", "audio/54d1c041_n.mp3", "audio/54d1c041_s.mp3", "audio/55076223_n.mp3", "audio/55076223_s.mp3", "audio/5773f520_n.mp3", "audio/5773f520_s.mp3", "audio/60dbf8b1_n.mp3", "audio/60dbf8b1_s.mp3", "audio/62e43be6_n.mp3", "audio/62e43be6_s.mp3", "audio/66dde6f5_n.mp3", "audio/66dde6f5_s.mp3", "audio/6a9809a7_n.mp3", "audio/6a9809a7_s.mp3", "audio/6c436b9e_n.mp3", "audio/6c436b9e_s.mp3", "audio/6d376bb2_n.mp3", "audio/6d376bb2_s.mp3", "audio/7170c6f7_n.mp3", "audio/7170c6f7_s.mp3", "audio/719de76f_n.mp3", "audio/719de76f_s.mp3", "audio/71b85371_n.mp3", "audio/71b85371_s.mp3", "audio/7919a9a3_n.mp3", "audio/7919a9a3_s.mp3", "audio/7d992d27_n.mp3", "audio/7d992d27_s.mp3", "audio/836a4330_n.mp3", "audio/836a4330_s.mp3", "audio/83df7789_n.mp3", "audio/83df7789_s.mp3", "audio/85e84816_n.mp3", "audio/85e84816_s.mp3", "audio/87c39f3f_n.mp3", "audio/87c39f3f_s.mp3", "audio/887fa92d_n.mp3", "audio/887fa92d_s.mp3", "audio/8bc0089f_n.mp3", "audio/8bc0089f_s.mp3", "audio/8c7ec1df_n.mp3", "audio/8c7ec1df_s.mp3", "audio/8d34393e_n.mp3", "audio/8d34393e_s.mp3", "audio/8ebc81d8_n.mp3", "audio/8ebc81d8_s.mp3", "audio/9146d530_n.mp3", "audio/9146d530_s.mp3", "audio/92e0e7b7_n.mp3", "audio/92e0e7b7_s.mp3", "audio/93896dcd_n.mp3", "audio/93896dcd_s.mp3", "audio/95132cbf_n.mp3", "audio/95132cbf_s.mp3", "audio/951d2d62_n.mp3", "audio/951d2d62_s.mp3", "audio/9e78c0e3_n.mp3", "audio/9e78c0e3_s.mp3", "audio/a2407d33_n.mp3", "audio/a2407d33_s.mp3", "audio/a31a9574_n.mp3", "audio/a31a9574_s.mp3", "audio/a50497d5_n.mp3", "audio/a50497d5_s.mp3", "audio/aab4b125_n.mp3", "audio/aab4b125_s.mp3", "audio/b062c153_n.mp3", "audio/b062c153_s.mp3", "audio/b14b3253_n.mp3", "audio/b14b3253_s.mp3", "audio/b3133dea_n.mp3", "audio/b3133dea_s.mp3", "audio/b71a7f24_n.mp3", "audio/b71a7f24_s.mp3", "audio/c02de53f_n.mp3", "audio/c02de53f_s.mp3", "audio/c337a1d9_n.mp3", "audio/c337a1d9_s.mp3", "audio/c91fd798_n.mp3", "audio/c91fd798_s.mp3", "audio/d1bf9329_n.mp3", "audio/d1bf9329_s.mp3", "audio/d4e99899_n.mp3", "audio/d4e99899_s.mp3", "audio/e0e5c799_n.mp3", "audio/e0e5c799_s.mp3", "audio/e23a0818_n.mp3", "audio/e23a0818_s.mp3", "audio/e84b72ac_n.mp3", "audio/e84b72ac_s.mp3", "audio/f3257bd6_n.mp3", "audio/f3257bd6_s.mp3", "audio/f6561635_n.mp3", "audio/f6561635_s.mp3", "audio/faf3bb92_n.mp3", "audio/faf3bb92_s.mp3", "voices/chris/07b595ff-270dcc9a.mp3", "voices/chris/0998e93d-2ed9f8af.mp3", "voices/chris/13a91a92-10bfb883.mp3", "voices/chris/15d55d08-6a6ec33a.mp3", "voices/chris/1d8d2fd0-33696097.mp3", "voices/chris/1ecfdb80-ed11dc51.mp3", "voices/chris/22c276a0-9805909e.mp3", "voices/chris/2a357b0d-7bae53ad.mp3", "voices/chris/35d03aba-16518034.mp3", "voices/chris/37a6259c-d256c2fd.mp3", "voices/chris/37ab88fd-ed85bc38.mp3", "voices/chris/41a71d2d-b48b77b5.mp3", "voices/chris/54c22cfe-a08407e9.mp3", "voices/chris/54d1c041-3a7bc40e.mp3", "voices/chris/57a5dc8f-f2b8d387.mp3", "voices/chris/6c436b9e-5b54bc88.mp3", "voices/chris/b062c153-edc8fb54.mp3", "voices/chris/d1bf9329-88c6e899.mp3", "voices/negin/2a8f72d1-eb4ce6e7.mp3", "voices/negin/41a71d2d-e2726bac.mp3", "voices/negin/4fdb7d53-77ff5693.mp3", "voices/negin/54c22cfe-fded3879.mp3", "voices/negin/719de76f-715b7e0c.mp3", "voices/negin/d1bf9329-6ca0aa2c.mp3"];

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
    e.respondWith(caches.match(req, {ignoreSearch: true}).then(r => r || fetch(req)));
    return;
  }
  if (url.hostname.endsWith('fonts.googleapis.com') || url.hostname.endsWith('fonts.gstatic.com')) {
    e.respondWith(caches.open('fonts').then(c => c.match(req).then(r => r || fetch(req).then(res => { c.put(req, res.clone()); return res; }))));
  }
});
