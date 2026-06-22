/**
 * Custom Chakra theme.
 *
 * Design intent: this is a money-management tool people check daily, often
 * quickly, often on mobile. The signature move is a deep "ledger ink" navy
 * paired with a warm signal-amber used ONLY for money-positive states
 * (savings, goals met) and a clear coral/red reserved for overdue/overspend —
 * so color itself carries financial meaning instead of decorating randomly.
 *
 * Type: Lexend for numbers/headings (slightly rounded, very legible at small
 * sizes — good for amounts), Inter for body text/UI labels.
 */
import { extendTheme } from "@chakra-ui/react";

const colors = {
  brand: {
    50: "#EEF2FB",
    100: "#D3DCF2",
    400: "#3A5BA0",
    500: "#1F3A6B", // ledger ink navy — primary
    600: "#15294E",
    900: "#0B1830",
  },
  positive: {
    400: "#E0A726",
    500: "#C2891A", // signal amber — savings, growth, goals met
    600: "#9A6B12",
  },
  danger: {
    400: "#E5685B",
    500: "#D14B3D", // coral-red — overdue, overspend only
    600: "#A93429",
  },
  surface: {
    50: "#FAFAF8",
    100: "#F3F2EE",
    200: "#E8E6DF",
  },
};

const fonts = {
  heading: `'Lexend', sans-serif`,
  body: `'Inter', sans-serif`,
};

const components = {
  Button: {
    baseStyle: { fontWeight: 600, borderRadius: "8px" },
    variants: {
      solid: { bg: "brand.500", color: "white", _hover: { bg: "brand.600" } },
    },
  },
  Card: {
    baseStyle: {
      container: {
        borderRadius: "12px",
        boxShadow: "0 1px 2px rgba(11,24,48,0.06), 0 1px 1px rgba(11,24,48,0.04)",
        border: "1px solid",
        borderColor: "surface.200",
      },
    },
  },
};

const theme = extendTheme({
  colors,
  fonts,
  components,
  styles: {
    global: {
      body: { bg: "surface.50", color: "brand.900" },
    },
  },
});

export default theme;
