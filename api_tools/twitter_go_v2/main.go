package main

import (
	"flag"
	"log"
	"net/url"
	"strings"
	"tweep2/tp"

	"github.com/ChimeraCoder/anaconda"
)

var (
	keywordsPath      string
	outputPath        string
	epochlen          int
	consumerKey       = tp.GetEnv("TWITTER_CONSUMER_KEY")
	consumerSecret    = tp.GetEnv("TWITTER_CONSUMER_SECRET")
	accessToken       = tp.GetEnv("TWITTER_ACCESS_TOKEN")
	accessTokenSecret = tp.GetEnv("TWITTER_ACCESS_TOKEN_SECRET")
)

func init() {
	// parse commanline flags, require keywords path.
	flag.StringVar(&keywordsPath, "keywords", "", "filepath for keywords")
	flag.StringVar(&outputPath, "outputPath", "out", "Path for storage")
	flag.IntVar(&epochlen, "epochlen", 5000, "Number of tweets peer file.")
	flag.Parse()
	if keywordsPath == "" {
		log.Fatal("Error: args for command flag `-track` are required.",
			"`-help` for more information.\n")
	}
}

func main() {

	keywords, err := tp.ReadLines(keywordsPath)
	if err != nil {
		panic(err)
	}

	anaconda.SetConsumerKey(consumerKey)
	anaconda.SetConsumerSecret(consumerSecret)
	api := anaconda.NewTwitterApi(accessToken, accessTokenSecret)

	s := tp.InitStreamer(keywords, epochlen, outputPath, api)

	stream := s.API.PublicStreamFilter(url.Values{
		"track": s.Keywords,
	})
	defer stream.Stop()
	s.Log.Infof("tracking terms: '%s'", strings.Join(s.Keywords, ","))
	s.NewEpoch()
	i := s.EpochLen
	for v := range stream.C {
		tweet, ok := v.(anaconda.Tweet)
		if !ok {
			if _, ok := v.(anaconda.LimitNotice); !ok {
				s.Log.Warningf("recived unexpeted value of type %T", v)
			}
			continue
		}
		if tweet.RetweetedStatus != nil || tweet.ExtendedTweet.FullText == "" {
			continue
		}
		s.WriteTweet(tweet)
		i--
		if i <= 0 {
			s.File.Close()
			s.NewEpoch()
			i = s.EpochLen
		}
	}
}
