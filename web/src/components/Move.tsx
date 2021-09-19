import { Box, Flex, Text } from "@chakra-ui/react";
import React from "react";

interface MoveProps {
  move: string;
  pick: number;
  win: number;
}

export const Move: React.FC<MoveProps> = ({ move, pick, win }) => {
  return (
    <Box
      borderWidth="1px"
      height="80px"
      width="140px"
      minWidth="140px"
      borderRadius="sm"
      marginBottom={["0", "0", "5px", "5px"]}
      marginRight={["5px", "5px", "0", "0"]}
    >
      <Flex marginLeft={"10px"} direction={"column"} justifyContent="center">
        <Text fontSize="xl" fontWeight="bold">
          {move}
        </Text>
        <Text fontSize="small" fontFamily="sans-serif">
          Pick Rate: {pick}%
        </Text>
        <Text fontSize="small" fontFamily="sans-serif">
          Win Rate: {win}%
        </Text>
      </Flex>
    </Box>
  );
};
