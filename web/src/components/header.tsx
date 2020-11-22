// library imports
import React from "react";
import { useHistory } from "react-router-dom";

// local imports

export const Header = () => {
  const history = useHistory();

  return (
    <header>
      <div className="inner">
        <div
          className="title"
          onClick={() => {
            history.push("/");
          }}
        >
          TrenDuk
        </div>
        <nav className="links">
          <a href="https://github.com/HOYOUNG98/TrenDuk">GitHub</a>
        </nav>
      </div>
    </header>
  );
};
