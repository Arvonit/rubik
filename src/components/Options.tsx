import { Button } from '@chakra-ui/button';
import { Input } from '@chakra-ui/input';

interface Props {
  cube: string;
  setCube: (cube: string) => void;
  onSolve: () => void;
  isLoading: boolean;
}

function Options({ cube, setCube, onSolve, isLoading }: Props) {
  return (
    <>
      <Input
        placeholder="54-Character Cube String"
        onChange={(event) => setCube(event.target.value)}
      />
      <Button isLoading={isLoading} loadingText="Solving" colorScheme="blue" onClick={onSolve}>
        Solve
      </Button>
    </>
  );
}

export default Options;
