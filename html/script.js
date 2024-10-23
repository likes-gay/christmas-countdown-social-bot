navigator.serviceWorker.register("service-worker.js");

const image = document.querySelector("img[src=currentImage\\.png]");

navigator.serviceWorker.addEventListener("message", async (e) => {
    if(!e.data.imageData) return;
    const tags = await ExifReader.load(e.data.imageData);
    
    const altText = tags["alt_text"]?.description;

    if(!altText) {
        console.error("No alt text found in image, using default alt text.");
        return;
    }
    
    image.alt = altText;
    image.title = altText;
});