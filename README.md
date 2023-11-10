# Bluesky Chrsitmas Countdown

This is a Christmas countdown bot, made for [Bluesky](https://bsky.app).

Everyday, this bot posts an image with how many days are left until Christmas.

## Account Link

The account is **[@xmas-countdown.bsky.social](https://bsky.app/profile/xmas-countdown.bsky.social)** drop it a follow ;)

Link: https://bsky.app/profile/xmas-countdown.bsky.social

## File Structure

- [`python`](https://github.com/Zoobdude/bluesky-chrsitmas-countdown/tree/main/python): adds the counter text and outputs to [`images`](https://github.com/Zoobdude/bluesky-chrsitmas-countdown/tree/main/images).
  - Every file should be a `.png`
  - The filename is the amount of days remaining
- [`typescript`](https://github.com/Zoobdude/bluesky-chrsitmas-countdown/tree/main/typescript): posts the images using the [Bluesky API](https://atproto.com/blog/create-post).
  - Runs from a [GitHub Action](https://github.com/Zoobdude/bluesky-chrsitmas-countdown/blob/main/.github/workflows/main.yml) every 24 hours

## Credits

- [@Zoobdude](https://github.com/Zoobdude) - did the Python
- [@YummyBacon5](https://github.com/YummyBacon5) - created the TypeScript
