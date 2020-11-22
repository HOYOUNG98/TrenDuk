// library imports
import React from "react";
import { BrowserRouter, Switch, Route } from "react-router-dom";

// local imports
import { Header } from "./components/header";
import { Board } from "./components/board";
import { GiboTable, RateStat } from "./components/stat";
import "./app.css";
import "antd/dist/antd.css";

const App = () => {
  return (
    <div className="outline-container">
      <BrowserRouter>
        <Header />
        <Switch>
          <Route exact path="/">
            <div className="board">
              <Board />
            </div>
            <div className="divider" />
            <div className="stat">
              <div>
                <RateStat />
              </div>
              <div>
                <GiboTable />
              </div>
            </div>
          </Route>
          <Route exact path="/about">
            <div>ABOUT PAGE </div>
          </Route>
        </Switch>
      </BrowserRouter>
    </div>
  );
};

export default App;
