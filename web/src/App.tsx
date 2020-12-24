// library imports
import React, { useEffect } from "react";
import { BrowserRouter, Switch, Route } from "react-router-dom";

// local imports
import { Header } from "./components/header";
import { Board } from "./components/board";
import { GiboTable, RateStat } from "./components/stat";
import "./app.css";
import "antd/dist/antd.css";
import { shallowEqual, useSelector } from "react-redux";
import { RootState } from "./cache";
import { BarLoader } from "react-spinners";
import { getBranches } from "./api/getBranches";

const App = () => {
  // Wait for API request - API request when render
  useEffect(() => {
    getBranches();
  }, []);

  const { blackBranchNodes, whiteBranchNodes } = useSelector(
    (state: RootState) => ({
      blackBranchNodes: state.node.blackBranchNodes,
      whiteBranchNodes: state.node.whiteBranchNodes,
    }),
    shallowEqual
  );
  console.log(blackBranchNodes, whiteBranchNodes);
  return (
    <div className="outline-container">
      <BrowserRouter>
        <Header />
        {blackBranchNodes.length === 0 && whiteBranchNodes.length === 0 ? (
          <div
            style={{
              width: "100vw",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              flexWrap: "wrap",
            }}
          >
            <BarLoader />
          </div>
        ) : (
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
        )}
      </BrowserRouter>
    </div>
  );
};

export default App;
