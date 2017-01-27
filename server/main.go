package main

import (
  "net/http" 
  "io"
  "encoding/json"
  "fmt"
  "time"
  "math/rand"
  "crypto/sha1"
  "encoding/base64"
)

type TokenCookie struct {
  Host string `json:"host"`
  Time string `json:"time"`
  Token string  `json:"token"`
  DSCP int `json:"dscp"`
}

func start(res http.ResponseWriter, req *http.Request) {
  res.Header().Set("Content-Type", "application/json")

  host := req.Header.Get("X-Real-IP")
  time := time.Now().UTC().Format("20060102150405")
  randval := string(rand.Intn(1000000))

  token := host + time + randval

  hash := sha1.New()
  hash.Write([]byte(token))
  sekret := base64.StdEncoding.EncodeToString(hash.Sum(nil))

  cookie := TokenCookie{Host: host, Time: time, Token:sekret}
  fmt.Println(cookie)
  json.NewEncoder(res).Encode(cookie)
}

func index(res http.ResponseWriter, req *http.Request) {
  res.Header().Set(
    "Content-Type",
    "text/html",
  )

  io.WriteString(
    res,
    `<DOCTYPE html>
<html>
  <head>
      <title>Hello World</title>
  </head>
  <body>
    <h1>
        Hello, welcome to the trace server
    </h1>
    <p>
        WebServer for doing a series of PANIC DSCP Traces from Network Edges.
        For code and maybe even some documentation, please check out the github
        repo here:
    </p>
    <p>
        <a href="https://github.com/uoaerg/edgetrace">https://github.com/uoaerg/edgetrace</a>
    </p>
  </body>
</html>`,
  )
}
func main() {
  http.HandleFunc("/", index)
  http.HandleFunc("/start", start)


  fmt.Println("Starting up Server, listening on port: 4000")
  http.ListenAndServe(":4000", nil)
}
