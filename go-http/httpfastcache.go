package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"github.com/patrickmn/go-cache"
	"io/ioutil"
	"net/http"
	"os"
	"time"
)

// ConfigType represents config info
type ConfigType struct {
	HostPort   string
	Stacosys   string
	CorsOrigin string
}

var config ConfigType
var countCache = cache.New(5*time.Minute, 10*time.Minute)

func die(format string, v ...interface{}) {
	fmt.Fprintln(os.Stderr, fmt.Sprintf(format, v...))
	os.Exit(1)
}

func commentsCount(w http.ResponseWriter, r *http.Request) {

	// only GET method is supported
	if r.Method != "GET" {
		http.NotFound(w, r)
		return
	}

	// set header
	w.Header().Add("Content-Type", "application/json")
	w.Header().Add("Access-Control-Allow-Origin", config.CorsOrigin)

	// get cached value
	cachedBody, found := countCache.Get(r.URL.String())
	if found {
		//fmt.Printf("return cached value")
		w.Write([]byte(cachedBody.(string)))
		return
	}

	// relay request to stacosys
	fmt.Println("QUERY: " + config.Stacosys + r.URL.String())
	response, err := http.Get(config.Stacosys + r.URL.String())
	if err != nil {
		http.NotFound(w, r)
		return
	}
	defer response.Body.Close()
	body, err := ioutil.ReadAll(response.Body)
	if err != nil {
		http.NotFound(w, r)
		return
	}

	// cache body and return response
	countCache.Set(r.URL.String(), string(body), cache.DefaultExpiration)
	fmt.Printf(string(body))
	w.Write(body)
}

func main() {
	pathname := flag.String("config", "", "config pathname")
	flag.Parse()
	if *pathname == "" {
		die("%s --config <pathname>", os.Args[0])
	}
	// read config File
	file, e := ioutil.ReadFile(*pathname)
	if e != nil {
		die("File error: %v", e)
	}
	json.Unmarshal(file, &config)
	fmt.Printf("config: %s\n", string(file))

	http.HandleFunc("/comments/count/", commentsCount)
	http.HandleFunc("/comments/count", commentsCount)
	http.ListenAndServe(config.HostPort, nil)
}
