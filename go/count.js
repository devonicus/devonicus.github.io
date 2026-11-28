// Counts visits to the devonicus.com/go/<game> share links (owner, 28 Nov 2026): which game, which link source (?src=),
// and the kind of device (iPhone/iPad, Android or computer). No cookies, nothing stored on the device, nothing about
// the visitor: each visit gets a fresh random id, so visits can't be linked to a person or to each other.
(function () {
  var APP = "BA3E2A13-68F4-4C51-ADEB-F9E531D21B18"; // TelemetryDeck: Devonicus games (shared)
  var game = (location.pathname.split("/")[2] || "").slice(0, 40);
  var src = (new URLSearchParams(location.search).get("src") || "direct").replace(/[^a-z0-9_-]/gi, "").slice(0, 40) || "direct";
  var ua = navigator.userAgent || "";
  var device = /iPhone|iPad|iPod/.test(ua) || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1) ? "iOS" : /Android/.test(ua) ? "Android" : "computer";
  var rnd = function () { var a = new Uint8Array(16); (window.crypto || {}).getRandomValues ? crypto.getRandomValues(a) : a.forEach(function (_, i) { a[i] = Math.random() * 256; }); return Array.prototype.map.call(a, function (b) { return ("0" + b.toString(16)).slice(-2); }).join(""); };
  var sent = false;
  function ping() {
    if (sent) return Promise.resolve(); sent = true;
    var body = JSON.stringify([{ appID: APP, clientUser: rnd(), sessionID: rnd(), type: "Web.goVisit", payload: { game: game, src: src, device: device } }]);
    try { return fetch("https://nom.telemetrydeck.com/v2/", { method: "POST", headers: { "Content-Type": "application/json" }, body: body, keepalive: true, mode: "cors" }).catch(function () {}); }
    catch (e) { return Promise.resolve(); }
  }
  // phones: count, then go to the store (never wait more than 0.6 s)
  window.dvGo = function (url) {
    var done = false, go = function () { if (!done) { done = true; location.replace(url); } };
    ping().then(go); setTimeout(go, 600);
  };
  // computers stay on the page: count once it has loaded
  window.addEventListener("load", function () { if (device === "computer") ping(); });
})();
