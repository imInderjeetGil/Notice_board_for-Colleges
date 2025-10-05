self.addEventListener('push', function (event) {
  const data = event.data.json();
  const title = data.title;
  const options = {
    body: data.body,
    icon: '/static/icons/notice.png',  // optional
    data: { url: data.url }
  };
  event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('notificationclick', function (event) {
  event.notification.close();
  event.waitUntil(clients.openWindow(event.notification.data.url));
});
