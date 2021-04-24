import { Box } from '@chakra-ui/layout';

interface Props {
  color: string;
  updateColor: (index: number) => void;
  cubeColorIndex: number;
}

function Piece({ color, updateColor, cubeColorIndex }: Props) {
  return (
    <Box
      backgroundColor={color}
      border="2px"
      borderColor="blackAlpha.200"
      height="50px"
      width="50px"
      onClick={event => updateColor(cubeColorIndex)}
    />
  );
}

export default Piece;
