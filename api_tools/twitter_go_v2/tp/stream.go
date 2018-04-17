package tp

import (
	"bufio"
	"os"

	"github.com/ChimeraCoder/anaconda"
	"github.com/sirupsen/logrus"
)

// Streamer : stores the state of the the streaming api and provides a number
// of high level methods for interactiong with the service.
type Streamer struct {
	EpochLen int
	Keywords []string
	Path     string
	File     *os.File
	Writer   *bufio.Writer
	API      *anaconda.TwitterApi
	Log      *Logger
}

// InitStreamer : creates a new streamer.
func InitStreamer(
	keywords []string,
	epochLen int,
	path string,
	api *anaconda.TwitterApi,
) *Streamer {
	s := &Streamer{
		EpochLen: epochLen,
		Keywords: keywords,
		Path:     path,
		Log:      &Logger{logrus.New()},
		API:      api,
	}
	s.API.SetLogger(s.Log)
	return s
}

// NewEpoch : open a new file to write tweets to and set up the writer.
func (s *Streamer) NewEpoch() {
	s.File = newFile(s.Path)
	s.Writer = bufio.NewWriter(s.File)
}

// WriteTweet : write tweet to the streamers current file.
func (s *Streamer) WriteTweet(tweet anaconda.Tweet) {
	b, err := JSONCustomTweet(&tweet)
	check(err)
	_, err = s.Writer.Write(append(b, '\n'))
	check(err)
	s.Writer.Flush()
}
