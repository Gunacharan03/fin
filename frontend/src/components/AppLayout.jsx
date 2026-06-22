import { Box, Flex, Drawer, DrawerOverlay, DrawerContent, useDisclosure } from "@chakra-ui/react";
import Navbar from "./Navbar";
import Sidebar from "./Sidebar";
import Footer from "./Footer";

export default function AppLayout({ children }) {
  const { isOpen, onOpen, onClose } = useDisclosure();

  return (
    <Flex direction="column" minH="100vh">
      <Navbar onMenuClick={onOpen} />
      <Flex flex={1}>
        <Box
          as="nav"
          w="240px"
          borderRight="1px solid"
          borderColor="surface.200"
          display={{ base: "none", md: "block" }}
        >
          <Sidebar />
        </Box>

        <Drawer isOpen={isOpen} placement="left" onClose={onClose}>
          <DrawerOverlay />
          <DrawerContent maxW="240px">
            <Sidebar onNavigate={onClose} />
          </DrawerContent>
        </Drawer>

        <Box flex={1} p={{ base: 4, md: 6 }} bg="surface.50">
          {children}
        </Box>
      </Flex>
      <Footer />
    </Flex>
  );
}
