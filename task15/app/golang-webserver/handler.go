package main

import (
	"fmt"
	"math/rand"
	"net/http"
	"time"

	dto "github.com/prometheus/client_model/go"
)

func (s *server) indexHandler() http.HandlerFunc {
	return func(resp http.ResponseWriter, req *http.Request) {
		fmt.Fprint(resp, indexTemplate)
	}
}

func (s *server) hotelHandler() http.HandlerFunc {
	return func(resp http.ResponseWriter, req *http.Request) {
		resp.WriteHeader(http.StatusOK)
		resp.Header().Set("Content-Type", "application/json")
		fmt.Fprint(resp, hotelTemplate)
	}
}

func (s *server) healthHandler() http.HandlerFunc {
	return func(resp http.ResponseWriter, req *http.Request) {
		resp.WriteHeader(http.StatusOK)
		fmt.Fprintf(resp, "OK")
	}
}

func (s *server) readinessHandler() http.HandlerFunc {
	seed := rand.NewSource(time.Now().UnixNano())
	randomness := rand.New(seed)
	readySeconds := randomness.Intn(12)

	ready := false
	time.AfterFunc(time.Duration(readySeconds)*time.Second, func() {
		ready = true
	})

	return func(resp http.ResponseWriter, req *http.Request) {
		if !ready {
			resp.WriteHeader(http.StatusServiceUnavailable)

		} else {
			resp.WriteHeader(http.StatusOK)
			fmt.Fprintf(resp, "Ready\nreadySeconds: %d", readySeconds)
		}
	}
}

func (s *server) requestsHandler() http.HandlerFunc {
	return func(resp http.ResponseWriter, req *http.Request) {
		for k, v := range s.requestCounter {
			m := &dto.Metric{}
			v.Write(m)
			fmt.Fprintf(resp, "/%s: %+v\n", k, m.Counter.GetValue())
		}
	}
}
