import { useEffect, useState } from "react";
import {
  VStack, HStack, Heading, Button, Box, Text,
  Modal, ModalOverlay, ModalContent, ModalHeader, ModalBody, ModalFooter, ModalCloseButton,
  FormControl, FormLabel, Input, Select, useDisclosure, useToast,
} from "@chakra-ui/react";
import { FiPlus } from "react-icons/fi";
import { reminderService } from "../services/reminderService";
import { useAuth } from "../context/AuthContext";
import ReminderCard from "../components/ReminderCard";
import LoadingSpinner from "../components/LoadingSpinner";

const CURRENCY_SYMBOLS = { INR: "₹", USD: "$", EUR: "€", GBP: "£" };

export default function RemindersPage() {
  const { user } = useAuth();
  const toast = useToast();
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [reminders, setReminders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState({
    title: "", amount: "", due_date: "", frequency: "once", category: "EMI", notes: "",
  });
  const currency = CURRENCY_SYMBOLS[user?.currency] || "₹";

  const load = async () => {
    setLoading(true);
    try {
      const res = await reminderService.list();
      setReminders(res.items);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const handleMarkPaid = async (id) => {
    await reminderService.markPaid(id);
    toast({ title: "Marked as paid", status: "success", duration: 2000 });
    load();
  };

  const handleCreate = async () => {
    if (!form.title || !form.amount || !form.due_date) {
      toast({ title: "Please fill all required fields", status: "warning", duration: 2000 });
      return;
    }
    await reminderService.create({ ...form, amount: parseFloat(form.amount) });
    toast({ title: "Reminder created", status: "success", duration: 2000 });
    setForm({ title: "", amount: "", due_date: "", frequency: "once", category: "EMI", notes: "" });
    onClose();
    load();
  };

  const overdue = reminders.filter((r) => r.status === "overdue");
  const pending = reminders.filter((r) => r.status === "pending");
  const paid = reminders.filter((r) => r.status === "paid");

  return (
    <VStack align="stretch" spacing={6}>
      <HStack justify="space-between">
        <Heading size="lg" fontFamily="heading">Reminders & EMIs</Heading>
        <Button leftIcon={<FiPlus />} colorScheme="blue" onClick={onOpen}>
          New Reminder
        </Button>
      </HStack>

      {loading ? (
        <LoadingSpinner />
      ) : reminders.length === 0 ? (
        <Box bg="white" py={10} borderRadius="12px" border="1px solid" borderColor="surface.200" textAlign="center">
          <Text color="gray.500">No reminders set. Add one for your next EMI or bill.</Text>
        </Box>
      ) : (
        <>
          {overdue.length > 0 && (
            <Box>
              <Heading size="sm" color="danger.500" mb={2}>Overdue ({overdue.length})</Heading>
              <VStack align="stretch" spacing={2}>
                {overdue.map((r) => <ReminderCard key={r.id} reminder={r} currency={currency} onMarkPaid={handleMarkPaid} />)}
              </VStack>
            </Box>
          )}
          {pending.length > 0 && (
            <Box>
              <Heading size="sm" color="brand.500" mb={2}>Upcoming ({pending.length})</Heading>
              <VStack align="stretch" spacing={2}>
                {pending.map((r) => <ReminderCard key={r.id} reminder={r} currency={currency} onMarkPaid={handleMarkPaid} />)}
              </VStack>
            </Box>
          )}
          {paid.length > 0 && (
            <Box>
              <Heading size="sm" color="gray.500" mb={2}>Paid ({paid.length})</Heading>
              <VStack align="stretch" spacing={2}>
                {paid.map((r) => <ReminderCard key={r.id} reminder={r} currency={currency} />)}
              </VStack>
            </Box>
          )}
        </>
      )}

      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>New Reminder</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <VStack spacing={3}>
              <FormControl isRequired>
                <FormLabel fontSize="sm">Title</FormLabel>
                <Input value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} placeholder="e.g. Car Loan EMI" />
              </FormControl>
              <FormControl isRequired>
                <FormLabel fontSize="sm">Amount</FormLabel>
                <Input type="number" value={form.amount} onChange={(e) => setForm({ ...form, amount: e.target.value })} placeholder="0.00" />
              </FormControl>
              <FormControl isRequired>
                <FormLabel fontSize="sm">Due date</FormLabel>
                <Input type="date" value={form.due_date} onChange={(e) => setForm({ ...form, due_date: e.target.value })} />
              </FormControl>
              <FormControl>
                <FormLabel fontSize="sm">Frequency</FormLabel>
                <Select value={form.frequency} onChange={(e) => setForm({ ...form, frequency: e.target.value })}>
                  <option value="once">Once</option>
                  <option value="weekly">Weekly</option>
                  <option value="monthly">Monthly</option>
                  <option value="yearly">Yearly</option>
                </Select>
              </FormControl>
              <FormControl>
                <FormLabel fontSize="sm">Category</FormLabel>
                <Input value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })} placeholder="EMI" />
              </FormControl>
            </VStack>
          </ModalBody>
          <ModalFooter>
            <Button variant="ghost" mr={3} onClick={onClose}>Cancel</Button>
            <Button colorScheme="blue" onClick={handleCreate}>Create reminder</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </VStack>
  );
}
