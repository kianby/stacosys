package main

import (
	"github.com/patrickmn/go-cache"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"time"
)

const stacoURL string = "http://127.0.0.1:8100"

var countCache = cache.New(5*time.Minute, 10*time.Minute)

func commentsCount(w http.ResponseWriter, r *http.Request) {

	// only GET method is supported
	if r.Method != "GET" {
		http.NotFound(w, r)
		return
	}

	// set header
	w.Header().Add("Content-Type", "application/json")
	w.Header().Add("Access-Control-Allow-Origin", "*")

	// get cached value
	cachedBody, found := countCache.Get(r.URL.String())
	if found {
		//log.Printf("return cached value")
		w.Write([]byte(cachedBody.(string)))
		return
	}

	// relay request to stacosys
	response, err := http.Get(stacoURL + r.URL.String())
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
	log.Printf(string(body))
	w.Write(body)
}

func comments(w http.ResponseWriter, r *http.Request) {
	io.WriteString(w, "Hello world!")
}

func main() {
	http.HandleFunc("/comments/count", commentsCount)
	http.HandleFunc("/comments", comments)
	http.ListenAndServe(":8200", nil)
}
