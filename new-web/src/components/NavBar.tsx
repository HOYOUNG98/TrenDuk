// library imports
import { Box, Flex } from "@chakra-ui/react";
import React from "react";

interface NavBarProps {}

export const NavBar: React.FC<NavBarProps> = ({}) => {
  return (
    <Flex bg="SlateGrey" p={4}>
      <Box ml={"auto"}>Trenduk</Box>
    </Flex>
  );
};
