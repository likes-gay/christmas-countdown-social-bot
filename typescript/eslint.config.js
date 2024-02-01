import tsParser from "@typescript-eslint/parser";
import tsPlugin from "@typescript-eslint/eslint-plugin";

export default [
	{
		files: ["**/*.ts", "**/*.js"],
		ignores: ["node_modules/**/*"],
		languageOptions: {
			parser: tsParser,
			ecmaVersion: "latest",
			sourceType: "module",
		},
		plugins: {
			typescript: tsPlugin,
		},
		rules: {
			//...tsPlugin.rules,
			indent: [
				"error",
				"tab",
			],
			"linebreak-style": [
				"error",
				"unix",
			],
			quotes: [
				"error",
				"double",
			],
			semi: [
				"error",
				"always",
			],
			"quote-props": [
				"error",
				"as-needed",
			],
			"keyword-spacing": [
				"error",
				{
					before: true,
					after: true,
					overrides: {
						if: { after: false },
						for: { after: false },
					},
				},
			],
			"comma-dangle": [
				"error",
				"always-multiline",
			],
			"typescript/no-unused-vars": "warn",
		},
	},
];