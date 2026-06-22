import { useEffect, useState } from "react";
import {
  VStack, HStack, Heading, Select, Button, Box, Text, Input,
  Modal, ModalOverlay, ModalContent, ModalHeader, ModalBody, ModalFooter, ModalCloseButton,
  FormControl, FormLabel, useDisclosure, useToast,
} from "@chakra-ui/react";
import { Link } from "react-router-dom";
import { FiPlus } from "react-icons/fi";
import { transactionService } from "../services/transactionService";
import { useAuth } from "../context/AuthContext";
import TransactionCard from "../components/TransactionCard";
import LoadingSpinner from "../components/LoadingSpinner";

const CURRENCY_SYMBOLS = { INR: "₹", USD: "$", EUR: "€", GBP: "£" };

export default function TransactionsPage() {
  const { user } = useAuth();
  const toast = useToast();
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [typeFilter, setTypeFilter] = useState("");
  const [editing, setEditing] = useState(null);
  const currency = CURRENCY_SYMBOLS[user?.currency] || "₹";

  const load = async () => {
    setLoading(true);
    try {
      const filters = typeFilter ? { type: typeFilter } : {};
      const res = await transactionService.list(filters);
      setTransactions(res.items);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, [typeFilter]);

  const handleDelete = async (id) => {
    await transactionService.remove(id);
    toast({ title: "Transaction deleted", status: "success", duration: 2000 });
    load();
  };

  const handleEdit = (txn) => {
    setEditing({ ...txn, date: txn.date.slice(0, 10) });
    onOpen();
  };

  const handleUpdateSubmit = async () => {
    await transactionService.update(editing.id, {
      amount: parseFloat(editing.amount),
      category: editing.category,
      description: editing.description,
      date: editing.date,
    });
    toast({ title: "Transaction updated", status: "success", duration: 2000 });
    onClose();
    load();
  };

  return (
    <VStack align="stretch" spacing={5}>
      <HStack justify="space-between">
        <Heading size="lg" fontFamily="heading">Transactions</Heading>
        <Button as={Link} to="/transactions/add" leftIcon={<FiPlus />} colorScheme="blue">
          Add Transaction
        </Button>
      </HStack>

      <HStack>
        <Select w="200px" placeholder="All types" value={typeFilter} onChange={(e) => setTypeFilter(e.target.value)}>
          <option value="income">Income</option>
          <option value="expense">Expense</option>
        </Select>
      </HStack>

      {loading ? (
        <LoadingSpinner />
      ) : transactions.length === 0 ? (
        <Box bg="white" py={10} borderRadius="12px" border="1px solid" borderColor="surface.200" textAlign="center">
          <Text color="gray.500">No transactions found. Add one to get started.</Text>
        </Box>
      ) : (
        <VStack align="stretch" spacing={2}>
          {transactions.map((t) => (
            <TransactionCard key={t.id} transaction={t} currency={currency} onEdit={handleEdit} onDelete={handleDelete} />
          ))}
        </VStack>
      )}

      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Edit Transaction</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            {editing && (
              <VStack spacing={3}>
                <FormControl>
                  <FormLabel fontSize="sm">Amount</FormLabel>
                  <Input type="number" value={editing.amount} onChange={(e) => setEditing({ ...editing, amount: e.target.value })} />
                </FormControl>
                <FormControl>
                  <FormLabel fontSize="sm">Category</FormLabel>
                  <Input value={editing.category} onChange={(e) => setEditing({ ...editing, category: e.target.value })} />
                </FormControl>
                <FormControl>
                  <FormLabel fontSize="sm">Description</FormLabel>
                  <Input value={editing.description} onChange={(e) => setEditing({ ...editing, description: e.target.value })} />
                </FormControl>
                <FormControl>
                  <FormLabel fontSize="sm">Date</FormLabel>
                  <Input type="date" value={editing.date} onChange={(e) => setEditing({ ...editing, date: e.target.value })} />
                </FormControl>
              </VStack>
            )}
          </ModalBody>
          <ModalFooter>
            <Button variant="ghost" mr={3} onClick={onClose}>Cancel</Button>
            <Button colorScheme="blue" onClick={handleUpdateSubmit}>Save changes</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </VStack>
  );
}
