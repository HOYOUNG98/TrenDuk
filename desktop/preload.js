const { contextBridge } = require("electron");
const path = require("path");
const sqlite3 = require("sqlite3").verbose();

/**
 * The preload script runs before. It has access to web APIs
 * as well as Electron's renderer process modules and some
 * polyfilled Node.js functions.
 *
 * https://www.electronjs.org/docs/latest/tutorial/sandbox
 */
window.addEventListener("DOMContentLoaded", () => {
  const replaceText = (selector, text) => {
    const element = document.getElementById(selector);
    if (element) element.innerText = text;
  };

  for (const type of ["chrome", "node", "electron"]) {
    replaceText(`${type}-version`, process.versions[type]);
  }
});

contextBridge.exposeInMainWorld("api", {
  query: (move, color, sequence_depth, parent_id) => {
    let dbFile = path.join(__dirname, "data/main.db");
    const db = new sqlite3.Database(dbFile);

    let sql = `
          WITH children AS (
            SELECT child_id
            FROM node 
                JOIN is_child ON node.node_id = is_child.parent_id
            WHERE parent_id = $1
        ),

        total AS (
            SELECT Substr(game.datetime, 0, 5) as year, COUNT(*) AS total
            FROM node_game
                JOIN children ON node_game.node_id = children.child_id
                JOIN game ON node_game.game_id = game.game_id
            GROUP BY Substr(game.datetime, 0, 5)
        ),

        game_ AS (
            SELECT *,
                CASE 
                    WHEN Substr(game.result, 0, 2) = $2 THEN 1
                    WHEN Substr(game.result, 0, 2) <> $2 THEN 0
                END AS win
            FROM game
        ),

        res AS (
            SELECT children.child_id as move, Substr(game_.datetime, 0, 5) as year, CAST(SUM(win) AS FLOAT) / CAST(COUNT(*) AS FLOAT) as win_rate, COUNT(*) as sub_total
            FROM node_game
                JOIN game_ ON game_.game_id = node_game.game_id
                JOIN children ON children.child_id = node_game.node_id
            GROUP BY children.child_id, Substr(game_.datetime, 0, 5)
            HAVING sub_total > 5
        )

        SELECT Substr(move, 0, 5) as move, res.year, res.win_rate, CAST(sub_total AS FLOAT) / CAST(total.total as FLOAT) as pick_rate
        FROM res LEFT JOIN total ON res.year = total.year;
            `;
    const id = `${move}${color}${sequence_depth}${parent_id}`;

    return new Promise((resolve, _) => {
      db.all(sql, [id, color], (err, rows) => {
        if (err) {
          return console.error(err.message);
        }

        let unique_moves = [...new Set(rows.map((row) => row.move))];

        let pick_rates = {};
        let win_rates = {};
        unique_moves.forEach((move) => {
          pick_rates[move] = new Array(23).fill(0);
          win_rates[move] = new Array(23).fill(0);
        });

        rows.forEach(
          ({
            move: _move,
            year: _year,
            win_rate: _win_rate,
            pick_rate: _pick_rate,
          }) => {
            if (_year >= 2000 && _year <= 2022) {
              pick_rates[_move][_year - 2000] = _pick_rate;
              win_rates[_move][_year - 2000] = _win_rate;
            }
          }
        );

        // filter out datapoints that doesn't pass threshold.
        // if a move has never passed a pick rate of 10% throughout entire years, eliminate it.

        const THRESHOLD = 0.1;

        const entries = Object.entries(pick_rates);
        const filtered_keys = entries
          .filter((entry) => Math.max(...entry[1]) >= THRESHOLD)
          .map((entry) => entry[0]);

        notable_pick_rates = Object.keys(win_rates)
          .filter((key) => filtered_keys.includes(key))
          .reduce((obj, key) => {
            obj[key] = pick_rates[key];
            return obj;
          }, {});

        notable_win_rates = Object.keys(win_rates)
          .filter((key) => filtered_keys.includes(key))
          .reduce((obj, key) => {
            obj[key] = win_rates[key];
            return obj;
          }, {});

        db.close();

        resolve({ pick_rate: notable_pick_rates, win_rate: notable_win_rates });
      });
    });
  },
});
