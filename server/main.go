package main

import (
	"crypto/sha1"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"math/rand"
	"net/http"
	"time"
	"net"
)

type TokenCookie struct {
	Host  string `json:"host"`
	Time  string `json:"time"`
	Token string `json:"token"`
	DSCP  int    `json:"dscp"`
	TTL   int    `json:"ttl"`
	Description string `json:"description"`
	OS string `json:"os"`
}


var salt string

func calcsekret(host string, time string, salt string) string { 

	token := host + time + salt

	hash := sha1.New()
	hash.Write([]byte(token))

	return hex.EncodeToString(hash.Sum(nil))
}

func start(res http.ResponseWriter, req *http.Request) {
	res.Header().Set("Content-Type", "application/json")

	host := req.Header.Get("X-Real-IP")
	time := time.Now().UTC().Format("20060102150405")

	sekret := calcsekret(host, time, salt)	

	cookie := TokenCookie{Host: host, Time: time, Token: sekret}
	fmt.Printf("New HTTP CONNECTION: %v",cookie)
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

func udplisten() {
	port := 60606
    conn, err := net.ListenUDP("udp", &net.UDPAddr{Port: port})
	if err != nil {                     
		fmt.Printf("Some error %v", err)
		return                          
	}

    defer conn.Close()
 
    data := make([]byte, 1024)
 
    for {
        size, addr, err := conn.ReadFromUDP(data)

		var token TokenCookie                        
		err = json.Unmarshal(data[0:size], &token)           
													 
		if err != nil {                              
			fmt.Println("error:", err)               
		}                                            

		recv_token := calcsekret(token.Host, token.Time, salt)

		if recv_token == token.Token {
			fmt.Printf("UDP DATAGRAM from: %v: %+v\n", addr, token)
		}

        if err != nil {
            fmt.Println("Error: ",err)
        } 
    }
}

func main() {
	salt = string(rand.Intn(0xFFFFFFFF))

	//http.HandleFunc("/", index)
	http.HandleFunc("/start", start)
	http.Handle("/", http.FileServer(http.Dir("./static")))
	
	fmt.Println("Starting up Web Server, listening on port: 4000")
	go http.ListenAndServe(":4000", nil)

	fmt.Println("Starting up UDP Listening on port: 60606")
	go udplisten()
 
	var input string
	fmt.Scanln(&input)
}
