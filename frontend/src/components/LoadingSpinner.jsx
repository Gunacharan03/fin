import { Center, Spinner, Text, VStack } from "@chakra-ui/react";

export default function LoadingSpinner({ label = "Loading..." }) {
  return (
    <Center py={10}>
      <VStack spacing={3}>
        <Spinner size="lg" color="brand.500" thickness="3px" />
        <Text fontSize="sm" color="gray.500">{label}</Text>
      </VStack>
    </Center>
  );
}
