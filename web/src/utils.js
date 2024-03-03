matchlist = []

var socket = io("ws://"+window.location.href.split('/')[2]);

function getel(str){return document.getElementById(str)}
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

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
    getEventList()
    getUsername()
    getMatchPosition()
    func()
  })
}



function getUsername(){
  socket.emit("getUsername")
}

function setUsername(value){
  socket.emit("setUsername", value)
}


function onUsername(func){
  socket.on('username', (data)=>{
    getel('username').value = data
    func(data)
  })
  getel('username').addEventListener("keyup", (e) => {
    if(e.key == "Enter"){
      getel('username').blur()
      setUsername(getel('username').value)
    }
  })
}

function getEventList(){
  socket.emit("getEvents")
}

function setEvent(event){
  socket.emit('setSelectedEvent', event)
}

function onEventList(func){
  socket.on('eventList', (data, selectedEvent)=>{
    matchlist = data.split('•')
    line = ''
    if(selectedEvent == ''){
      line += '<option disabled selected value>select</option>'
    }
    for(i=0; i<matchlist.length;i++){
      if(matchlist[i]==selectedEvent){
        line += `<option selected `
      }else{
        line += `<option `
      }
      line += `value="${matchlist[i]}">${matchlist[i]}</option>`
    }
    getel('events').innerHTML = line
    func(matchlist)
  })
  getel('events').addEventListener("change", (e) => {
    setEvent(getel('events').value)
  })
}

function getMatchPosition(){
  socket.emit("getMatchPosition")
}

function setMatchPosition(pos){
  socket.emit("setMatchPosition", pos)
}

function setCurMatch(match){
  socket.emit('setCurMatch', match)
}


function onMatchPosition(func){
  socket.on('matchPosition', (matchPosition)=>{
    getel('position').value = matchPosition
    func(matchPosition)
  })
  getel('position').addEventListener("change", (e) => {
    setMatchPosition(getel('position').value)
  })
}

function sortTable(table, n) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  
  switching = true;
  dir = "asc";
  while (switching) {
      switching = false;
      rows = table.getElementsByTagName("TR");
      for (i = 1; i < (rows.length - 1); i++) {
          shouldSwitch = false;
          x = rows[i].getElementsByTagName("TH")[n];
          y = rows[i + 1].getElementsByTagName("TH")[n];
                  var cmpX=isNaN(parseInt(x.innerHTML))?x.innerHTML.toLowerCase():parseFloat(x.innerHTML);
                  var cmpY=isNaN(parseInt(y.innerHTML))?y.innerHTML.toLowerCase():parseFloat(y.innerHTML);
  cmpX=(cmpX=='-')?0:cmpX;
  cmpY=(cmpY=='-')?0:cmpY;
          if (dir == "asc") {
            if (cmpX < cmpY) {
              shouldSwitch= true;
              break;
            }
          } else if (dir == "desc") {
            if (cmpX > cmpY) {
              shouldSwitch= true;
              break;
            }
          }
      }
      if (shouldSwitch) {
          rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
          switching = true;
          switchcount ++;      
      } else {
          if (switchcount == 0 && dir == "asc") {
              dir = "desc";
              switching = true;
          }
      }
  }
}

let darkMode = true

function toggleDarkMode(){
  const setProp = (a, b)=>{document.documentElement.style.setProperty(a, b)}
  if(darkMode){
    setProp("--backround-0", "#dadada");
    setProp("--backround-1", "#c0c0c0");
    setProp("--backround-2", "#9e9e9e");
    setProp("--text-1", "#1f1f1f");
    setProp("--text-2", "#dddddd");
    setProp("--select-1", "#059100");
    darkMode = false
  }else{
    setProp("--backround-0", "#1d1d1d");
    setProp("--backround-1", "#333");
    setProp("--backround-2", "#242424");
    setProp("--text-1", "#f2f2f2");
    setProp("--text-2", "#000000");
    setProp("--select-1", "#059100");
    darkMode = true
  }
}