import { Flex, Box, Text, Badge, IconButton, HStack } from "@chakra-ui/react";
import { FiTrash2, FiEdit2, FiArrowUpRight, FiArrowDownRight } from "react-icons/fi";

export default function TransactionCard({ transaction, currency = "₹", onEdit, onDelete }) {
  const isIncome = transaction.type === "income";

  return (
    <Flex
      align="center"
      justify="space-between"
      p={3.5}
      borderRadius="10px"
      border="1px solid"
      borderColor="surface.200"
      bg="white"
      _hover={{ borderColor: "brand.100" }}
    >
      <HStack spacing={3}>
        <Box
          p={2}
          borderRadius="full"
          bg={isIncome ? "positive.50" : "danger.50"}
          color={isIncome ? "positive.600" : "danger.500"}
        >
          {isIncome ? <FiArrowUpRight /> : <FiArrowDownRight />}
        </Box>
        <Box>
          <Text fontWeight={600} fontSize="sm">
            {transaction.description || transaction.category}
          </Text>
          <HStack spacing={2} mt={0.5}>
            <Badge size="sm" colorScheme={isIncome ? "yellow" : "gray"} fontSize="2xs">
              {transaction.category}
            </Badge>
            <Text fontSize="xs" color="gray.500">
              {new Date(transaction.date).toLocaleDateString()}
            </Text>
          </HStack>
        </Box>
      </HStack>

      <HStack spacing={2}>
        <Text fontWeight={700} color={isIncome ? "positive.600" : "danger.500"} fontFamily="heading">
          {isIncome ? "+" : "-"}{currency}{transaction.amount.toLocaleString()}
        </Text>
        {onEdit && (
          <IconButton aria-label="Edit" icon={<FiEdit2 />} size="sm" variant="ghost" onClick={() => onEdit(transaction)} />
        )}
        {onDelete && (
          <IconButton
            aria-label="Delete"
            icon={<FiTrash2 />}
            size="sm"
            variant="ghost"
            color="danger.500"
            onClick={() => onDelete(transaction.id)}
          />
        )}
      </HStack>
    </Flex>
  );
}
