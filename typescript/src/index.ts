import fs from "fs";
import { SessionInfo, CreatedPostResponse, UploadedBlobResponse, ErrorResponse, PostRecord, AuthTokens } from "./types";
import "dotenv/config";
import path from "path";

const BSKY_URL = "https://bsky.social";

const oneDayInMs = 24 * 60 * 60 * 1000;
const todayDate = new Date().getTime();
const christmasDate = new Date(new Date().getFullYear(), 11, 25).getTime();
const daysUntilChristmas = Math.round(Math.abs((christmasDate - todayDate) / oneDayInMs));

const createdSession: SessionInfo = await fetch(`${BSKY_URL}/xrpc/com.atproto.server.createSession`, {
	headers: {
		"Content-Type": "application/json"
	},
	body: JSON.stringify({
		identifier: process.env.HANDLE!,
		password: process.env.PASSWORD!
	} as AuthTokens),
	method: "POST"
}).then(x => x.json());

const imageFileRead = fs.readFileSync(
	path.resolve(`./../images/${daysUntilChristmas}.png`)
);
const accessToken = "Bearer " + createdSession.accessJwt;

const createdBlob: UploadedBlobResponse = await fetch(`${BSKY_URL}/xrpc/com.atproto.repo.uploadBlob`, {
	headers: {
		Authorization: accessToken,
		"Content-Type": "image/x-png"
	},
	body: imageFileRead,
	method: "POST"
}).then(x => x.json());

const createdPost = await fetch(`${BSKY_URL}/xrpc/com.atproto.repo.createRecord`, {
	headers: {
		Authorization: accessToken,
		"Content-Type": "application/json"
	},
	body: JSON.stringify({
		repo: createdSession.did,
		collection: "app.bsky.feed.post",
		record: {
			$type: "app.bsky.feed.post",
			text: `There ${daysUntilChristmas == 1 ? "is" : "are"} ${daysUntilChristmas} ${daysUntilChristmas == 1 ? "day" : "days"} until Christmas!`,
			createdAt: new Date().toISOString(),
			langs: ["en-GB"],
			embed: {
				$type: "app.bsky.embed.images",
				images: [{
					alt: `${daysUntilChristmas} ${daysUntilChristmas == 1 ? "day" : "days"} until Christmas!`,
					image: createdBlob.blob
				}]
			}
		}
	} as PostRecord),
	method: "POST"
});

if(createdPost.ok) {
	const createdPostJson: CreatedPostResponse = await createdPost.json();

	console.log(`Post created!\nLink: https://bsky.app/profile/${createdSession.handle}/post/${createdPostJson.uri.split("/").at(-1)}`);
	process.exit(0);
}

const createdPostJson: ErrorResponse = await createdPost.json();

console.error(`Creating the post has failed!\nError type: \`${createdPostJson.error}\`\nError message: \`${createdPostJson.message}\``);
process.exit(1);