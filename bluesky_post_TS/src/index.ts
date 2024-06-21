import { CreatedSessionResponse, CreatedPostResponse, UploadedBlobResponse, ErrorResponse, PostRecord, AuthTokens } from "./types";
import core from "@actions/core";
import path from "path";
import fs from "fs";
import ExifReader from 'exifreader';
import "dotenv/config";

const BSKY_URL = "https://bsky.social";

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
		core.setFailed(JSON.stringify(errorMsg));
	} else {
		console.error(errorMsg);
	}
	
	process.exit(1);
}

const createdSession: CreatedSessionResponse = await fetchWithError(`${BSKY_URL}/xrpc/com.atproto.server.createSession`, {
	headers: {
		"Content-Type": "application/json",
	},
	body: JSON.stringify({
		identifier: process.env.BSKY_HANDLE!,
		password: process.env.BSKY_PASSWORD!,
	} as AuthTokens),
	method: "POST",
}).then(x => x.json());

const imageFileRead = fs.readFileSync(
	path.resolve("./../currentImage.png"),
);

const tags = ExifReader.load(imageFileRead);

const caption = tags['caption'].description;
const numDays = tags['days_until_christmas'].description;

const accessToken = "Bearer " + createdSession.accessJwt;

const createdBlob: UploadedBlobResponse = await fetchWithError(`${BSKY_URL}/xrpc/com.atproto.repo.uploadBlob`, {
	headers: {
		Authorization: accessToken,
		"Content-Type": "image/png",
	},
	body: imageFileRead,
	method: "POST",
}).then(x => x.json());

const createdPost: CreatedPostResponse = await fetchWithError(`${BSKY_URL}/xrpc/com.atproto.repo.createRecord`, {
	headers: {
		Authorization: accessToken,
		"Content-Type": "application/json",
	},
	body: JSON.stringify({
		repo: createdSession.did,
		collection: "app.bsky.feed.post",
		record: {
			$type: "app.bsky.feed.post",
			text: caption,
			createdAt: new Date().toISOString(),
			langs: ["en-GB"],
			embed: {
				$type: "app.bsky.embed.images",
				images: [{
					alt: `${numDays} until Christmas!`,
					image: createdBlob.blob,
				}],
			},
		},
	} as PostRecord),
	method: "POST",
}).then(x => x.json());

console.log(`Post created!\nLink: https://bsky.app/profile/${createdSession.handle}/post/${createdPost.uri.split("/").at(-1)}`);