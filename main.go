package main

import (
	//"net/http"

	//"io"
	//"os"

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

type Match struct {
	red1  string
	red2  string
	red3  string
	blue1 string
	blue2 string
	blue3 string
}

type Event struct {
	Title   string
	key     string
	matches Match
}

type MatchResults struct {
	winteam      bool
	pointsScored int
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

// func initMatch(name string, data Event) {
// 	files, err := os.ReadDir("/tmp/")
// 	parseError(err)

// 	for _, file := range files {
// 		fmt.Println(file.Name(), file.IsDir())
// 	}

// }

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
			var splitstring = strings.Split(string(message), "§")[0]

			switch splitstring {
			case "getMatches":
				conn.WriteMessage(mt, []byte("Matches§"+strings.Join(getMatchDirs(), "•")))
			case "getFilesInMatch":
				//fmt.Println(getFileInMatchDir())
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

	r.StaticFile("/src/utils.js", "./web/src/utils.js")
	r.StaticFile("/src/qr-scanner.umd.min.js", "./web/src/qr-scanner.umd.min.js")
	r.StaticFile("/src/qr-scanner-worker.min.js", "./web/src/qr-scanner-worker.min.js")
	r.StaticFile("/src/qr-scanner.umd.min.js.map", "./web/src/qr-scanner.umd.min.js.map")
	r.StaticFile("/src/qr.js", "./web/src/qr.js")
	r.StaticFile("/src/style.css", "./web/src/style.css")

	r.Run(":80")

}
