package main

import (
	"copop/pkg"
	"fmt"
	"io"
	"log"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"sync"
	"time"
)

var BUFFERSIZE int64

func copy(src, dst string, BUFFERSIZE int64) error {
	sourceFileStat, err := os.Stat(src)
	if err != nil {
		return err
	}

	if !sourceFileStat.Mode().IsRegular() {
		return fmt.Errorf("%s is not a regular file.", src)
	}

	source, err := os.Open(src)
	if err != nil {
		return err
	}
	defer source.Close()

	ff, err := source.Stat()
	if err != nil {
		return err
	}

	_, err = os.Stat(dst)
	if err == nil {
		return fmt.Errorf("File %s already exists.", dst)
	}

	destination, err := os.Create(dst)
	if err != nil {
		return err
	}

	defer destination.Close()

	if err != nil {
		panic(err)
	}

	total := ff.Size()
	buf := make([]byte, BUFFERSIZE)
	buffin := 0
	for {
		n, err := source.Read(buf)
		if err != nil && err != io.EOF {
			return err
		}

		if n == 0 || err == io.EOF {
			//finish copying then the next
			break
		}

		downb, err := destination.Write(buf[:n])

		if err != nil {
			return err
		}

		if (int64(downb)-int64(buffin)) > (BUFFERSIZE/5) && downb > 10000 {
			buffin = downb
			percent := float64(downb) / float64(total) * 100
			//nowcc := big.NewFloat(percent).SetPrec(3).String()
			Logf("Now: %d %.2f\n", downb, percent)
		}

	}
	return err
}

func removefil(source string, w *sync.WaitGroup) {
	defer w.Done()
	err := os.Remove(source)
	if err != nil {
		Logf("Error from removing file: %s %q\n", source, err)
		return
	}
}

func blocktransfer(source, destination string) {

	BUFFERSIZE, err := strconv.ParseInt(os.Args[3], 10, 64)

	if err != nil {
		Logf("Invalid buffer size: %q\n", err)
		return
	}

	Logf("Copying %s to %s\n", source, destination)

	result := copy(source, destination, BUFFERSIZE)

	if result != nil {
		Logf("File copying failed: %q\n", err)
	} else {
		Logf("File moving file done: %s\n", destination)
	}
}

func Log(s string) {
	var optionalLogFile = ""

	if len(os.Args) == 5 {
		optionalLogFile = os.Args[4]
	} else {
		optionalLogFile = "farm_plot.log"
	}

	f, err := os.OpenFile(optionalLogFile, os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)
	if err != nil {
		log.Fatalf("error opening file: %v", err)
	}
	defer f.Close()
	wrt := io.MultiWriter(os.Stdout, f)
	//nowExt := time.Now()
	log.SetOutput(wrt)
	log.Println(fmt.Sprintf("%s", s))
}
func Logf(format string, a ...interface{}) {
	Log(fmt.Sprintf(format, a))
}

var KB = uint64(1024)

func main() {
	var wg sync.WaitGroup

	if len(os.Args) < 4 {
		fmt.Printf("usage: %s source destination BUFFERSIZE logfile(optional) \n", filepath.Base(os.Args[0]))
		return
	}

	sourceDir := os.Args[1]
	destinationDir := os.Args[2]
	k := strings.Index(destinationDir, ",")

	if k > -1 {

		Log("exit and done. because there is not yet developed for destination in list yet")
	} else {

		for {

			matches, _ := filepath.Glob(fmt.Sprintf("%s/*.plot", sourceDir))
			Logf("Found plot files %d", len(matches))

			if len(matches) > 0 {
				match := matches[0]
				fileinfo, _ := os.Stat(match)
				if fileinfo.Mode().IsRegular() {
					name := fileinfo.Name()
					des := fmt.Sprintf("%s%s", destinationDir, name)

					usage := pkg.NewDiskUsage(destinationDir)

					if usage.Free() > uint64(fileinfo.Size()) {
						blocktransfer(match, des)
						wg.Add(1)
						go removefil(match, &wg)
					} else {
						Log("there is not enough space")
						Logf("Free:", usage.Free()/(KB*KB))
						Logf("Available:", usage.Available()/(KB*KB))
						Logf("Size:", usage.Size()/(KB*KB))
						Logf("Used:", usage.Used()/(KB*KB))
						Logf("Usage:", usage.Usage()*100, "%")
						time.Sleep(100 * time.Second)
					}
				}
				time.Sleep(5 * time.Second)
			} else {
				time.Sleep(50 * time.Second)
			}
		}
	}
	wg.Wait()
}
