// in sw.js
const CACHE_NAME = "dumbshort-cache-v2"; // Version update to prevent caching issues
const urlsToCache = ["/", "/static/css/output.css"];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log("Opened cache");
      return cache.addAll(urlsToCache);
    })
  );
});

self.addEventListener("fetch", (event) => {
  // We only respond to GET requests. POST, PUT, etc. always go to the network.
  if (event.request.method !== "GET") {
    return;
  }

  event.respondWith(
    caches.match(event.request).then((response) => {
      // Cache hit - return response
      if (response) {
        return response;
      }
      // Not in cache, so fetch from the network
      return fetch(event.request);
    })
  );
});
