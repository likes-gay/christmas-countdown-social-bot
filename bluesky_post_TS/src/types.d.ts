export type CreatedSessionResponse = {
	did: string;
	didDoc: {
		"@context": string[];
		id: string;
		alsoKnownAs: string[];
		verificationMethod: {
			id: string;
			type: string;
			controller: string;
			publicKeyMultibase: string;
		}[];
		service: {
			id: string;
			type: string;
			serviceEndpoint: string;
		}[];
	};
	handle: string;
	email: string;
	emailConfirmed: boolean;
	accessJwt: string;
	refreshJwt: string;
};

export type CreatedPostResponse = {
	uri: string;
	cid: string;
};

export type UploadedBlobResponse = {
	blob: {
		$type: "blob",
		ref: {
			$link: string;
		};
		mimeType: string;
		size: number;
	};
};

export type PostRecord = {
	repo: string;
	collection: "app.bsky.feed.post";
	record: {
		$type: "app.bsky.feed.post";
		text: string;
		createdAt: string;
		langs: string[];
		embed: {
			$type: "app.bsky.embed.images";
			images: {
				alt: string;
				image: UploadedBlobResponse["blob"];
			}[];
		};
	};
};

export type ErrorResponse = {
	error: string;
	message: string;
};

export type AuthTokens = {
	identifier: string;
	password: string;
};