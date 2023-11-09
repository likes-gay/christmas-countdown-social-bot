import fs from "fs";

const oneDayInMs = 24 * 60 * 60 * 1000;
const todayDate = new Date().getTime();
const christmasDate = new Date(2023, 12, 25).getTime();

console.log(
	Math.round(Math.abs((christmasDate - todayDate) / oneDayInMs))
);