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

  let nodes;
  try {
    const node = data.nodeID
      ? await NodeModel.getNodeByID(data.nodeID)
      : await NodeModel.getRootNode();

    const blackChildrenNodes = await NodeModel.getBlackChildrenNodes(node._id);
    const whiteChildrenNodes = await NodeModel.getWhiteChildrenNodes(node._id);

    nodes = [...blackChildrenNodes, ...whiteChildrenNodes];
  } catch (error) {
    return res.send({ status: "500", error });
  }
  return res.send({
    status: "200",
    data: nodes,
  });
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
