package main

import (
	"context"
	"fmt"
	"log"
	"strings"
	"time"

	"go.mongodb.org/mongo-driver/bson"
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

type YearlyStat struct {
	Year  string `bson:"year,omitempty"`
	Count int    `bson:"count,omitempty"`
	Win   int    `bson:"win,omitempty"`
	Lose  int    `bson:"lose,omitempty"`
}

// TODO: Parent can be undefined
type Node struct {
	ID         primitive.ObjectID   `bson:"_id,omitempty"`
	Root       bool                 `bson:"root,omitempty"`
	Move       string               `bson:"move,omitempty"`
	Color      string               `bson:"color,omitempty"`
	Children   []primitive.ObjectID `bson:"children,omitempty"`
	Parent     primitive.ObjectID   `bson:"parent,omitempty"`
	Games      []primitive.ObjectID `bson:"games,omitempty"`
	YearlyStat []YearlyStat         `bson:"yearlyStat,omitempty"`
}

type CustomNode struct {
	Children   []*CustomNode
	Parent     *CustomNode
	Move       string
	Color      string
	Root       bool
	Games      []primitive.ObjectID
	YearlyStat []YearlyStat
}

func main() {
	start := time.Now()
	root := CustomNode{Root: true}
	cursor := queryMoves()
	i := 0
	for cursor.Next(context.Background()) {
		var gibo Gibo
		if err := cursor.Decode(&gibo); err != nil {
			log.Fatal(err)
		}

		if len(gibo.Date) == 0 {
			continue
		}

		topLeft, topRight, bottomLeft, bottomRight := assortCorners(gibo.Moves)

		buildTree(&root, topLeft, gibo)
		buildTree(&root, topRight, gibo)
		buildTree(&root, bottomLeft, gibo)
		buildTree(&root, bottomRight, gibo)

		i++
	}

	fmt.Println("FINISH TREE CREATION")

	res := traverse(&root, primitive.NewObjectID(), primitive.NewObjectID())
	fmt.Println(len(res))
	insertManyMoves(res)
	elapsed := time.Since(start)
	log.Println(elapsed)
}

func assortCorners(moves []Move) ([8]Move, [8]Move, [8]Move, [8]Move) {
	var topLeft, topRight, bottomLeft, bottomRight [8]Move
	tlindex, trindex, blindex, brindex := 0, 0, 0, 0

	for i := 0; i < len(moves); i++ {
		x := string(moves[i].Move[0])
		y := string(moves[i].Move[1])

		if tlindex == 8 && trindex == 8 && blindex == 8 && brindex == 8 {
			break
		}

		if x <= "j" && y <= "j" && tlindex < 8 {
			tmpMove := Move{
				Color: moves[i].Color,
				Move:  reflect(x) + y,
			}
			topLeft[tlindex] = tmpMove
			tlindex++
		}
		if x >= "j" && y <= "j" && trindex < 8 {
			tmpMove := Move{
				Color: moves[i].Color,
				Move:  x + y,
			}
			topRight[trindex] = tmpMove
			trindex++
		}
		if x <= "j" && y >= "j" && blindex < 8 {
			tmpMove := Move{
				Color: moves[i].Color,
				Move:  reflect(x) + reflect(y),
			}
			bottomLeft[blindex] = tmpMove
			blindex++
		}
		if x >= "j" && y >= "j" && brindex < 8 {
			tmpMove := Move{
				Color: moves[i].Color,
				Move:  x + reflect(y),
			}
			bottomRight[brindex] = tmpMove
			brindex++
		}

	}

	for _, moveArray := range [4][8]Move{topLeft, topRight, bottomLeft, bottomRight} {
		reflected := false
		for i, move := range moveArray {
			if move == (Move{}) {
				continue
			}

			x := string(move.Move[0])
			y := string(move.Move[1])
			if i%2 == 0 && !reflected && reflect(x) < y {
				reflected = true
			}

			if i%2 == 1 && !reflected && reflect(x) > y {
				reflected = true
			}

			if reflected {
				move.Move = reflect(y) + reflect(x)
			}
		}
	}

	return topLeft, topRight, bottomLeft, bottomRight
}

func buildTree(root *CustomNode, moves [8]Move, gibo Gibo) {
	var currentNode = root

	for _, move := range moves {

		var win, lose int
		if move.Color == checkWinner(gibo.Result) {
			win = 1
			lose = 0
		} else {
			win = 0
			lose = 1
		}

		var matchingChild *CustomNode
		for _, child := range currentNode.Children {
			if child.Color == move.Color && child.Move == move.Move {
				matchingChild = child
			}
		}

		if matchingChild == nil {
			GamesArray := []primitive.ObjectID{gibo.ID}
			yearlyStatArray := []YearlyStat{{
				Year:  gibo.Date[:4],
				Count: 1,
				Win:   win,
				Lose:  lose},
			}
			tmpNode := CustomNode{
				Parent:     currentNode,
				Move:       move.Move,
				Color:      move.Color,
				Games:      GamesArray,
				YearlyStat: yearlyStatArray,
			}
			// Append yealy
			currentNode.Children = append(currentNode.Children, &tmpNode)
			currentNode = &tmpNode
		} else {
			for i, year := range matchingChild.YearlyStat {
				tmpYearlyStat := YearlyStat{
					Year:  year.Year,
					Count: year.Count + 1,
					Win:   year.Win + win,
					Lose:  year.Lose + lose,
				}
				if year.Year == gibo.Date[:4] {
					matchingChild.YearlyStat[i] = tmpYearlyStat
				}
			}
			currentNode = matchingChild

		}
	}
}

func traverse(node *CustomNode, parentID primitive.ObjectID, assignedID primitive.ObjectID) []interface{} {

	var childrenID = make([]primitive.ObjectID, len(node.Children))

	var returnValue []interface{}
	for i, child := range node.Children {
		childrenID[i] = primitive.NewObjectID()
		output := traverse(child, parentID, childrenID[i])
		returnValue = append(returnValue, output...)
	}
	tmpNode := Node{
		ID:         assignedID,
		Color:      node.Color,
		Move:       node.Move,
		Root:       node.Root,
		Parent:     parentID,
		Children:   childrenID,
		YearlyStat: node.YearlyStat,
	}
	returnValue = append(returnValue, tmpNode)
	return returnValue

}

func reflect(character string) string {
	reflection := map[string]string{
		"s": "a", "r": "b", "q": "c", "p": "d", "o": "e", "n": "f", "m": "g", "l": "h", "k": "i", "j": "j",
		"a": "s", "b": "r", "c": "q", "d": "p", "e": "o", "f": "n", "g": "m", "h": "l", "i": "k"}

	return reflection[character]
}

func queryMoves() *mongo.Cursor {
	ctx, cancel := context.WithTimeout(context.Background(), 1*time.Second)
	defer cancel()

	client, err := mongo.NewClient(options.Client().ApplyURI(os.Getenv("DB_URI")))
	if err != nil {
		log.Fatal(err)
	}
	err = client.Connect(ctx)
	if err != nil {
		log.Fatal(err)
	}

	giboCollection := client.Database("trenduk").Collection("gibo")

	cursor, err := giboCollection.Find(context.Background(), bson.D{})
	return cursor
}

func insertManyMoves(nodeArray []interface{}) {
	ctx, cancel := context.WithTimeout(context.Background(), 1*time.Second)
	defer cancel()

	client, err := mongo.NewClient(options.Client().ApplyURI(os.Getenv("DB_URI")))
	if err != nil {
		log.Fatal(err)
	}
	err = client.Connect(ctx)
	if err != nil {
		log.Fatal(err)
	}

	nodeCollection := client.Database("trenduk").Collection("node")

	nodeCollection.InsertMany(context.Background(), nodeArray)
}

func checkWinner(resultString string) string {
	res := strings.Contains(resultString, "흑")
	if res {
		return "B"
	} else {
		return "W"
	}
}
