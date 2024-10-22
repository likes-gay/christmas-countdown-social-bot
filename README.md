# Chrsitmas Countdown Social Bot

This is a Christmas countdown bot. It posts an image each day with how many days are left until Christmas, on various sites

## How it works
[`image_gen_PY`](https://github.com/likes-gay/christmas-countdown-social-bot/tree/main/image_gen_PY) uses the [Unsplash random image API](https://unsplash.com/documentation#get-a-random-photo) to grab a random Christmas related image.
Then, it is fed to the [Python Pillow Library](https://pypi.org/project/pillow/) to dim the image, apply blur, and finally add the text. It is the finnaly saved as `currentImage.png`

[`bluesky_post_TS`](https://github.com/likes-gay/christmas-countdown-social-bot/tree/main/bluesky_post_TS) then posts the image made on the last step using the [Bluesky API](https://atproto.com/blog/create-post).

[`threads_post_PY`](https://github.com/likes-gay/christmas-countdown-social-bot/tree/main/threads_post_PY) uses the [Threads API](https://developers.facebook.com/docs/threads/) to post the image made on the first step.

All the scripts are then run from a [GitHub Action](https://github.com/likes-gay/christmas-countdown-social-bot/blob/main/.github/workflows/main.yml) every 24 hours.

## Account Links

## Bluesky
[@xmas-countdown.likes.gay](https://bsky.app/profile/xmas-countdown.likes.gay)

## Threads
[@daily_xmas_countdown](https://www.threads.net/@daily_xmas_countdown)

## Credits

- [@Zoobdude](https://github.com/Zoobdude) - did the Python
- [@YummyBacon5](https://github.com/YummyBacon5) - created the TypeScript
