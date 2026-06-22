import { Box, Text } from "@chakra-ui/react";

export default function Footer() {
  return (
    <Box as="footer" py={4} textAlign="center" borderTop="1px solid" borderColor="surface.200">
      <Text fontSize="xs" color="gray.500">
        Fin — For Every Income, A Smarter Outcome
      </Text>
    </Box>
  );
}
