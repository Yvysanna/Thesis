function doClick(index) {
    
    // Recreate variables because with navigation / click they disappear
    const HUBS = "section[data-testid=home-page] section";
    const PLAYLISTS = "section div[data-testid=grid-container]";
    const IMGS = "img[data-testid=card-image]";
    const LINKS = "a[data-testid=see-all-link]";

    
    const selectAll = (query, func) => Array.from(document.querySelectorAll(query)).map(s => func(s));
    const selectOne = (query, func) => Array.from(document.querySelector(query).childNodes).map(s => func(s));
    const innerText = (e) => e.innerText.split('\n').join(' ');
    const href = location.href; 
    if (href !== "https://open.spotify.com/") {
        let myPlaylists = selectOne(PLAYLISTS, (s) => [innerText(s), href, s.querySelector(IMGS).src, s.querySelector('a').href]);
        console.log(myPlaylists);
        var db = openDatabase('mySpotifyDB', '1.0', 'Spotifiying to DB', 2 * 1024 * 1024); 
        db.transaction(function (tx) {   
            tx.executeSql('CREATE TABLE IF NOT EXISTS PLAYLIST (name, href, img, listid)'); 
            myPlaylists.forEach(playlist => tx.executeSql('INSERT INTO PLAYLIST (name, href, img, listid) VALUES (?, ?, ?, ?)', playlist));
        }, err => {console.log(err); history.back()}, suc => {console.log(suc), history.back()});
    } else {
        let myHubs = selectAll(HUBS, (s) => [s.ariaLabel, s.querySelector(LINKS)]);
        var db = openDatabase('mySpotifyDB', '1.0', 'Spotifiying to DB', 2 * 1024 * 1024);
        let next = null;
        db.transaction(function (tx) {   
            tx.executeSql('CREATE TABLE IF NOT EXISTS HUBS (name unique, descr)');
            tx.executeSql('SELECT name FROM HUBS', [], (tx, rs) => {
                const rows = Array.from(rs.rows);
                next = myHubs.find(hub => !rows.find(row => row.name == hub[0]));
                if (next) {
                    tx.executeSql('INSERT INTO HUBS (name, descr) VALUES (?, ?)', next, (tx, rs) => {
                        console.log(next);
                        if (!next[1]) {
                            const sel = `section[data-testid=home-page] section[aria-label='${next[0]}'] div[data-testid=grid-container]`;
                            const hubs = selectOne(sel, (s) => [innerText(s), href, s.querySelector(IMGS).src, s.querySelector('a').href]);
                            console.log('DOES THIS WORK?', hubs)
                            hubs.forEach(playlist => tx.executeSql('INSERT INTO PLAYLIST (name, href, img, listid) VALUES (?, ?, ?, ?)', playlist));
                        }
                    });
                };
            });
        }, err => console.log(err), suc => {next ? next[1]?.click() : () => null;});
    }
}
doClick(1);
