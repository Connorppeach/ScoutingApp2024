package main

import (
	"log"
	"os"
	"strings"

	"github.com/gin-gonic/gin"
	"github.com/gorilla/websocket"

	//"net/http"

	"time"
)

const datadir = "./data/"

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
}

func parseError(err error) {
	if err != nil {
		log.Fatal(err)
	}
}

func makedir(path string) bool {
	_, err := os.Stat(path)
	if err == nil {
		return true
	}
	if os.IsNotExist(err) {
		os.Mkdir(path, os.ModeDir)
		return false
	}
	os.Mkdir(path, os.ModeDir)
	return false
}

func getMatchDirs() []string {
	files, err := os.ReadDir(datadir)
	if err != nil {
		var nullstrr []string
		return nullstrr
	}

	var returndata []string
	for _, file := range files {
		returndata = append(returndata, file.Name())
	}
	return returndata
}

func getFileInMatchDir(name string) []string {
	files, err := os.ReadDir(datadir + name)
	if err != nil {
		var nullstrr []string
		return nullstrr
	}

	var returndata []string
	for _, file := range files {
		returndata = append(returndata, file.Name())
	}
	return returndata
}

func main() {
	r := gin.Default()

	makedir(datadir)
	os.Chmod(datadir, 0755)

	r.GET("/ws", func(c *gin.Context) {
		conn, err := upgrader.Upgrade(c.Writer, c.Request, nil)
		if err != nil {
			return
		}
		defer conn.Close()
		for {
			mt, message, _ := conn.ReadMessage()

			time.Sleep(time.Second / 2)

			if string(message) == "" {
				continue
			}

			println("Message:" + string(message))
			var splitstring = strings.Split(string(message), "§")

			switch splitstring[0] {
			case "getMatches":
				conn.WriteMessage(mt, []byte("MatchList§"+strings.Join(getMatchDirs(), "•")))
			case "getFilesInMatch":
				conn.WriteMessage(mt, []byte("MatchFileList§"+splitstring[1]+"§"+strings.Join(getFileInMatchDir(splitstring[1]), "•")))
			case "readFromFile":
				data, err := os.ReadFile(datadir + splitstring[1] + "/" + splitstring[2])
				if err != nil {
					log.Fatal(err)
					conn.WriteMessage(mt, []byte("MatchFileContent§"+splitstring[1]+"§"+splitstring[2]+"§false"))
				} else {
					conn.WriteMessage(mt, []byte("MatchFileContent§"+splitstring[1]+"§"+splitstring[2]+"§"+string(data)))
				}
			case "writeToFile":
				makedir(datadir + splitstring[1])      //No exploits here!
				os.Chmod(datadir+splitstring[1], 0755) //Directory transversal is definitely not real!
				err = os.WriteFile(datadir+splitstring[1]+"/"+splitstring[2], []byte(splitstring[3]), 0755)
				parseError(err)
			default:
				conn.WriteMessage(mt, []byte("Malformed Message"))
			}

			//conn.WriteMessage(mt, []byte(strings.Split(string(message), "§")[0]))
		}
	})

	r.StaticFile("/favicon.ico", "./web/src/favicon.ico")

	r.StaticFile("/", "./web/index.html")

	r.StaticFile("/qrscan", "./web/qrscan.html")
	r.StaticFile("/qrgen", "./web/qrgen.html")
	r.StaticFile("/fileupload", "./web/fileupload.html")
	r.StaticFile("/tba", "./web/TBA.html")

	r.StaticFile("/jsonpack", "./web/jsonpack.html")
	r.StaticFile("/src/jsonpack.js", "./web/src/jsonpack.js")


	r.StaticFile("/src/utils.js", "./web/src/utils.js")
	r.StaticFile("/src/qr-scanner.umd.min.js", "./web/src/qr-scanner.umd.min.js")
	r.StaticFile("/src/qr-scanner-worker.min.js", "./web/src/qr-scanner-worker.min.js")
	r.StaticFile("/src/qr-scanner.umd.min.js.map", "./web/src/qr-scanner.umd.min.js.map")
	r.StaticFile("/src/qr.js", "./web/src/qr.js")
	r.StaticFile("/src/style.css", "./web/src/style.css")

	r.Run(":4388")

}
