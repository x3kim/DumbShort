// in sw.js
const CACHE_NAME = "dumbshort-cache-v2"; // Version update to prevent caching issues. Because cache is never your friend.
const urlsToCache = ["/", "/static/css/output.css"];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log("Opened cache. Because you totally want this cached.");
      return cache.addAll(urlsToCache);
    })
  );
});

self.addEventListener("fetch", (event) => {
  // We only respond to GET requests. POST, PUT, etc. always go to the network. Because security or something.
  if (event.request.method !== "GET") {
    return;
  }

  event.respondWith(
    caches.match(event.request).then((response) => {
      // Cache hit - return response. Because why use the network if you don't have to?
      if (response) {
        return response;
      }
      // Not in cache, so fetch from the network. Welcome to the 21st century.
      return fetch(event.request);
    })
  );
});
