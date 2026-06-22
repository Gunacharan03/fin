import { Flex, Box, Text, Badge, Button, HStack } from "@chakra-ui/react";
import { FiCheck } from "react-icons/fi";

export default function ReminderCard({ reminder, currency = "₹", onMarkPaid, onDelete }) {
  const statusColors = { pending: "blue", paid: "green", overdue: "red" };

  return (
    <Flex
      align="center"
      justify="space-between"
      p={4}
      borderRadius="10px"
      border="1px solid"
      borderColor={reminder.status === "overdue" ? "danger.400" : "surface.200"}
      bg="white"
    >
      <Box>
        <HStack spacing={2} mb={1}>
          <Text fontWeight={600} fontSize="sm">{reminder.title}</Text>
          <Badge colorScheme={statusColors[reminder.status]} fontSize="2xs">{reminder.status}</Badge>
        </HStack>
        <Text fontSize="xs" color="gray.500">
          Due {new Date(reminder.due_date).toLocaleDateString()} · {reminder.frequency} · {reminder.category}
        </Text>
      </Box>

      <HStack spacing={3}>
        <Text fontWeight={700} fontFamily="heading">{currency}{reminder.amount.toLocaleString()}</Text>
        {reminder.status !== "paid" && onMarkPaid && (
          <Button size="sm" leftIcon={<FiCheck />} colorScheme="blue" variant="outline" onClick={() => onMarkPaid(reminder.id)}>
            Mark paid
          </Button>
        )}
      </HStack>
    </Flex>
  );
}
