import { Alert, AlertIcon } from '@chakra-ui/alert';
import { Container, VStack } from '@chakra-ui/layout';
import { useState } from 'react';
import Cube from './components/Cube';
import Header from './components/Header';
import Options from './components/Options';
import Results from './components/Results';

function App() {
  const DEFAULT_CUBE = 'RRRRRRRRRBBBBBBBBBWWWWWWWWWGGGGGGGGGYYYYYYYYYOOOOOOOOO';
  const [cube, setCube] = useState(DEFAULT_CUBE);
  const [selectedColor, setSelectedColor] = useState('');
  const [showAlert, toggleAlert] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  // const [showSuccess, toggleSuccess] = useState(false);
  const [alertText, setAlertText] = useState('');
  const [originalCube, setOriginalCube] = useState('');
  const [moves, setMoves] = useState([]);
  const [timeToSolve, setTimeToSolve] = useState(0);

  function onSolve() {
    if (showAlert) {
      return;
    }

    setIsLoading(true);
    toggleAlert(false);

    fetch(`http://localhost:8000/?cube=${cube}`)
      .then(response => response.json())
      .then(response => {
        console.log(response);
        setIsLoading(false);
        if (response.error !== undefined) {
          setAlertText(response.error);
          toggleAlert(true);
          return;
        }

        // setMoves(`Original Cube: ${cube}\n` + response.moves.toString());
        setMoves(response.moves);
        setTimeToSolve(response.timeToSolve);
        setOriginalCube(cube);
        setCube(response.cube);
      })
      .catch(error => {
        setIsLoading(false);
        setAlertText('Unable to connect to the server.');
        toggleAlert(true);
        console.log(error);
      });
  }

  function validateCube(cubeString: string) {
    const cubeChars = new Set(['W', 'B', 'R', 'G', 'Y', 'O']);

    if (cubeString.length === 0) {
      cubeString = DEFAULT_CUBE;
    }

    if (cubeString.length > 0 && cubeString.length !== 54) {
      setAlertText('Cube string must be 54 characters long.');
      toggleAlert(true);
      return;
    }

    for (let i = 0; i < cubeString.length; i++) {
      const char = cubeString.charAt(i);

      if (!cubeChars.has(char)) {
        setAlertText(
          'The cube string argument contains invalid characters ' +
            `(i.e. something other than 'W', 'B', 'R', 'G', 'Y', 'O').`
        );
        toggleAlert(true);
        return;
      }
    }

    toggleAlert(false);
    setCube(cubeString);
  }

  return (
    <Container maxWidth="5xl" centerContent>
      <VStack>
        <Header />
        {showAlert && (
          <Alert status="error">
            <AlertIcon />
            {alertText}
          </Alert>
        )}
        <Cube
          cube={cube}
          setCube={validateCube}
          selectedColor={selectedColor}
          setSelectedColor={setSelectedColor}
        />
        {!showAlert && (
          <Results originalCube={originalCube} moves={moves} timeToSolve={timeToSolve} />
        )}
        <Options cube={cube} setCube={validateCube} onSolve={onSolve} isLoading={isLoading} />
      </VStack>
    </Container>
  );
}

export default App;
