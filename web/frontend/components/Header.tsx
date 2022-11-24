import { FC } from "react";
import { Icon, Center, Box } from "@chakra-ui/react";
import { FiCode } from "react-icons/fi";
import { GiPirateFlag } from "react-icons/gi";
import { AiOutlineHeart } from "react-icons/ai";
import NextLink from "next/link";

export const Header: FC = () => {
  return (
    <Center minH="50px" maxH="50px" bg="#000000" color="#ffffff" stroke="">
      See which sequences are popular among professional Go players!
    </Center>
  );
};
