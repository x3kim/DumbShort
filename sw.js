const CACHE_NAME = "dumbshort-cache-v1";
const urlsToCache = [
  "/",
  "/static/css/output.css",
  "/templates/404.html",
  // Wir cachen das JavaScript nicht, da es inline in der index.html ist.
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log("Opened cache");
      return cache.addAll(urlsToCache);
    })
  );
});

self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      // Cache hit - return response
      if (response) {
        return response;
      }
      return fetch(event.request);
    })
  );
});
