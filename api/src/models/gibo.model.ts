import { Document, Model, model, Schema, Types } from "mongoose";

const GiboSchema = new Schema({
  giboName: String,
  giboDate: String,
  giboLocation: String,
  giboMinutes: Number,
  giboSeconds: Number,
  giboTimeCount: Number,
  giboKomi: Number,
  giboResult: String,
  giboBlackPlayerName: String,
  giboBlackPlayerRank: String,
  giboWhitePlayerName: String,
  giboWhitePlayerRank: String,
  giboMoves: [String],
  giboLink: String,
  published: Date,
  analyzed: Boolean,
});

interface Gibo {
  giboName: string;
  giboDate: string;
  giboLocation: string;
  giboMinutes: number;
  giboSeconds: number;
  giboTimeCount: number;
  giboKomi: number;
  giboResult: string;
  giboBlackPlayerName: string;
  giboBlackPlayerRank: string;
  giboWhitePlayerName: string;
  giboWhitePlayerRank: string;
  giboMoves: [string];
  giboLink: string;
  published: Date;
  analyzed: boolean;
}

export interface GiboDocument extends Gibo, Document {}

// Receives list of ID and returns corresponding instances
// Shows only 10 instances
GiboSchema.statics.getGiboByIDBatch = async function (
  nodeIDArray: [Types.ObjectId]
) {
  return this.find(
    { _id: { $in: nodeIDArray } },
    "giboName giboDate giboBlackPlayerName giboWhitePlayerName"
  )
    .limit(10)
    .exec();
};

export interface GiboModel extends Model<GiboDocument> {
  getGiboByIDBatch(nodeIDArray: [Types.ObjectId]): Promise<[GiboDocument]>;
}

export default model<GiboDocument, GiboModel>("gibo", GiboSchema, "gibo");
