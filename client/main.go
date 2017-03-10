package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"encoding/json"
	"net"
	"time"
	"flag"
	"runtime"

	"golang.org/x/net/ipv4"
	"gopkg.in/cheggaaa/pb.v1"
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

type DSCP struct {
	Name string
	Value int
}

func main() {
	url := "https://trace.erg.abdn.ac.uk/start"
	host := "trace.erg.abdn.ac.uk"
	port := "60606"
	send_count := 10
	packets_per_second := 5

	send_interval := time.Duration((1 / float32(packets_per_second)) * 1000)

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

	description := flag.String("description", "Not given", "Wifi on a Bus")
	flag.Parse()
	fmt.Println("Edge connection description:", *description)

	fmt.Printf("connecting to %s .  .  . ", url)
	res, err := http.Get(url)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf(". . ... done\n")
	data, err := ioutil.ReadAll(res.Body)

	res.Body.Close()
	if err != nil {
		log.Fatal(err)
	}

	if res.StatusCode != 200 {
		fmt.Printf("Server returned %v please try running this tool another time\n", res.StatusCode)
		return
	}

	var token TokenCookie
	err = json.Unmarshal(data, &token)

	if err != nil {
		fmt.Println("Server didn't return a valid token, you may have to pass a captive portal")
		fmt.Println("error:", err)
		fmt.Println(data)
		return
	}

	fmt.Printf("received token:\n %+v\n", token)
	token.Description = *description
	token.TTL = 64
	token.OS = runtime.GOOS

	conn, err := net.Dial("udp", host + ":" + port)
	if err != nil {
		fmt.Printf("error creating UDP flow: %v", err)
		return
	}

	start := time.Now()

	fmt.Println("Sending Datagrams")
	bar := pb.StartNew(send_count * len(dscp_map))
    for _, mark := range dscp_map {
		token.DSCP = mark.Value

		if err := ipv4.NewConn(conn).SetTOS(token.DSCP << 2); err != nil {
			fmt.Printf("Error creating connection: %v", err)
			return
		}

		if err != nil {
			fmt.Printf("error %v", err)
			return
		}

		for i := 1; i <= send_count ; i++ {	
			json.NewEncoder(conn).Encode(token)
			time.Sleep(time.Millisecond * send_interval)
			bar.Increment()
		}
	}
	bar.Finish()
	conn.Close()

	fmt.Printf("Sent %v Datagrams representing %v DSCP Marks sent in %v\n", 
		len(dscp_map) * send_count,
		len(dscp_map), 
		time.Since(start))
	fmt.Println("Thank you for helping make the internet better")
}
