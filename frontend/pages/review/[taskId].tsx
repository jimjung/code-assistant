import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { useQuery } from 'react-query';
import {
  Box,
  VStack,
  Heading,
  Text,
  Progress,
  Alert,
  AlertIcon,
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
} from '@chakra-ui/react';
import { getReviewStatus } from '../../services/api';
import { CodeIssue } from '../../types';

export default function ReviewPage() {
  const router = useRouter();
  const { taskId } = router.query;
  const [pollInterval, setPollInterval] = useState(5000);

  const { data, error, isLoading } = useQuery(
    ['review', taskId],
    () => getReviewStatus(taskId as string),
    {
      enabled: !!taskId,
      refetchInterval: pollInterval,
      onSuccess: (data) => {
        if (data.status === 'completed') {
          setPollInterval(0);
        }
      },
    }
  );

  if (isLoading) {
    return (
      <Box p={8}>
        <VStack spacing={4}>
          <Heading size="md">Analyzing code...</Heading>
          <Progress
            size="lg"
            isIndeterminate
            width="100%"
            colorScheme="blue"
          />
        </VStack>
      </Box>
    );
  }

  if (error) {
    return (
      <Alert status="error">
        <AlertIcon />
        Error loading review: {error.message}
      </Alert>
    );
  }

  return (
    <Box p={8}>
      <VStack spacing={6} align="stretch">
        <Heading size="lg">Code Review Results</Heading>
        
        {data.status === 'processing' && (
          <Box>
            <Text mb={2}>Analysis in progress...</Text>
            <Progress
              value={data.completion_percentage}
              size="lg"
              colorScheme="blue"
            />
          </Box>
        )}

        {data.status === 'completed' && (
          <>
            <Box>
              <Heading size="md" mb={2}>Summary</Heading>
              <Text>{data.summary}</Text>
            </Box>

            <Box>
              <Heading size="md" mb={4}>Issues Found</Heading>
              <Accordion allowMultiple>
                {data.issues.map((issue: CodeIssue, index: number) => (
                  <AccordionItem key={index}>
                    <AccordionButton>
                      <Box flex="1" textAlign="left">
                        <Text fontWeight="bold">
                          {issue.file_path}:{issue.line_number}
                        </Text>
                        <Text color={getIssueColor(issue.risk_level)}>
                          {issue.issue_type} - {issue.risk_level} risk
                        </Text>
                      </Box>
                    </AccordionButton>
                    <AccordionPanel>
                      <VStack align="stretch" spacing={2}>
                        <Text><strong>Description:</strong> {issue.description}</Text>
                        <Text><strong>Suggestion:</strong> {issue.suggestion}</Text>
                      </VStack>
                    </AccordionPanel>
                  </AccordionItem>
                ))}
              </Accordion>
            </Box>
          </>
        )}
      </VStack>
    </Box>
  );
}

function getIssueColor(risk: string): string {
  switch (risk) {
    case 'high':
      return 'red.500';
    case 'medium':
      return 'orange.500';
    case 'low':
      return 'yellow.500';
    default:
      return 'gray.500';
  }
} 