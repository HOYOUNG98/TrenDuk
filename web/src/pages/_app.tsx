// library import
import { ChakraProvider, ColorModeProvider } from "@chakra-ui/react";
import { Provider } from "react-redux";

// local import
import theme from "../theme";
import { store } from "../store";
import "react-vis/dist/style.css";

function MyApp({ Component, pageProps }: any) {
  return (
    <Provider store={store}>
      <ChakraProvider resetCSS theme={theme}>
        <ColorModeProvider
          options={{
            useSystemColorMode: true,
          }}
        >
          <Component {...pageProps} />
        </ColorModeProvider>
      </ChakraProvider>
    </Provider>
  );
}

export default MyApp;
