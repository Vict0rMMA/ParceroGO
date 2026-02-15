var CACHE_NAME = 'delivery-v1';
var STATIC_URLS = ['/static/style.css', '/static/theme.js', '/static/alerts.js', '/static/delivery-services.js', '/static/delivery.js', '/'];

self.addEventListener('install', function (e) {
    e.waitUntil(
        caches.open(CACHE_NAME)
            .then(function (cache) { return cache.addAll(STATIC_URLS.filter(Boolean)); })
            .then(function () { return self.skipWaiting(); })
    );
});

self.addEventListener('activate', function (e) {
    e.waitUntil(
        caches.keys().then(function (keys) {
            return Promise.all(
                keys.filter(function (k) { return k !== CACHE_NAME; }).map(function (k) { return caches.delete(k); })
            );
        }).then(function () { return self.clients.claim(); })
    );
});

self.addEventListener('fetch', function (e) {
    e.respondWith(
        caches.match(e.request).then(function (r) { return r || fetch(e.request); })
    );
});

self.addEventListener('push', function (e) {
    var data = e.data ? e.data.json() : {};
    var title = data.title || 'Delivery';
    var opts = { body: data.body || '', icon: '/static/logo.png', badge: '/static/logo.png' };
    e.waitUntil(self.registration.showNotification(title, opts));
});
