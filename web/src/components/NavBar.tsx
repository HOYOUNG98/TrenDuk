// library imports
import { LinkIcon } from "@chakra-ui/icons";
import { Box, Flex, Link } from "@chakra-ui/react";
import React from "react";

interface NavBarProps {}

export const NavBar: React.FC<NavBarProps> = ({}) => {
  return (
    <Flex boxShadow="0 2px 8px #f0f1f2" p={4}>
      <Box fontSize="1.2em">Trenduk</Box>
      <Box ml={"auto"}>
        <Link isExternal href="https://github.com/HOYOUNG98/TrenDuk">
          Github <LinkIcon />
        </Link>
      </Box>
    </Flex>
  );
};
