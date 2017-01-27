package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"encoding/json"
	"net"
	"time"
	"golang.org/x/net/ipv4"
)

type TokenCookie struct {
	Host  string `json:"host"`
	Time  string `json:"time"`
	Token string `json:"token"`
	DSCP  int    `json:"dscp"`
}

type DSCP struct {
	Name string
	Value int
}


func main() {
	url := "http://trace.enoti.me/start"

	dscp_map := [21]DSCP{
		{Name:"BE",   Value:0x00},
		{Name:"EF",   Value:0x2e},
		{Name:"CS1",  Value:0x08},
		{Name:"CS2",  Value:0x10},
		{Name:"CS3",  Value:0x18},
		{Name:"CS4",  Value:0x20},
		{Name:"CS5",  Value:0x28},
		{Name:"CS6",  Value:0x30},
		{Name:"CS7",  Value:0x38},
		{Name:"AF11", Value:0x0a},
		{Name:"AF12", Value:0x0c},
		{Name:"AF13", Value:0x0e},
		{Name:"AF21", Value:0x12},
		{Name:"AF22", Value:0x14},
		{Name:"AF23", Value:0x16},
		{Name:"AF31", Value:0x1a},
		{Name:"AF32", Value:0x1c},
		{Name:"AF33", Value:0x1e},
		{Name:"AF41", Value:0x22},
		{Name:"AF42", Value:0x24},
		{Name:"AF43", Value:0x26},
	}

	res, err := http.Get(url)
	if err != nil {
		log.Fatal(err)
	}

	data, err := ioutil.ReadAll(res.Body)

	res.Body.Close()
	if err != nil {
		log.Fatal(err)
	}

	var token TokenCookie
	err = json.Unmarshal(data, &token)

	if err != nil {
		fmt.Println("error:", err)
	}

	fmt.Printf("%+v\n", token)

    for _, mark := range dscp_map {
		conn, err := net.Dial("udp", "trace.enoti.me:60606")
		fmt.Println("Created UDP Connection")

		fmt.Printf("sending mark: %v\n", mark.Value)

		token.DSCP = mark.Value
		if err := ipv4.NewConn(conn).SetTOS(token.DSCP); err != nil {
			// error handling
		}

		if err != nil {
			fmt.Printf("Some error %v", err)
			return
		}

		for i := 1; i <= 10; i++ {	
			token.Time = time.Now().UTC().Format("20060102150405")    

			json.NewEncoder(conn).Encode(token)
			time.Sleep(time.Millisecond * 100)
		}

		conn.Close()
	}
}
