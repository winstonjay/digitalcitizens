package tp

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/sirupsen/logrus"
)

// Logger : Extends the logrus logger to meet the interface requirements
// needed to be used as a logger the anaconda api.
type Logger struct {
	*logrus.Logger
}

// Critical :
func (lg *Logger) Critical(args ...interface{}) { lg.Error(args...) }

// Criticalf :
func (lg *Logger) Criticalf(format string, args ...interface{}) { lg.Errorf(format, args...) }

// Notice :
func (lg *Logger) Notice(args ...interface{}) { lg.Info(args...) }

// Noticef :
func (lg *Logger) Noticef(format string, args ...interface{}) { lg.Infof(format, args...) }

func newFile(filename string) *os.File {
	t := time.Now()
	filename = fmt.Sprintf("%s%d-%02d-%02dT%02d%02d%02d.ndjson",
		filename, t.Year(), t.Month(), t.Day(), t.Hour(), t.Minute(), t.Second())
	outfile, err := os.Create(filename)
	check(err)
	return outfile
}

func check(e error) {
	if e != nil {
		log.Fatalf("Error: %v\n", e)
	}
}

// GetEnv load enviroment varible.
func GetEnv(name string) string {
	v := os.Getenv(name)
	if v == "" {
		log.Fatalf("Error: Env variable %q is required.\n", name)
	}
	return v
}

// ReadLines : read file into a string array line by line.
func ReadLines(path string) ([]string, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer f.Close()
	var lines []string
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	return lines, scanner.Err()
}
