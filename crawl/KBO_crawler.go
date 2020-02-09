package main

import (
	"fmt"
    "log"
    "net/http"
    "html/template"
    "github.com/PuerkitoBio/goquery"
    "os"
    "strconv"
)

type Page struct {
    Title string
    Body  []byte
}

// Render Handler
func renderTemplate(w http.ResponseWriter, tmpl string, p *Page){
    t, err := template.ParseFiles("static/" + tmpl + ".html")
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
    err = t.Execute(w, p)
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
    }
}

// Routers
func rootHandler(w http.ResponseWriter, r *http.Request) {
    title := "index"
    body := r.FormValue("body")
    p := &Page{Title: title, Body: []byte(body)}
    renderTemplate(w, "root", p)
}


//TODO: Get Url to Crawling
func getCrawlUrlHandler(w http.ResponseWriter, r *http.Request){
    title := r.URL.Path[len("/getUrl"):]
    body := r.FormValue("body")
    p := &Page{Title: title, Body: []byte(body)}
    renderTemplate(w, "page/getUrl", p)
}

func backCrawlHandler(w http.ResponseWriter, r *http.Request){
    title := "Go Ahead"
    body := r.FormValue("body")
    test := Crawl(body)
    p := &Page{Title: title, Body: []byte(test)}

    renderTemplate(w, "page/back_run", p)
}
func check(e error) {
    if e != nil {
        panic(e)
    }
}

//TODO: web-crawl
func Crawl(url string) string {
	f, err := os.Create("./KBO_raw")
	check(err)

	test := "DONE"

	defer f.Close()

//    res, err := http.Get(url)

	for i := 0 ; i < 100000 ; i++ {
	    res, err := http.Get("https://www.koreabaseball.com/Record/Player/HitterDetail/Basic.aspx?playerId="+strconv.Itoa(i))
	    if err != nil {
	        log.Fatal(err)
	    }
	    defer res.Body.Close()
	    if res.StatusCode != 200 {
	        log.Fatalf("status code error: %d %s", res.StatusCode, res.Status)
	    }

	    doc, err := goquery.NewDocumentFromReader(res.Body)
	    if err != nil {
	        log.Fatal(err)
	    }

		doc.Find(".player_basic").Each(func(i int, s *goquery.Selection) {
			photo := s.Find("img")
			p_url, _ := photo.Attr("src")
			info := s.Find("li").Text()
			if len(p_url) != 0 {
				n, err := f.WriteString(p_url + info + "\n")
				if err != nil {
					log.Fatal(err)
				}
				fmt.Printf("wrote %d bytes\n", n)
				f.Sync()
			}
		})

	}
    return test
}

//TODO: Render the Tag lists for selection
//TODO: Save to Files (csv) || Insert to Database

func main() {
    http.HandleFunc("/", rootHandler)
    http.HandleFunc("/getUrl", getCrawlUrlHandler)
    http.HandleFunc("/back_run", backCrawlHandler)
    log.Fatal(http.ListenAndServe(":8788", nil))
}
