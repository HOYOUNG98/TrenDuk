function initiateBoard() {
  var board = new WGo.Board(document.getElementById("board"), {
    width: 400,
    section: {
      top: 0,
      left: 9,
      right: 0,
      bottom: 9,
    },
  });

  var curr_color = WGo.B;
  var parent_id = "rootroot0root";

  board.addEventListener("click", function (x, y) {
    console.log(curr_color);
    board.addObject({
      x: x,
      y: y,
      c: curr_color,
    });

    const move = String.fromCharCode(x + 97) + String.fromCharCode(18 - y + 97);
    const color = curr_color;
    const sequence_depth = board
      .getState()
      .objects.map((state) => {
        var res = 0;
        for (let i = 0; i < state.length; i++) {
          res += state[i].length;
        }
        return res;
      })
      .reduce((a, b) => {
        return a + b;
      });

    const color_ = color === WGo.B ? "B" : "W";
    fetchMove(move, color_, sequence_depth, parent_id);

    curr_color = curr_color === WGo.B ? WGo.W : WGo.B;
    parent_id = move + color_ + sequence_depth + parent_id;
    console.log(parent_id);
  });
}

const fetchMove = (move, color, sequence_depth, parent_id) => {
  var pyshell = require("python-shell");
  pyshell.run(
    "./scripts/move.py",
    { args: [move, color, sequence_depth, parent_id] },
    function (err, results) {
      console.log(move, color, sequence_depth, results);
      const res = JSON.parse(results[0]);

      var pick_rate_dataset = [];

      for (const [move, data] of Object.entries(res.pick_rate)) {
        const updated_data = data.map((val) => {
          return val === 0 ? NaN : val;
        });

        const randomColor =
          "#" + Math.floor(Math.random() * 16777215).toString(16);

        pick_rate_dataset.push({
          label: move,
          backgroundColor: randomColor,
          borderColor: randomColor,
          data: updated_data,
        });
      }

      const pick_rate_config = {
        type: "line",
        data: {
          labels: Array.from(new Array(23), (_, i) => i + 2000),
          datasets: pick_rate_dataset,
        },
        options: {},
      };

      var old_chart = Chart.getChart("pick_rate");
      if (old_chart) old_chart.destroy();
      new Chart(
        document.getElementById("pick_rate").getContext("2d"),
        pick_rate_config
      );

      var win_rate_dataset = [];

      for (const [move, data] of Object.entries(res.win_rate)) {
        const updated_data = data.map((val) => {
          return val === 0 ? NaN : val;
        });

        const randomColor =
          "#" + Math.floor(Math.random() * 16777215).toString(16);

        win_rate_dataset.push({
          label: move,
          backgroundColor: randomColor,
          borderColor: randomColor,
          data: updated_data,
        });
      }

      const win_rate_config = {
        type: "line",
        data: {
          labels: Array.from(new Array(23), (_, i) => i + 2000),
          datasets: pick_rate_dataset,
        },
        options: {},
      };

      var old_chart = Chart.getChart("win_rate");
      if (old_chart) old_chart.destroy();
      new Chart(
        document.getElementById("win_rate").getContext("2d"),
        win_rate_config
      );

      return pick_rate_chart;
    }
  );
};
