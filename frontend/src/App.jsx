import { BrowserRouter, Routes, Route } from "react-router-dom";

import Reconciliation from "./pages/Reconciliation";
import Analytics from "./pages/Analytics";
import Narrative from "./pages/Narrative";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Reconciliation />} />
      <Route path="/analytics" element={<Analytics />} />
      <Route path="/narrative" element={<Narrative />} />
    </Routes>
  );
}