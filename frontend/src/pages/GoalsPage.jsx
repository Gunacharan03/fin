import { useEffect, useState } from "react";
import {
  VStack, HStack, Heading, Button, SimpleGrid, Box, Text,
  Modal, ModalOverlay, ModalContent, ModalHeader, ModalBody, ModalFooter, ModalCloseButton,
  FormControl, FormLabel, Input, useDisclosure, useToast,
} from "@chakra-ui/react";
import { Link } from "react-router-dom";
import { FiPlus } from "react-icons/fi";
import { goalService } from "../services/goalService";
import { useAuth } from "../context/AuthContext";
import GoalCard from "../components/GoalCard";
import LoadingSpinner from "../components/LoadingSpinner";

const CURRENCY_SYMBOLS = { INR: "₹", USD: "$", EUR: "€", GBP: "£" };

export default function GoalsPage() {
  const { user } = useAuth();
  const toast = useToast();
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [goals, setGoals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeGoal, setActiveGoal] = useState(null);
  const [contributionAmount, setContributionAmount] = useState("");
  const currency = CURRENCY_SYMBOLS[user?.currency] || "₹";

  const load = async () => {
    setLoading(true);
    try {
      const res = await goalService.list();
      setGoals(res.items);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const handleContributeClick = (goal) => {
    setActiveGoal(goal);
    setContributionAmount("");
    onOpen();
  };

  const handleContributeSubmit = async () => {
    if (!contributionAmount || parseFloat(contributionAmount) <= 0) return;
    await goalService.contribute(activeGoal.id, parseFloat(contributionAmount));
    toast({ title: "Funds added to goal", status: "success", duration: 2000 });
    onClose();
    load();
  };

  const handleDelete = async (id) => {
    await goalService.remove(id);
    toast({ title: "Goal deleted", status: "success", duration: 2000 });
    load();
  };

  return (
    <VStack align="stretch" spacing={5}>
      <HStack justify="space-between">
        <Heading size="lg" fontFamily="heading">Savings Goals</Heading>
        <Button as={Link} to="/goals/add" leftIcon={<FiPlus />} colorScheme="blue">
          New Goal
        </Button>
      </HStack>

      {loading ? (
        <LoadingSpinner />
      ) : goals.length === 0 ? (
        <Box bg="white" py={10} borderRadius="12px" border="1px solid" borderColor="surface.200" textAlign="center">
          <Text color="gray.500">No goals yet. Create one to start tracking progress.</Text>
        </Box>
      ) : (
        <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={4}>
          {goals.map((g) => (
            <GoalCard key={g.id} goal={g} currency={currency} onContribute={handleContributeClick} onDelete={handleDelete} />
          ))}
        </SimpleGrid>
      )}

      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Add funds to "{activeGoal?.title}"</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <FormControl>
              <FormLabel fontSize="sm">Amount to add</FormLabel>
              <Input type="number" value={contributionAmount} onChange={(e) => setContributionAmount(e.target.value)} placeholder="0.00" />
            </FormControl>
          </ModalBody>
          <ModalFooter>
            <Button variant="ghost" mr={3} onClick={onClose}>Cancel</Button>
            <Button colorScheme="blue" onClick={handleContributeSubmit}>Add funds</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </VStack>
  );
}
