import {
  Box,
  Center,
  Container,
  Flex,
  Grid,
  GridItem,
  Spacer,
  Wrap,
  WrapItem,
} from "@chakra-ui/react";
import Head from "next/head";
import axios from "axios";

import { ChildStats } from "../components/ChildStats";
import { Goban } from "../components/Goban";
import { useEffect, useState } from "react";
import { Footer } from "../components/Footer";
import { Header } from "../components/Header";
import { colorObjToStr, colorStrToObj } from "../utils/helper";

interface IData {
  [key: string]: {
    pick_rates: any;
    win_rates: any;
  };
}

interface IMove {
  color: "B" | "W";
  x: number;
  y: number;
  depth: number;
}
export default function Home() {
  const [currentNode, updateNode] = useState<string>("rootroot0root");
  const [data, setData] = useState<IData>({});
  const [moves, updateMoves] = useState<Array<IMove>>([]);

  useEffect(() => {
    if (currentNode !== "rootroot0root") {
      updateMoves((old) => [...old, colorStrToObj(currentNode)]);
    }

    const queryParam =
      (currentNode !== "rootroot0root" ? currentNode : "") +
      moves
        .reverse()
        .map((move: IMove) => colorObjToStr(move))
        .join("") +
      "rootroot0root";

    axios
      .get(
        `https://cs2wm0wty9.execute-api.us-east-1.amazonaws.com/production/rates_by_parent?parent=${queryParam}`
      )
      .then((response) => {
        setData(response.data);
      });
  }, [currentNode]);

  return (
    <div>
      <Head>
        <title>TrenDuk</title>
        <meta name="description" content="Generated by create next app" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Header />
      <Container maxW="100rem" marginTop="20px">
        <Flex direction="column" minH="86vh" maxH="86vh">
          <Wrap direction="row">
            <Center>
              <WrapItem margin="50px">
                <Goban size={500} moves={moves} />
              </WrapItem>
            </Center>
            <Center>
              <WrapItem>
                <Box
                  overflowY="auto"
                  maxHeight="86vh"
                  minHeight="86vh"
                  width="100%"
                  css={{
                    "&::-webkit-scrollbar": {
                      width: "0",
                    },
                  }}
                >
                  <Grid templateColumns="repeat(2, 4fr)" gap={6}>
                    {Object.keys(data).map((key, _) => {
                      const curr_move = colorStrToObj(key);
                      return (
                        <div key={key}>
                          <ChildStats
                            pickRate={data[key]["pick_rates"]}
                            winRate={data[key]["win_rates"]}
                            moves={[...moves, curr_move]}
                            updateNode={updateNode}
                            updateMoves={updateMoves}
                          />
                        </div>
                      );
                    })}
                  </Grid>
                </Box>
              </WrapItem>
            </Center>
          </Wrap>
        </Flex>
      </Container>
      <Footer />
    </div>
  );
}
