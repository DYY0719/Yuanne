// Yuanne Service Worker - PWA 离线缓存
const CACHE_NAME = 'yuanne-v1';
const CACHE_URLS = [
  '/',
  '/static/manifest.json',
  '/static/icon-192.png',
  '/static/icon-512.png',
  '/static/avatar.jpg',
  '/static/ima.jpg'
];

// 安装：预缓存静态资源
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(CACHE_URLS))
  );
  self.skipWaiting();
});

// 激活：清理旧缓存
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(
      keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
    ))
  );
  self.clients.claim();
});

// 请求拦截：缓存优先，API 走网络
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);
  // API 请求：仅走网络
  if (url.pathname.startsWith('/api/')) {
    return;
  }
  // 静态资源：缓存优先
  event.respondWith(
    caches.match(event.request).then((cached) => cached || fetch(event.request))
  );
});
