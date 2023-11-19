function getel(str){return document.getElementById(str)}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

var ws = new WebSocket("ws://"+window.location.href.split('/')[2]+"/ws");

Array.prototype.remove= function(){
  var what, a= arguments, L= a.length, ax;
  while(L && this.length){
      what= a[--L];
      while((ax= this.indexOf(what))!= -1){
          this.splice(ax, 1);
      }
  }
  return this;
}

ws.onclose = function(event) {
  if (event.wasClean) {
    console.log(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
  } else {
    // e.g. server process killed or network down
    // event.code is usually 1006 in this case
    console.log('[close] Connection died');
  }
};

ws.onerror = function(error) {
  console.log(error)
}

function onOpen(func){
  ws.onopen = function(event) {
    console.log("[open] Connection established");
    func(event)
  };
}

function onMessage(func){
  ws.onmessage = function(event) {
    console.log(`[message] Data received from server: ${event.data}`);
    func(event)
  }
}
