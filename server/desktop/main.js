const { app, BrowserWindow } = require("electron");

function createWindow() {
  window = new BrowserWindow({ width: 1200, height: 600 });
  window.loadFile("index.html");

  var python = require("child_process").spawn("python", ["./hello.py"]);
  python.stdout.on("data", function (data) {
    // console.log("data: ",data.toString('utf8'));
  });
}

app.on("ready", createWindow);

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});
