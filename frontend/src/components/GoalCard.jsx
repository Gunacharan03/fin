import { Box, Text, Progress, HStack, Badge, Button, VStack } from "@chakra-ui/react";

export default function GoalCard({ goal, currency = "₹", onContribute, onDelete }) {
  const statusColors = { active: "blue", completed: "yellow", abandoned: "gray" };

  return (
    <Box p={5} borderRadius="12px" border="1px solid" borderColor="surface.200" bg="white">
      <HStack justify="space-between" mb={2}>
        <Text fontWeight={700} fontFamily="heading" fontSize="md">{goal.title}</Text>
        <Badge colorScheme={statusColors[goal.status]} borderRadius="full" px={2}>
          {goal.status}
        </Badge>
      </HStack>

      <Text fontSize="sm" color="gray.600" mb={3}>
        {currency}{goal.current_amount.toLocaleString()} of {currency}{goal.target_amount.toLocaleString()}
      </Text>

      <Progress
        value={goal.progress_percent}
        size="sm"
        borderRadius="full"
        colorScheme={goal.progress_percent >= 100 ? "yellow" : "blue"}
        mb={3}
      />

      <HStack justify="space-between">
        <Text fontSize="xs" color="gray.500">{goal.progress_percent}% complete</Text>
        {goal.target_date && (
          <Text fontSize="xs" color="gray.500">
            Target: {new Date(goal.target_date).toLocaleDateString()}
          </Text>
        )}
      </HStack>

      {goal.status === "active" && (onContribute || onDelete) && (
        <HStack mt={4} spacing={2}>
          {onContribute && (
            <Button size="sm" variant="outline" colorScheme="blue" onClick={() => onContribute(goal)}>
              Add funds
            </Button>
          )}
          {onDelete && (
            <Button size="sm" variant="ghost" color="danger.500" onClick={() => onDelete(goal.id)}>
              Delete
            </Button>
          )}
        </HStack>
      )}
    </Box>
  );
}
