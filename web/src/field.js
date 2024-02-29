let dragged = false
let isShift = false
let clickIndex = -1

let selNodeIndex = -1

let finNodes = {
  autoNodes: [],
  teleNodes: []
}
let mode = "auto"
let nodes = []

let displayMode = ""
let paths = []

const canvas = document.querySelector('canvas')
const ctx = canvas.getContext("2d")

function displayPath(nodeArray){
  if(nodeArray == undefined){
    return
  }
  const rect = canvas.getBoundingClientRect()
  for(let i=0;i<nodeArray.length;i++){


    drawCircle(nodeArray[i].x*rect.width, nodeArray[i].y*rect.height, nodeRadius*rect.width, nodeColor)

    if(i > 0){

      startX = nodeArray[i].x * rect.width
      startY = nodeArray[i].y * rect.height
      stopX = nodeArray[i-1].x * rect.width
      stopY = nodeArray[i-1].y * rect.height
      
      ctx.beginPath()
      ctx.moveTo(startX, startY)
      ctx.lineTo(stopX, stopY)
      ctx.strokeStyle = nodeColor
      ctx.lineWidth = lineWidth*rect.width
      ctx.stroke()
    }
  }
}

window.clearCanvas = ()=>{
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  if(displayMode == "edit"){
    displayPath(nodes)
  }else if(displayMode == "display"){
    for(let i=0;i<paths.length;i++){
      if(mode == "auto"){
        displayPath(paths[i].autoNodes)
      }else if(mode == "tele"){
        displayPath(paths[i].tele)
      }
    }
  }
}

function drawCircle(x, y, radius, fill, stroke, strokeWidth) {
  ctx.beginPath()
  ctx.arc(x, y, radius, 0, 2 * Math.PI, false)
  if (fill) {
    ctx.fillStyle = fill
    ctx.fill()
  }
  if (stroke) {
    ctx.lineWidth = strokeWidth
    ctx.strokeStyle = stroke
    ctx.stroke()
  }
}

function getElementAt(x, y){
  const rect = canvas.getBoundingClientRect()
  for(let i=0;i<nodes.length;i++){
    dist = Math.sqrt(Math.pow((x*rect.width) - (nodes[i].x*rect.width), 2) + Math.pow((y*rect.height) - (nodes[i].y*rect.height), 2))
    if(nodeRadius*1.5*rect.height >= dist){
      return i
    }
  }
  return -1
}

function addCircle(x, y){
  nodes.push({
    x: x,
    y: y
  })
}

// function getCanvasSize(){
//   return {
//     specifiedWidth : canvas.width,
//     specifiedHeight :canvas.height,
//     realWidth : canvas.offsetWidth,
//     realHeight : canvas.offsetHeight,
//     heightScale: canvas.height/canvas.offsetHeight,
//     widthScale: canvas.width/canvas.offsetWidth
//   }
// }

function getMousePos(e){
  const rect = canvas.getBoundingClientRect()
  // const mouseX = Math.round(e.clientX - rect.left) / rect.width
  // const mouseY = Math.round(e.clientY - rect.top) / rect.height


  // const mouseX = (e.clientX - rect.left / rect.width).toPrecision(10)
  // const mouseY = (e.clientY - rect.top / rect.height).toPrecision(10)

  const mouseX = Number(((e.clientX - rect.left) / rect.width).toPrecision(4))
  const mouseY = Number(((e.clientY - rect.top) / rect.height).toPrecision(4))

  // var s = getCanvasSize();
  // var x = e.pageX - canvas.offsetLeft
  // var y = e.pageY - canvas.offsetTop
  // mouseX = x*s.realWidth
  // mouseY = y*s.realHeight

  return {mouseX, mouseY}
}

