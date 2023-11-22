function getel(str){return document.getElementById(str)}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

var socket = io("ws://"+window.location.href.split('/')[2]);

// var ws = new WebSocket("ws://"+window.location.href.split('/')[2]+"/ws");

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

socket.onclose = function() {
  console.log('[close] Connection died');
}

socket.onerror = function(error) {
  console.log(error)
}

function onOpen(func){
  socket.on('connect', () => {
    console.log("[open] Connection established")
    func()
  })
}