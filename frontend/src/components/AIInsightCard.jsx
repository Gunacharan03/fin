import { Box, Text, HStack, Icon, VStack } from "@chakra-ui/react";
import { FiZap } from "react-icons/fi";

export default function AIInsightCard({ title, content, icon = FiZap, accentColor = "brand.500" }) {
  return (
    <Box
      p={5}
      borderRadius="12px"
      bg="white"
      border="1px solid"
      borderColor="surface.200"
      borderLeftWidth="4px"
      borderLeftColor={accentColor}
    >
      <HStack spacing={2} mb={2}>
        <Icon as={icon} color={accentColor} />
        <Text fontWeight={700} fontFamily="heading" fontSize="sm" color={accentColor}>
          {title}
        </Text>
      </HStack>
      <VStack align="stretch" spacing={2}>
        <Text fontSize="sm" color="gray.700" whiteSpace="pre-line" lineHeight="1.7">
          {content}
        </Text>
      </VStack>
    </Box>
  );
}
