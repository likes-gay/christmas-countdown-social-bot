self.addEventListener("fetch", async (e) => {
	if(!e.request.url.endsWith("/currentImage.png")) return;

	const response = fetch(e.request);
	e.respondWith(response.then(x => x.clone()));
	const arrBuffer = await response.then(x => x.blob()).then(x => x.arrayBuffer());

	const client = await self.clients.get(e.clientId);
	client.postMessage({
		imageData: arrBuffer
	});
});