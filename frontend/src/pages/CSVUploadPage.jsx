import { useState, useRef } from "react";
import {
  VStack, Heading, Text, Box, Button, Input, Table, Thead, Tbody, Tr, Th, Td,
  Badge, Alert, AlertIcon, HStack, useToast, TableContainer,
} from "@chakra-ui/react";
import { FiUploadCloud } from "react-icons/fi";
import { csvService } from "../services/csvService";

export default function CSVUploadPage() {
  const toast = useToast();
  const fileInputRef = useRef();
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [importing, setImporting] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setPreview(null);
    setError("");
  };

  const handlePreview = async () => {
    if (!file) return;
    setError("");
    setLoading(true);
    try {
      const result = await csvService.preview(file);
      setPreview(result);
    } catch (err) {
      setError(err.response?.data?.detail || "Could not parse this file.");
    } finally {
      setLoading(false);
    }
  };

  const handleConfirmImport = async () => {
    setImporting(true);
    try {
      const result = await csvService.confirm(file);
      toast({ title: result.message, status: "success", duration: 3000 });
      setFile(null);
      setPreview(null);
      if (fileInputRef.current) fileInputRef.current.value = "";
    } catch (err) {
      setError(err.response?.data?.detail || "Import failed.");
    } finally {
      setImporting(false);
    }
  };

  return (
    <VStack align="stretch" spacing={6}>
      <Box>
        <Heading size="lg" fontFamily="heading" mb={1}>Import Bank Statement</Heading>
        <Text color="gray.500" fontSize="sm">
          Upload a CSV or Excel file from your bank. We'll auto-detect columns and categorize transactions for you.
        </Text>
      </Box>

      <Box bg="white" p={6} borderRadius="12px" border="1px solid" borderColor="surface.200">
        <VStack align="stretch" spacing={4}>
          <Input ref={fileInputRef} type="file" accept=".csv,.xlsx,.xls" onChange={handleFileChange} p={1.5} />

          {error && (
            <Alert status="error" borderRadius="8px" fontSize="sm">
              <AlertIcon />
              {error}
            </Alert>
          )}

          <HStack>
            <Button leftIcon={<FiUploadCloud />} colorScheme="blue" onClick={handlePreview} isLoading={loading} isDisabled={!file}>
              Preview transactions
            </Button>
            {preview && (
              <Button colorScheme="yellow" onClick={handleConfirmImport} isLoading={importing}>
                Confirm & import {preview.preview_count} transactions
              </Button>
            )}
          </HStack>
        </VStack>
      </Box>

      {preview && (
        <Box bg="white" p={4} borderRadius="12px" border="1px solid" borderColor="surface.200">
          <Heading size="sm" mb={3} fontFamily="heading">Preview ({preview.preview_count} found)</Heading>
          <TableContainer maxH="420px" overflowY="auto">
            <Table size="sm">
              <Thead>
                <Tr>
                  <Th>Date</Th>
                  <Th>Description</Th>
                  <Th>Category</Th>
                  <Th>Type</Th>
                  <Th isNumeric>Amount</Th>
                </Tr>
              </Thead>
              <Tbody>
                {preview.transactions.map((t, i) => (
                  <Tr key={i}>
                    <Td>{new Date(t.date).toLocaleDateString()}</Td>
                    <Td maxW="220px" isTruncated>{t.description}</Td>
                    <Td><Badge fontSize="2xs">{t.category}</Badge></Td>
                    <Td>
                      <Badge colorScheme={t.type === "income" ? "yellow" : "gray"} fontSize="2xs">
                        {t.type}
                      </Badge>
                    </Td>
                    <Td isNumeric>{t.amount.toLocaleString()}</Td>
                  </Tr>
                ))}
              </Tbody>
            </Table>
          </TableContainer>
        </Box>
      )}
    </VStack>
  );
}
