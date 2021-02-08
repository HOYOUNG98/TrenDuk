// import libraries
import express from "express";
import mongoose from "mongoose";
import cors from "cors";
import dotenv from "dotenv";
import bodyParser from "body-parser";

// import local files
import { getBranches, getBranchPoints, getGibos } from "./controllers";

const app = express();

dotenv.config();
const url = process.env.DB_URL || "undefined";

// DB connection
const connectDB = async () => {
  await mongoose
    .connect(url, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => {
      console.log("Database connection established.");
    })
    .catch((err: any) => {
      console.log(err);
    });
};

app.use(bodyParser.json());
app.use(cors());
app.get("/", function (req, res) {
  res.send("hello world");
});
// Created Request URLs
app.post("/getBranches", getBranches);
app.post("/getGibos", getGibos);
app.post("/getBranchPoints", getBranchPoints);

// We don't start server unless DB connection is established
const executeServer = async () => {
  await connectDB();

  app.listen(process.env.PORT, () => {
    console.log(`App listening on port ${process.env.PORT}`);
  });
};

executeServer();
