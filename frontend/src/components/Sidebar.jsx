import { VStack, Box, Text, Icon } from "@chakra-ui/react";
import { NavLink } from "react-router-dom";
import {
  FiHome, FiList, FiPlusCircle, FiTarget, FiBell,
  FiBarChart2, FiUpload, FiZap, FiMessageCircle, FiUser,
} from "react-icons/fi";

const navItems = [
  { label: "Dashboard", icon: FiHome, to: "/dashboard" },
  { label: "Transactions", icon: FiList, to: "/transactions" },
  { label: "Add Transaction", icon: FiPlusCircle, to: "/transactions/add" },
  { label: "Goals", icon: FiTarget, to: "/goals" },
  { label: "Reminders", icon: FiBell, to: "/reminders" },
  { label: "Analytics", icon: FiBarChart2, to: "/analytics" },
  { label: "Import CSV", icon: FiUpload, to: "/csv-upload" },
  { label: "AI Insights", icon: FiZap, to: "/ai-insights" },
  { label: "Advisor Chat", icon: FiMessageCircle, to: "/chatbot" },
  { label: "Profile", icon: FiUser, to: "/profile" },
];

export default function Sidebar({ onNavigate }) {
  return (
    <VStack align="stretch" spacing={1} p={3} h="100%" bg="white">
      {navItems.map((item) => (
        <Box
          as={NavLink}
          key={item.to}
          to={item.to}
          onClick={onNavigate}
          display="flex"
          alignItems="center"
          gap={3}
          px={3}
          py={2.5}
          borderRadius="8px"
          fontSize="sm"
          fontWeight={500}
          color="gray.600"
          _hover={{ bg: "surface.100", color: "brand.500" }}
          sx={{
            "&.active": {
              bg: "brand.50",
              color: "brand.500",
              fontWeight: 600,
            },
          }}
        >
          <Icon as={item.icon} boxSize={4.5} />
          <Text>{item.label}</Text>
        </Box>
      ))}
    </VStack>
  );
}
