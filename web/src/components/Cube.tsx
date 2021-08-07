import { Button } from '@chakra-ui/button';
import { Box, HStack, SimpleGrid, VStack } from '@chakra-ui/layout';
import { useState } from 'react';
import Piece from './Piece';

interface Props {
  cube: string;
  setCube: (cube: string) => void;
  selectedColor: string;
  setSelectedColor: (color: string) => void;
}

function Cube({ cube, setCube, selectedColor, setSelectedColor }: Props) {
  // Maintain state of the background color of the color chooser
  // We want the background of the chooser to reflect the color selected (or not selected).
  const [backgroundColor, setBackgroundColor] = useState('');

  enum Color {
    WHITE = 'gray.100',
    BLUE = 'blue.400',
    RED = 'red.500',
    ORANGE = 'orange.300',
    GREEN = 'green.400',
    YELLOW = 'yellow.300'
  }

  function changeSelectedColor(color: string) {
    console.log(color);

    if (color === selectedColor) {
      setBackgroundColor('white');
      setSelectedColor('');
      return;
    }

    setSelectedColor(color);
    switch (color) {
      case 'W':
        setBackgroundColor(Color.WHITE);
        break;
      case 'B':
        setBackgroundColor(Color.BLUE);
        break;
      case 'R':
        setBackgroundColor(Color.RED);
        break;
      case 'O':
        setBackgroundColor(Color.ORANGE);
        break;
      case 'G':
        setBackgroundColor(Color.GREEN);
        break;
      case 'Y':
        setBackgroundColor(Color.YELLOW);
        break;
    }
  }

  function cubeColorToBackgroundColor(color: string): string {
    switch (color) {
      case 'W':
        return Color.WHITE;
      case 'B':
        return Color.BLUE;
      case 'R':
        return Color.RED;
      case 'O':
        return Color.ORANGE;
      case 'G':
        return Color.GREEN;
      case 'Y':
        return Color.YELLOW;
      default:
        return 'white';
    }
  }

  function updateColor(index: number) {
    if (selectedColor === '') {
      return;
    }

    const newCube = cube.substring(0, index) + selectedColor + cube.substring(index + 1);
    setCube(newCube);
  }

  function createPieceFromIndex(index: number) {
    return (
      <Piece
        color={cubeColorToBackgroundColor(cube[index])}
        updateColor={updateColor}
        cubeColorIndex={index}
      />
    );
  }

  function createFaceFromIndex(index: number) {
    return (
      <SimpleGrid columns={3} spacing="0px">
        {createPieceFromIndex(index)}
        {createPieceFromIndex(index + 1)}
        {createPieceFromIndex(index + 2)}
        {createPieceFromIndex(index + 3)}
        {createPieceFromIndex(index + 4)}
        {createPieceFromIndex(index + 5)}
        {createPieceFromIndex(index + 6)}
        {createPieceFromIndex(index + 7)}
        {createPieceFromIndex(index + 8)}
      </SimpleGrid>
    );
  }

  return (
    <VStack>
      {/* Cube map */}
      <VStack spacing={0}>
        <div style={{ position: 'relative', left: '-75px' }}>{createFaceFromIndex(0)}</div>
        <HStack spacing={0}>
          {createFaceFromIndex(9)}
          {createFaceFromIndex(18)}
          {createFaceFromIndex(27)}
          {createFaceFromIndex(36)}
        </HStack>
        <div style={{ position: 'relative', left: '-75px' }}>{createFaceFromIndex(45)}</div>
      </VStack>

      {/* Color chooser */}
      <Box backgroundColor={backgroundColor} padding={4}>
        <Button onClick={event => changeSelectedColor('W')} />
        <Button colorScheme="blue" onClick={event => changeSelectedColor('B')} />
        <Button colorScheme="red" onClick={event => changeSelectedColor('R')} />
        <Button colorScheme="orange" onClick={event => changeSelectedColor('O')} />
        <Button colorScheme="green" onClick={event => changeSelectedColor('G')} />
        <Button colorScheme="yellow" onClick={event => changeSelectedColor('Y')} />
      </Box>
    </VStack>
  );
}

export default Cube;
