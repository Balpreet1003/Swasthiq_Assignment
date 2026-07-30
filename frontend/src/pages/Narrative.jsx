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

      setReport(await getReport(),);
      setAnalytics(await getAnalytics());
      const narrativeData = await getNarrative();
      setNarrative(narrativeData.narrative);
    }

    load();

  }, []);


  return (
    <DashboardLayout>

      <Header
        title="AI Narrative"
        subtitle="AI Generated Daily Summary"
        date={report?.report_date}
      />

      <div>

        {
          (!report || !analytics) ? (
            <div className="col-span-2 text-lg text-slate-500">
              Loading...
            </div>
          ) : (
            <div className="grid gap-8 lg:grid-cols-2">
              <NarrativeCard
                narrative={narrative}
                isLoading={!narrative}
              />

              <TracedFigures
                report={report}
                analytics={analytics}
              />
            </div>
          )
        }

      </div>

    </DashboardLayout>
  );
}