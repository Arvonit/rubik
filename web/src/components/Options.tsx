import { Button } from '@chakra-ui/button';
import { Input } from '@chakra-ui/input';
import { VStack } from '@chakra-ui/layout';
import { useState } from 'react';

interface Props {
  cube: string;
  setCube: (cube: string) => void;
  onSolve: () => void;
  isLoading: boolean;
}

function Options({ cube, setCube, onSolve, isLoading }: Props) {
  const [localCube, setLocalCube] = useState('');

  return (
    <VStack>
      <Input placeholder="54 char cube string" onChange={event => setCube(event.target.value)} />
      <Button isLoading={isLoading} loadingText="Solving" colorScheme="blue" onClick={onSolve}>
        Solve
      </Button>
    </VStack>
  );
}

export default Options;
