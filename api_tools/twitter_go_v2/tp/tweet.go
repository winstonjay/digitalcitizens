package tp

import (
	"encoding/json"

	"github.com/ChimeraCoder/anaconda"
)

// CustomTweet :
type CustomTweet struct {
	CreatedAt         string                `json:"created_at"`
	FullText          string                `json:"full_text"`
	Entities          anaconda.Entities     `json:"entities"`
	PossiblySensitive bool                  `json:"possibly_sensitive"`
	Lang              string                `json:"lang"`
	Source            string                `json:"source"`
	Coordinates       *anaconda.Coordinates `json:"coordinates"`
	User              anaconda.User         `json:"user"`
}

// JSONCustomTweet :
func JSONCustomTweet(tweet *anaconda.Tweet) ([]byte, error) {
	t := &CustomTweet{
		CreatedAt:         tweet.CreatedAt,
		FullText:          tweet.ExtendedTweet.FullText,
		Entities:          tweet.Entities,
		PossiblySensitive: tweet.PossiblySensitive,
		Lang:              tweet.Lang,
		Source:            tweet.Source,
		Coordinates:       tweet.Coordinates,
		User:              tweet.User,
	}
	return json.Marshal(t)
}
