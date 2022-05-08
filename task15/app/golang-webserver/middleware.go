package main

import (
	"net/http"

	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promauto"
)

func (s *server) reqCounterMiddleware(h http.HandlerFunc, route string) http.HandlerFunc {
	s.requestCounter[route] = promauto.NewCounter(prometheus.CounterOpts{
		Name: "casestudy_processed_requests_total_" + route,
		Help: "The total number of processed requests for route " + route,
	})
	return func(resp http.ResponseWriter, req *http.Request) {
		s.requestCounter[route].Inc()
		h(resp, req)
	}
}
