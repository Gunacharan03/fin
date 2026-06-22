import { Flex, HStack, Heading, Spacer, Avatar, Menu, MenuButton, MenuList, MenuItem, Text, IconButton } from "@chakra-ui/react";
import { FiMenu, FiLogOut, FiUser } from "react-icons/fi";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar({ onMenuClick }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <Flex
      as="header"
      align="center"
      px={5}
      py={3}
      bg="white"
      borderBottom="1px solid"
      borderColor="surface.200"
      position="sticky"
      top={0}
      zIndex={10}
    >
      <IconButton
        aria-label="Open menu"
        icon={<FiMenu />}
        variant="ghost"
        display={{ base: "inline-flex", md: "none" }}
        onClick={onMenuClick}
        mr={3}
      />
      <Heading size="md" color="brand.500" letterSpacing="-0.02em">
        Fin
      </Heading>
      <Spacer />
      <Menu>
        <MenuButton>
          <HStack spacing={3}>
            <Text fontSize="sm" color="gray.600" display={{ base: "none", sm: "block" }}>
              {user?.name}
            </Text>
            <Avatar size="sm" name={user?.name} bg="brand.500" color="white" />
          </HStack>
        </MenuButton>
        <MenuList>
          <MenuItem icon={<FiUser />} onClick={() => navigate("/profile")}>
            Profile
          </MenuItem>
          <MenuItem icon={<FiLogOut />} onClick={handleLogout} color="danger.500">
            Log out
          </MenuItem>
        </MenuList>
      </Menu>
    </Flex>
  );
}
