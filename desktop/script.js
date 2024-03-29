function initiateBoard() {
  var board = new WGo.Board(document.getElementById("board"), {
    width: 555,
    section: {
      top: 0,
      left: 9,
      right: 0,
      bottom: 9,
    },
  });

  var curr_color = WGo.B;
  var parent_id = "rootroot0root";
  var valid_moves = [];

  board.addEventListener("click", async function (x, y) {
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
    let res = await window.api.query(move, color_, sequence_depth, parent_id);

    // Add options to our board
    unique_moves = [];

    let moves = Object.keys(res.pick_rate).map((val) => val.slice(0, 2));

    Object.keys(res.pick_rate).forEach((move) => {
      var new_color = curr_color === WGo.B ? "W" : "B";
      if (move.substring(2, 3) === new_color) {
        move = move.slice(0, 2);
        board.addObject({
          x: move[0].charCodeAt(0) - 97,
          y: 115 - move[1].charCodeAt(0),
          type: "MA",
        });
      }
    });

    valid_moves = unique_moves;

    updateChart(res, curr_color);

    curr_color = curr_color === WGo.B ? WGo.W : WGo.B;
    parent_id = move + color_ + sequence_depth + parent_id;
  });

  board.addEventListener("mousemove", function (x, y) {
    const move = String.fromCharCode(x + 97) + String.fromCharCode(18 - y + 97);
    var pick_rate_chart = Chart.getChart("pick_rate");

    if (!pick_rate_chart) return;

    var flag = false;
    for (let i = 0; i < pick_rate_chart._metasets.length; i++) {
      if (move === pick_rate_chart._metasets[i].label.substring(0, 2))
        flag = true;
    }
    if (!flag) return;

    var pick_rate_dataset = [];
    for (let i = 0; i < pick_rate_chart._metasets.length; i++) {
      const backgroundColor =
        pick_rate_chart._metasets[i]._dataset.backgroundColor;
      const borderColor = pick_rate_chart._metasets[i]._dataset.borderColor;
      const borderWidth =
        move === pick_rate_chart._metasets[i].label.substring(0, 2) ? 3 : 0.5;

      pick_rate_dataset.push({
        label: pick_rate_chart._metasets[i].label,
        backgroundColor,
        borderColor,
        borderWidth,
        data: pick_rate_chart._metasets[i]._dataset.data,
      });
    }

    pick_rate_chart.options.animation.duration = 0;
    pick_rate_chart.data.datasets = pick_rate_dataset;
    pick_rate_chart.update();

    var win_rate_chart = Chart.getChart("win_rate");

    if (!win_rate_chart) return;

    var flag = false;
    for (let i = 0; i < win_rate_chart._metasets.length; i++) {
      if (move === win_rate_chart._metasets[i].label.substring(0, 2))
        flag = true;
    }
    if (!flag) return;

    var win_rate_dataset = [];
    for (let i = 0; i < win_rate_chart._metasets.length; i++) {
      const backgroundColor =
        win_rate_chart._metasets[i]._dataset.backgroundColor;
      const borderColor = win_rate_chart._metasets[i]._dataset.borderColor;
      const borderWidth =
        move === win_rate_chart._metasets[i].label.substring(0, 2) ? 3 : 0.5;

      win_rate_dataset.push({
        label: win_rate_chart._metasets[i].label,
        backgroundColor,
        borderColor,
        borderWidth,
        data: win_rate_chart._metasets[i]._dataset.data,
      });
    }

    win_rate_chart.options.animation.duration = 0;
    win_rate_chart.data.datasets = win_rate_dataset;
    win_rate_chart.update();
  });
}

const updateChart = ({ pick_rate, win_rate }, new_color) => {
  var pick_rate_dataset = [];
  var win_rate_dataset = [];

  var new_color = new_color === WGo.B ? "B" : "W";
  for (const [move, data] of Object.entries(pick_rate)) {
    if (move.substring(2, 3) === new_color) {
      continue;
    }

    const pick_rate_data = data.map((val) => {
      return val === 0 ? NaN : val;
    });

    const win_rate_data = win_rate[move].map((val) => {
      return val === 0 ? NaN : val;
    });

    const randomColor = "#" + Math.floor(Math.random() * 16777215).toString(16);

    pick_rate_dataset.push({
      label: move,
      backgroundColor: randomColor,
      borderColor: randomColor,
      data: pick_rate_data,
    });

    win_rate_dataset.push({
      label: move,
      backgroundColor: randomColor,
      borderColor: randomColor,
      data: win_rate_data,
    });
  }

  const pick_rate_config = {
    type: "line",
    data: {
      labels: Array.from(new Array(23), (_, i) => i + 2000),
      datasets: pick_rate_dataset,
    },
    options: {
      plugins: {
        title: {
          display: true,
          text: "pick rate",
        },
      },
    },
  };

  var old_chart = Chart.getChart("pick_rate");
  if (old_chart) old_chart.destroy();
  new Chart(
    document.getElementById("pick_rate").getContext("2d"),
    pick_rate_config
  );

  const win_rate_config = {
    type: "line",
    data: {
      labels: Array.from(new Array(23), (_, i) => i + 2000),
      datasets: win_rate_dataset,
    },
    options: {
      plugins: {
        title: {
          display: true,
          text: "win rate",
        },
      },
    },
  };

  var old_chart = Chart.getChart("win_rate");
  if (old_chart) old_chart.destroy();
  new Chart(
    document.getElementById("win_rate").getContext("2d"),
    win_rate_config
  );
};
