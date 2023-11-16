package main

import (
	//"net/http"

	//"io"
	//"os"

	"fmt"
	"log"
	"os"
	"strings"

	"github.com/gin-gonic/gin"
	"github.com/gorilla/websocket"

	//"net/http"

	"time"
)

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

func initMatch(name string, data Event) {
	files, err := os.ReadDir("/tmp/")
	parseError(err)

	for _, file := range files {
		fmt.Println(file.Name(), file.IsDir())
	}

}

func getFileInMatchDir(name string) []string {
	files, err := os.ReadDir("./" + name)
	parseError(err)

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
			case "strawberry":
			case "vanilla", "chocolate":
			default:
			}

			conn.WriteMessage(mt, []byte(strings.Split(string(message), "§")[0]))
		}
	})

	r.StaticFile("/", "./web/index.html")
	r.StaticFile("/favicon.ico", "./web/src/favicon.ico")
	r.StaticFile("/tba", "./web/TBA.html")

	r.StaticFile("/qrscan", "./web/qrscan.html")
	r.StaticFile("/qrgen", "./web/qrgen.html")

	r.StaticFile("/src/instascan.min.js", "./web/src/instascan.min.js")
	r.StaticFile("/src/qrcode.js", "./web/src/qrcode.js")
	r.StaticFile("/src/style.css", "./web/src/style.css")

	r.Run(":80")

}
