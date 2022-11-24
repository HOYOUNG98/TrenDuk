import { FC } from "react";
import { Icon, Center, Box } from "@chakra-ui/react";
import { FiCode } from "react-icons/fi";
import { RiWindyLine } from "react-icons/ri";
import { AiOutlineHeart } from "react-icons/ai";
import NextLink from "next/link";

export const Footer: FC = () => {
  return (
    <Center minH="50px" maxH="50px">
      Powered by
      <NextLink href="https://github.com/HOYOUNG98/TrenDuk" passHref>
        <Icon as={FiCode} marginTop="7px" marginLeft="4px" marginRight="5px" />
      </NextLink>
      · <Box width="5px" />
      Made in
      <Icon as={RiWindyLine} marginLeft="4px" marginRight="5px" />
    </Center>
  );
};
