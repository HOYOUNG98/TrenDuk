import { Document, Model, model, Schema, Types } from "mongoose";

const NodeSchema = new Schema({
  root: Boolean,
  parentID: { type: Schema.Types.ObjectId, ref: "Node" },
  childrenID: [{ type: Schema.Types.ObjectId, ref: "Node" }],
  move: String,
  color: String,
  games: [{ type: Schema.Types.ObjectId, ref: "Gibo" }],
  yearPickCount: { type: Map, of: Number },
});

interface Node {
  root: Boolean;
  parentID: Types.ObjectId;
  childrenID: [Types.ObjectId];
  move: string;
  color: string;
  games: [Types.ObjectId];
  yearPickCount: Map<string, number>;
}

NodeSchema.virtual("gamesCount").get(function (this: Node) {
  return this.games.length;
});

export interface NodeDocument extends Node, Document {
  gamesCount: number;
}

// Parent ID matches id given and color is "B"
// Show top 4 with most game counts
// Project only parentID, move, color, yearPickCount
NodeSchema.statics.getBlackChildrenNodes = async function (id: Types.ObjectId) {
  return this.aggregate([
    { $project: { _id: 1, parentID: 1, move: 1, color: 1, yearPickCount: 1 } },
    { $match: { parentID: id, color: "B" } },
    { $sort: { gamesCount: -1 } },
    { $limit: 4 },
  ]).exec();
};

// Parent ID matches id given and color is "W"
// Show top 4 with most game counts
// Project only parentID, move, color, yearPickCount
NodeSchema.statics.getWhiteChildrenNodes = async function (id: Types.ObjectId) {
  return this.aggregate([
    { $project: { _id: 1, parentID: 1, move: 1, color: 1, yearPickCount: 1 } },
    { $match: { parentID: id, color: "W" } },
    { $sort: { gamesCount: -1 } },
    { $limit: 4 },
  ]).exec();
};

NodeSchema.statics.getNodeByID = async function (id: Types.ObjectId) {
  return this.findById(id).exec();
};

NodeSchema.statics.getRootNode = async function () {
  return this.findOne({ root: true }).exec();
};

export interface NodeModel extends Model<NodeDocument> {
  getBlackChildrenNodes(id: Types.ObjectId): Promise<[NodeDocument]>;
  getWhiteChildrenNodes(id: Types.ObjectId): Promise<[NodeDocument]>;

  getNodeByID(id: Types.ObjectId): Promise<NodeDocument>;
  getRootNode(): Promise<NodeDocument>;
}

export default model<NodeDocument, NodeModel>("node", NodeSchema, "node");
