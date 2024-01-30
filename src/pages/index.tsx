import Head from 'next/head';
import Image from 'next/image';
import { Alert, AlertIcon } from '@chakra-ui/alert';
import { Container, VStack } from '@chakra-ui/layout';
import { useState } from 'react';
import Cube from '../components/Cube';
import Header from '../components/Header';
import Options from '../components/Options';
import Results from '../components/Results';

export default function Home() {
  const DEFAULT_CUBE = 'RRRRRRRRRBBBBBBBBBWWWWWWWWWGGGGGGGGGYYYYYYYYYOOOOOOOOO';

  // State variables

  const [cube, setCube] = useState(DEFAULT_CUBE);
  const [selectedColor, setSelectedColor] = useState('');
  const [showAlert, toggleAlert] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
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

    // fetch(`https://arvonit-rubik.herokuapp.com/?cube=${cube}`)
    fetch(`/api/solve?cube=${cube}`)
      .then((response) => response.json())
      .then((response) => {
        console.log(response);
        if (response.error !== undefined) {
          setAlertText(response.error);
          toggleAlert(true);
          return;
        }

        setMoves(response.moves);
        setTimeToSolve(response.timeToSolve);
        setOriginalCube(cube);
        setCube(response.cube);
      })
      .catch((error) => {
        setAlertText('Unable to connect to the server.');
        toggleAlert(true);
        console.log(error);
      })
      .finally(() => {
        setIsLoading(false);
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
    <>
      <Head>
        <title>Rubik&apos;s Cube Solver</title>
        <meta name="description" content="Rubik's cube solver" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
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

          {/* Show the results only if we do not get an error from the server */}
          {!showAlert && (
            <Results originalCube={originalCube} moves={moves} timeToSolve={timeToSolve} />
          )}

          <Options cube={cube} setCube={validateCube} onSolve={onSolve} isLoading={isLoading} />
        </VStack>
      </Container>
    </>
  );
}
