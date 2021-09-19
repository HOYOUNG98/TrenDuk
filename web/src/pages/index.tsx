// library imports
import React, { useEffect, useState } from "react";
import { useSelector, useDispatch } from "react-redux";

// local imports
import { WGoBoard } from "../components/WGoBoard";
import { Chart } from "../components/Chart";
import { RootState } from "../store";
import { NavBar } from "../components/NavBar";
import {
  Box,
  Flex,
  Text,
  HStack,
  Radio,
  RadioGroup,
  VStack,
  Wrap,
} from "@chakra-ui/react";
import { ReactVisDataReducer } from "../helpers/rechartConversion";
import { IReactVisData } from "../types";

const Index: React.FC = () => {
  const [yearlyPick, yearlyPickUpate] = useState<IReactVisData[]>([]);
  const [yearlyWin, yearlyWinUpdate] = useState<IReactVisData[]>([]);

  const { currentMoves, hoverPoint, selectedColor } = useSelector(
    (state: RootState) => ({
      currentMoves: state.node.currentMoves,
      hoverPoint: state.current.hoverPoint,
      selectedColor: state.current.selectedColor,
    })
  );

  useEffect(() => {
    yearlyPickUpate(
      ReactVisDataReducer(currentMoves, hoverPoint, "pick_percentage")
    );
    yearlyWinUpdate(
      ReactVisDataReducer(currentMoves, hoverPoint, "win_percentage")
    );
  }, [hoverPoint, currentMoves]);

  return (
    <Flex direction="column">
      <NavBar />
      <Flex
        width="100%"
        height="100%"
        marginTop="-50px"
        justifyContent="center"
        alignItems="center"
        direction={["column", "column", "row", "row"]}
      >
        {/* Moves List */}
        <Flex
          width={["100%", "160px", "160px", "160px"]}
          height={["100px", "500px", "500px", "500px"]}
          direction={["row", "row", "column", "column"]}
          overflowX="auto"
        >
          <Box borderWidth="1px" height="100px" width="160px" borderRadius="lg">
            <Text fontSize="xl">MOVE</Text>
            <Text fontSize="medium">Description</Text>
          </Box>

          <Box borderWidth="1px" height="100px" width="160px" borderRadius="lg">
            <Text fontSize="large">MOVE</Text>
            <Text fontSize="medium">Description</Text>
          </Box>

          <Box borderWidth="1px" height="100px" width="160px" borderRadius="lg">
            <Text fontSize="large">MOVE</Text>
            <Text fontSize="medium">Description</Text>
          </Box>
          <Box borderWidth="1px" height="100px" width="160px" borderRadius="lg">
            <Text fontSize="large">MOVE</Text>
            <Text fontSize="medium">Description</Text>
          </Box>
          <Box borderWidth="1px" height="100px" width="160px" borderRadius="lg">
            <Text fontSize="large">MOVE</Text>
            <Text fontSize="medium">Description</Text>
          </Box>
          <Box borderWidth="1px" height="100px" width="160px" borderRadius="lg">
            <Text fontSize="large">MOVE</Text>
            <Text fontSize="medium">Description</Text>
          </Box>
          <Box borderWidth="1px" height="100px" width="160px" borderRadius="lg">
            <Text fontSize="large">MOVE</Text>
            <Text fontSize="medium">Description</Text>
          </Box>
          <Box
            borderWidth="1px"
            height="100px"
            width="160pxs"
            borderRadius="lg"
          >
            <Text fontSize="large">MOVE</Text>
            <Text fontSize="medium">Description</Text>
          </Box>
        </Flex>
        {/* Board */}
        <WGoBoard />
        {/* Charts */}
        <Flex
          width={["100%", "40%", "40%", "40%"]}
          height={["100px", "500px", "500px", "500px"]}
          direction={["row", "row", "column", "column"]}
          overflow="auto"
        >
          <Chart
            data={yearlyPick}
            move={hoverPoint}
            variant={"Pick Rate (%)"}
          />
          <Chart data={yearlyWin} move={hoverPoint} variant={"Win Rate (%)"} />
        </Flex>
      </Flex>
    </Flex>
  );
};

export default Index;
