// library imports
import { Text, Flex } from "@chakra-ui/react";
import React from "react";

interface NavBarProps {}

export const NavBar: React.FC<NavBarProps> = ({}) => {
  return (
    <Flex
      background="black"
      minHeight={["40px", "40px", "50px", "50px"]}
      alignItems="center"
      justifyContent="center"
    >
      <Text color="white" fontWeight="600" fontFamily="sans-serif">
        Which moves are popular?
      </Text>
    </Flex>
  );
};
