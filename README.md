# Chrsitmas Countdown Social Bot

This is a Christmas countdown bot. It posts an image with how many days are left until Christmas, on [Bluesky](https://bsky.app), each day.

The [`python`](https://github.com/likes-gay/bluesky-chrsitmas-countdown/tree/main/python) uses the [Unsplash random image API](https://unsplash.com/documentation#get-a-random-photo) to grab a random Christmas related image.
Then, it is fed to the [Python Pillow Library](https://pypi.org/project/pillow/) to dim the image, apply blur, and finally add the text. It is the finnaly saved as `currentImage.png`

The [`typescript`](https://github.com/likes-gay/bluesky-chrsitmas-countdown/tree/main/typescript) then posts the image made on the last step using the [Bluesky API](https://atproto.com/blog/create-post).

Both scripts are then run from a [GitHub Action](https://github.com/likes-gay/bluesky-chrsitmas-countdown/blob/main/.github/workflows/main.yml) every 24 hours.

## Account Link

The account is **[@xmas-countdown.likes.gay](https://bsky.app/profile/xmas-countdown.likes.gay)**, drop it a follow ;)

Link: https://bsky.app/profile/xmas-countdown.likes.gay

## Credits

- [@Zoobdude](https://github.com/Zoobdude) - did the Python
- [@YummyBacon5](https://github.com/YummyBacon5) - created the TypeScript
