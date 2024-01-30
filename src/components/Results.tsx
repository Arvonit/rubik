import { Text, VStack } from '@chakra-ui/layout';

interface Props {
  originalCube: string;
  moves: Array<string>;
  timeToSolve: number;
}

function Results({ originalCube, moves, timeToSolve }: Props) {
  if (moves.length === 0 && originalCube !== '') {
    return <Text>The cube is already solved!</Text>;
  } else if (timeToSolve === 0) {
    return <></>;
  }

  let movesString = '';
  for (let i = 0; i < moves.length; i++) {
    if (i === moves.length - 1) {
      movesString += moves[i];
    } else {
      movesString += `${moves[i]}, `;
    }
  }

  return (
    <VStack>
      <Text>Original Cube: {originalCube}</Text>
      <Text>
        The solution requires {moves.length} moves and took {timeToSolve} seconds.
      </Text>
      <Text>Moves: {movesString}</Text>
    </VStack>
  );
}

export default Results;
