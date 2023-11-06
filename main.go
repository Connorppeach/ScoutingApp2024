package main

import (
  "net/http"

  "github.com/gin-gonic/gin"
)

func main() {
  r := gin.Default()
  r.GET("/scout/:key", func(c *gin.Context) {
    name := c.Param("key")
    c.String(http.StatusOK, "Hello %s", key)
  })
  r.Run() // listen and serve on 0.0.0.0:8080 (for windows "localhost:8080")
}