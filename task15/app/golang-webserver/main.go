package main

import (
	"net/http"
	"os"

	"github.com/gorilla/handlers"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

type server struct {
	requestCounter map[string]prometheus.Counter
}

func main() {
	s := &server{
		requestCounter: make(map[string]prometheus.Counter),
	}

	router := http.NewServeMux()
	router.HandleFunc("/", s.reqCounterMiddleware(s.indexHandler(), "index"))
	router.HandleFunc("/hotels", s.reqCounterMiddleware(s.hotelHandler(), "hotels"))
	router.HandleFunc("/health", s.healthHandler())
	router.HandleFunc("/ready", s.readinessHandler())
	router.HandleFunc("/requests", s.requestsHandler())
	router.Handle("/metrics", promhttp.Handler())

	loggedRouter := handlers.LoggingHandler(os.Stdout, router)
	http.ListenAndServe(":8080", loggedRouter)
}
