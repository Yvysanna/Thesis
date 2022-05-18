// Required variables
let idx = 19;
const HUBS = "section[data-testid=home-page] section";
const SONGS = "section[data-testid=component-shelf] div[data-testid=grid-container]";
const IMGS = "img[data-testid=card-image]";
const LINKS = "a[data-testid=see-all-link]";

// Useful functions
const selectAll = (query, func) => Array.from(document.querySelectorAll(query)).map(s => func(s));
const selectOne = (query, func) => Array.from(document.querySelector(query).childNodes).map(s => func(s));
const innerText = (e) => e.innerText.split('\n').join(' ');


// Create database from query
if (location.href !== "https://open.spotify.com/") {
      let mySongs = selectOne(SONGS, (s) => [innerText(s), location.href, s.querySelector(IMGS).src]);
      console.log(mySongs);
      var db = openDatabase('mySpotifyDB', '1.0', 'Spotifiying to DB', 2 * 1024 * 1024); 
      db.transaction(function (tx) {   
          tx.executeSql('CREATE TABLE IF NOT EXISTS SONGS (name unique, img)'); 
          mySongs.forEach(song => tx.executeSql('INSERT INTO SONGS (name, img) VALUES (?, ?)', song));
      });
      history.back();
  } else {
      let myHubs = selectAll(HUBS, (s) => [s.ariaLabel, s.querySelector(LINKS)]);
      let next = myHubs[idx][1];
      console.log(next);
      var db = openDatabase('mySpotifyDB', '1.0', 'Spotifiying to DB', 2 * 1024 * 1024); 
      db.transaction(function (tx) {   
          tx.executeSql('CREATE TABLE IF NOT EXISTS HUBS (name unique, descr)');
          tx.executeSql('INSERT INTO HUBS (name, descr) VALUES (?, ?)', myHubs[idx]);
      });
      next?.click();
  }