window.startGraphEdit = ()=>{
  displayMode = "edit"

  canvas.addEventListener("mousemove",function(e){
    e = getMousePos(e)
    mouseX = e.mouseX
    mouseY = e.mouseY
  
    if(dragged){
      elem = getElementAt(mouseX, mouseY)


      if(isShift && elem != -1 && elem != clickIndex){
        nodes[clickIndex].x = nodes[elem].x
        nodes[clickIndex].y = nodes[elem].y
      }else{
        nodes[clickIndex].x = mouseX
        nodes[clickIndex].y = mouseY
      }
    }startGraphEdit

    clearCanvas()

    //drawCircle(mouseX, mouseY, nodeRadius, nodeColor)
  })

  canvas.addEventListener("mousedown", (e)=>{
    e = getMousePos(e)
    mouseX = e.mouseX
    mouseY = e.mouseY

    elem = getElementAt(mouseX, mouseY)

    if(elem == -1){
      addCircle(mouseX,mouseY)
    }else{
      if(isShift){
        addCircle(nodes[elem].x,nodes[elem].y)
      }else{
        dragged = true
        clickIndex = elem
      }
    }
    clearCanvas()
  })

  canvas.addEventListener("mouseup", (e)=>{
    if(dragged){
      dragged = false
      clickIndex = -1
    }
  })

  canvas.addEventListener("dblclick", (e)=>{
  
    e = getMousePos(e)
    mouseX = e.mouseX
    mouseY = e.mouseY

    elem = getElementAt(mouseX, mouseY)

    if(elem != -1){
      nodes.splice(elem, 1)
    }

    if(isShift){
      nodes = []
    }

    clearCanvas()
  })

  document.addEventListener("keydown", (e)=>{
    key = e.which || e.keyCode
    if(key == 16){
      isShift = true
    }
  })
  document.addEventListener("keyup", (e)=>{
    key = e.which || e.keyCode;
    if(key == 16){
      isShift = false
    }
  })
}

window.startDisplay = ()=>{
  displayMode = "display"
}

function toLolConvert(nodeArray){
  newArr = []
  for(let i=0;i<nodeArray.length;i++){
    newObj = {}
    newObj.x = Number(String(nodeArray[i].x).slice(2))
    newObj.y = Number(String(nodeArray[i].y).slice(2))
    newArr.push(newObj)
  }
  return newArr
}

function fromLolConvert(nodeArray){
  newArr = []
  for(let i=0;i<nodeArray.length;i++){
    newObj = {}
    newObj.x = Number(String("0." + nodeArray[i].x))
    newObj.y = Number(String("0." + nodeArray[i].y))
    newArr.push(newObj)
  }
  return newArr
}

function invertX(nodeArray){
  newArr = []
  for(let i=0;i<nodeArray.length;i++){
    newObj = {}
    newObj.x = 1-(nodeArray[i].x)
    newObj.y = (nodeArray[i].y)
    newArr.push(newObj)
  }
  return newArr
}

window.setModeTele = ()=>{
  if(mode == "auto"){
    finNodes.autoNodes = nodes
    nodes = finNodes.teleNodes
    clearCanvas()
    mode = "tele"
  }
}

window.setModeAuto = ()=>{
  if(mode == "tele"){
    finNodes.teleNodes = nodes
    nodes = finNodes.autoNodes
    clearCanvas()
    mode = "auto"
  }
}

window.toggleMode = ()=>{
  if(mode == "auto"){
    window.setModeTele()
  }else{
    window.setModeAuto()
  }
}

window.clearNodes = ()=>{
  finNodes = {
    autoNodes: [],
    teleNodes: []
  }
  nodes = []
  mode = "auto"
  clearCanvas()
}

window.importPath = (newPaths, invert)=>{
  newNodes = {
    autoNodes: fromLolConvert(newPaths.autoNodes),
    teleNodes: fromLolConvert(newPaths.teleNodes),
  }
  if(invert){
    newNodes = {
      autoNodes: invertX(newNodes.autoNodes),
      teleNodes: invertX(newNodes.teleNodes),
    }
  }
  paths.push(newNodes)
  clearCanvas()
}

window.importNodes = (newNodes)=>{
  newNodes = {
    autoNodes: fromLolConvert(newNodes.autoNodes),
    teleNodes: fromLolConvert(newNodes.teleNodes),
  }
  // if(invert){
  //   newNodes = {
  //     autoNodes: invertX(newNodes.autoNodes),
  //     teleNodes: invertX(newNodes.teleNodes),
  //   }
  // }

  finNodes = newNodes
  nodes = newNodes.autoNodes
  mode = "auto"
  clearCanvas()
}

window.exportNodes = ()=>{
  if(mode == "auto"){
    finNodes.autoNodes = nodes
  }else{
    finNodes.teleNodes = nodes
  }
  return {
    autoNodes: toLolConvert(finNodes.autoNodes),
    teleNodes: toLolConvert(finNodes.teleNodes)
  }
}

window.onresize = ()=>{
  const img = document.getElementsByTagName("img")[0]
  const container = document.getElementsByClassName("container")[0].getBoundingClientRect()
  const height = container.width * (65 / 129)
  img.style.height = height + "px"
  canvas.style.height = height + "px"
  canvas.style.marginTop = -height + "px"
  canvas.style.transform = "translate(0px, " + height + "px)"
  canvas.width = container.width
  canvas.height = height
  document.getElementById("plotter").style.paddingBottom = height + "px"
  clearCanvas()
}

window.onresize()