import { useEffect, useState } from "react";

import DashboardLayout from "../layouts/DashboardLayout";
import Header from "../components/layout/Header";
import NarrativeCard from "../components/narrative/NarrativeCard";
import TracedFigures from "../components/narrative/TracedFigures";

import {
  getNarrative,
  getReport,
  getAnalytics,
} from "../api/api";

export default function Narrative() {

  const [narrative, setNarrative] = useState("");
  const [report, setReport] = useState(null);
  const [analytics, setAnalytics] = useState(null);

  useEffect(() => {

    async function load() {

      const [
        narrativeData,
        reportData,
        analyticsData,
      ] = await Promise.all([
        getNarrative(),
        getReport(),
        getAnalytics(),
      ]);

      setNarrative(narrativeData.narrative);
      setReport(reportData);
      setAnalytics(analyticsData);
    }

    load();

  }, []);

  if (!report || !analytics)
    return (
      <DashboardLayout>
        Loading...
      </DashboardLayout>
    );

  return (
    <DashboardLayout>

      <Header
        title="AI Narrative"
        subtitle="AI Generated Daily Summary"
      />

      <div className="grid gap-8 lg:grid-cols-2">

        <NarrativeCard
          narrative={narrative}
        />

        <TracedFigures
          report={report}
          analytics={analytics}
        />

      </div>

    </DashboardLayout>
  );
}