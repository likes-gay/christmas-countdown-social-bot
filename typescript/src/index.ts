import { CreatedSessionResponse, CreatedPostResponse, UploadedBlobResponse, ErrorResponse, PostRecord, AuthTokens } from "./types";
import core from "@actions/core";
import path from "path";
import fs from "fs";
import "dotenv/config";

console.log("Handle: ", process.env.HANDLE);
console.log("Password: ", process.env.BSKY_PASSWORD);
console.log(process.env);

const BSKY_URL = "https://bsky.social";

const todayDate = new Date();
const christmasDate = new Date(todayDate.getFullYear(), 11, 25).getTime();

const daysUntilChristmas = Math.ceil(
	(christmasDate - todayDate.getTime()) / (24 * 60 * 60 * 1000)
);

async function fetchWithError(url: string, ops?: RequestInit): Promise<Response> {
	const res = await fetch(url, ops);
	if(res.ok) return res;

	const resJson: ErrorResponse = await res.json();
	const errorMsg = {
		url,
		reqBody: ops?.body,
		resBody: resJson,
	};

	if(process.env.GITHUB_ACTIONS == "true") {
		core.setFailed(errorMsg.toString());
	} else {
		console.error(errorMsg);
	}
	
	process.exit(1);
}

const createdSession: CreatedSessionResponse = await fetchWithError(`${BSKY_URL}/xrpc/com.atproto.server.createSession`, {
	headers: {
		"Content-Type": "application/json"
	},
	body: JSON.stringify({
		identifier: process.env.HANDLE!,
		password: process.env.BSKY_PASSWORD!
	} as AuthTokens),
	method: "POST"
}).then(x => x.json());

const imageFileRead = fs.readFileSync(
	path.resolve(`./../currentImage.png`)
);
const accessToken = "Bearer " + createdSession.accessJwt;

const createdBlob: UploadedBlobResponse = await fetchWithError(`${BSKY_URL}/xrpc/com.atproto.repo.uploadBlob`, {
	headers: {
		Authorization: accessToken,
		"Content-Type": "image/png"
	},
	body: imageFileRead,
	method: "POST"
}).then(x => x.json());

let postText: string;
const daysText = `${daysUntilChristmas} ${daysUntilChristmas == 1 ? "day" : "days"}`;

const christmasEmojis = ["🎄", "🎅", "🎁", "❄️", "⛄", "🔔", "🕯️", "🌟", "🎉", "🦌", "🤶", "🍪", "🥛", "🎶", "👼", "🍭", "🎀", "🦌", "🏡", "🌲", "🍬", "🧦", "🎊", "🛷", "🔥", "🎁"];
const twoRandomEmojis = `${christmasEmojis[Math.floor(Math.random() * christmasEmojis.length)]}${christmasEmojis[Math.floor(Math.random() * christmasEmojis.length)]}`;

if(daysUntilChristmas !== 0) {
	postText = `There ${daysUntilChristmas == 1 ? "is" : "are"} ${daysText} until Christmas! ${twoRandomEmojis}`;
} else {
	postText = `CHRISTMAS IS TODAY!\n\nMerry ${todayDate.getFullYear()} Christmas! ${twoRandomEmojis}`;
}

const createdPost: CreatedPostResponse = await fetchWithError(`${BSKY_URL}/xrpc/com.atproto.repo.createRecord`, {
	headers: {
		Authorization: accessToken,
		"Content-Type": "application/json"
	},
	body: JSON.stringify({
		repo: createdSession.did,
		collection: "app.bsky.feed.post",
		record: {
			$type: "app.bsky.feed.post",
			text: postText,
			createdAt: new Date().toISOString(),
			langs: ["en-GB"],
			embed: {
				$type: "app.bsky.embed.images",
				images: [{
					alt: `${daysText} until Christmas!`,
					image: createdBlob.blob
				}]
			}
		}
	} as PostRecord),
	method: "POST"
}).then(x => x.json());

console.log(`Post created!\nLink: https://bsky.app/profile/${createdSession.handle}/post/${createdPost.uri.split("/").at(-1)}`);