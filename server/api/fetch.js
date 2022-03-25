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
}

const fetchMove = () => {
  var pyshell = require("python-shell");
  pyshell.run("hello.py", function (_, results) {
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

    new Chart(document.getElementById("pick_rate"), pick_rate_config);

    var pick_rate_dataset = [];

    for (const [move, data] of Object.entries(res.win_rate)) {
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

    const win_rate_config = {
      type: "line",
      data: {
        labels: Array.from(new Array(23), (_, i) => i + 2000),
        datasets: pick_rate_dataset,
      },
      options: {},
    };

    new Chart(document.getElementById("win_rate"), win_rate_config);
  });
};
