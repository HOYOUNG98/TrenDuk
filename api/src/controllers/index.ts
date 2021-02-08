// import libraries
import { Request, Response } from "express";
import { Types } from "mongoose";

// import local files
import GiboModel from "../models/gibo.model";
import NodeModel from "../models/node.model";

/*
  Global and general definitions
*/
interface ResponseBody {
  status: number;
  data: object | null;
  error?: null | object;
}

/*
  /getBranches request
  Receives id of a node and returns the childrens
*/

interface GetBranchesRequestData {
  nodeID: Types.ObjectId | null;
}

export const getBranches = async (req: Request, res: Response) => {
  const data: GetBranchesRequestData = req.body;

  try {
    const node = data.nodeID
      ? await NodeModel.getNodeByID(data.nodeID)
      : await NodeModel.getRootNode();

    const blackChildrenNodes = await NodeModel.getBlackChildrenNodes(node._id);
    const whiteChildrenNodes = await NodeModel.getWhiteChildrenNodes(node._id);

    const body: ResponseBody = {
      status: 200,
      data: { blackChildrenNodes, whiteChildrenNodes },
    };
    res.status(200);
    res.json(body);
  } catch (error) {
    console.log(error);

    const body: ResponseBody = {
      status: 500,
      data: null,
      error,
    };
    res.status(500);
    res.json(body);
  } finally {
    res.send();
  }
};

interface GetBranchPointsRequestData {
  nodeID: Types.ObjectId | null;
}

export const getBranchPoints = async (req: Request, res: Response) => {
  const data: GetBranchPointsRequestData = req.body;

  let black, white;
  try {
    const node = data.nodeID
      ? await NodeModel.getNodeByID(data.nodeID)
      : await NodeModel.getRootNode();

    const blackBranchPoints = await NodeModel.getBlackBranchMoves(node._id);
    const whiteBranchPoints = await NodeModel.getWhiteBranchMoves(node._id);

    console.log(blackBranchPoints);

    black = blackBranchPoints.map((node) => {
      return {
        _id: node._id,
        x: node.move[0].charCodeAt(0) - 97,
        y: node.move[1].charCodeAt(0) - 97,
      };
    });

    white = whiteBranchPoints.map((node) => {
      return {
        _id: node._id,
        x: node.move[0].charCodeAt(0) - 97,
        y: node.move[1].charCodeAt(0) - 97,
      };
    });
  } catch (error) {
    console.log(error);
    return res.send({ status: "500", error });
  }

  return res.send({ status: "200", black, white });
};

/*
  /getGibos request
  Receives id of a node and returns corresponding gibos
*/

interface GetGibosRequestData {
  nodeID: Types.ObjectId;
}

export const getGibos = async (req: Request, res: Response) => {
  const data: GetGibosRequestData = req.body;

  try {
    const node = await NodeModel.getNodeByID(data.nodeID);

    const relatedGiboArray = await GiboModel.getGiboByIDBatch(node.games);

    const body: ResponseBody = {
      status: 200,
      data: { relatedGiboArray },
    };
    res.status(200);
    res.json(body);
  } catch (error) {
    console.log(error);

    const body: ResponseBody = {
      status: 500,
      data: null,
      error,
    };
    res.status(500);
    res.json(body);
  } finally {
    res.send();
  }
};
