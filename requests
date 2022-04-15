// Required variables
const HUBS = "section[data-testid=home-page] section";
const SONGS = "section[data-testid=component-shelf] div[data-testid=grid-container]";
const IMGS = "img[data-testid=card-image]";
const LINKS = "a[data-testid=see-all-link]";

// Useful functions
const selectAll = (query, func) => Array.from(document.querySelectorAll(query)).map(s => func(s));
const selectOne = (query, func) => Array.from(document.querySelector(query).childNodes).map(s => func(s));
const innerText = (e) => e.innerText.split('\n').join(' ');

let myHubs = selectAll(HUBS, (s) => [s.ariaLabel, s.querySelector(LINKS)]);

// Then call:
myHubs[1][1].click()

// After click: redefine variable
const mySongs = selectOne(SONGS, (s) => [innerText(s), s.querySelector(IMGS)])
