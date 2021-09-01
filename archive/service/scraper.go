package main

import (
	"context"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"strings"
	"time"

	"net/http"

	iconv "github.com/djimenez/iconv-go"
	"github.com/gocolly/colly"
	"github.com/joho/godotenv"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type Time struct {
	Given   string
	Seconds string
	Count   string
}

type Player struct {
	Name string
	Rank string
}

type Move struct {
	Color string
	Move  string
}

type Gibo struct {
	ID          primitive.ObjectID `bson:"_id,omitempty"`
	Title       string             `bson:"title,omitempty"`
	Date        string             `bson:"date,omitempty"`
	Location    string             `bson:"location,omitempty"`
	Komi        string             `bson:"komi,omitempty"`
	Result      string             `bson:"result,omitempty"`
	Time        Time               `bson:"time,omitempty"`
	BlackPlayer Player             `bson:"blackPlayer,omitempty"`
	WhitePlayer Player             `bson:"whitePlayer,omitempty"`
	Handicap    string             `bson:"handicap,omitempty"`
	Moves       []Move             `bson:"moves,omitempty"`
	Link        string             `bson:"link,omitempty"`
	Analyzed    bool               `bson:"analyzed,omitempty"`
}

func main() {

	godotenv.Load(".env")
	start := time.Now()
	ctx, cancel := context.WithTimeout(context.Background(), 1*time.Second)
	defer cancel()

	mongoClient := createConnection(ctx, os.Getenv("DB_URI"))
	defer mongoClient.Disconnect(ctx)

	giboCollection := mongoClient.Database("trenduk").Collection("gibo")

	crawl(giboCollection)

	elapsed := time.Since(start)
	log.Println(elapsed)
}

func crawl(collection *mongo.Collection) {
	c := colly.NewCollector(
		colly.AllowedDomains("cyberoro.com", "www.cyberoro.com"),
	)

	c.OnHTML("td.board_pd", func(e *colly.HTMLElement) {

		if !strings.Contains(e.Attr("align"), "left") {
			return
		}

		link := e.ChildAttr("a[href]", "href")
		link = link[22 : strings.Index(link, ",")-1]
		crawlGiboSGF(collection, link)
	})

	// Change hard set number by checking up to 2014
	for i := 0; i < 452; i++ {
		c.Visit(fmt.Sprintf("https://www.cyberoro.com/bcast/gibo.oro?param=1&div=1&Tdiv=B&Sdiv=2&pageNo=%v&blockNo=1", i))
	}

}

func crawlGiboSGF(collection *mongo.Collection, link string) {
	resp, err := http.Get(link)
	if err != nil {
		log.Fatalln(err)
	}

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatalln(err)
	}

	// Change Encoding
	sb := string(body)
	content, _ := iconv.ConvertString(string(sb), "euc-kr", "utf-8")

	// Parse Content
	tmpGibo := Gibo{}

	splitter := strings.Index(content, ";")
	if splitter == -1 {
		fmt.Println(content)
		return
	}

	info := content[:splitter]
	info = strings.Replace(info, "[", ":", -1)
	info = strings.TrimLeft(info, "(")
	infoArray := strings.Split(info, "]")

	for i := 0; i < len(infoArray); i++ {
		element := strings.TrimSpace(infoArray[i])
		if len(infoArray[i]) <= 2 {
			continue
		}
		switch field := element[:2]; field {
		case "TE": // Game Name
			tmpGibo.Title = element[3:]
		case "RD": // Game Date
			tmpGibo.Date = element[3:]
		case "PC":
			tmpGibo.Location = element[3:]
		case "TM":
			tmpGibo.Time.Given = element[3:]
		case "LT":
			tmpGibo.Time.Seconds = element[3:]
		case "LC":
			tmpGibo.Time.Count = element[3:]
		case "KO":
			tmpGibo.Komi = element[3:]
		case "RE":
			tmpGibo.Result = element[3:]
		case "PB":
			tmpGibo.BlackPlayer.Name = element[3:]
		case "BR":
			tmpGibo.BlackPlayer.Rank = element[3:]
		case "PW":
			tmpGibo.WhitePlayer.Name = element[3:]
		case "WR":
			tmpGibo.WhitePlayer.Rank = element[3:]
		case "HD":
			tmpGibo.Handicap = element[3:]
		default:
			fmt.Println("ELEMENT: ", element)
		}
	}

	moves := content[splitter+1:]

	splitter = strings.Index(moves, ")")
	if splitter == -1 {
		fmt.Println(content)
		return
	}

	moves = moves[:splitter]
	moves = strings.Replace(moves, "[", "", -1)
	moves = strings.Replace(moves, "]", "", -1)
	movesArray := strings.Split(moves, ";")

	for i := 0; i < len(movesArray); i++ {
		tmpMove := Move{}
		tmpMove.Color = movesArray[i][:1]
		tmpMove.Move = movesArray[i][1:]
		tmpGibo.Moves = append(tmpGibo.Moves, tmpMove)
	}
	tmpGibo.Analyzed = false

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	collection.InsertOne(ctx, tmpGibo)
}

func createConnection(ctx context.Context, URI string) *mongo.Client {
	client, err := mongo.NewClient(options.Client().ApplyURI(URI))
	if err != nil {
		log.Fatal(err)
	}
	err = client.Connect(ctx)
	if err != nil {
		log.Fatal(err)
	}

	return client
}
