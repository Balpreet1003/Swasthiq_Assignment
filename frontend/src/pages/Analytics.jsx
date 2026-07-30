import { useEffect, useState } from "react";

import DashboardLayout from "../layouts/DashboardLayout";
import Header from "../components/layout/Header";
import RevenueChart from "../components/analytics/RevenueChart";
import RankingList from "../components/analytics/RankingList";

import { getAnalytics } from "../api/api";

export default function Analytics() {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadAnalytics() {
      try {
        const data = await getAnalytics();
        setAnalytics(data);
      } finally {
        setLoading(false);
      }
    }

    loadAnalytics();
  }, []);

  if (loading) {
    return (
      <DashboardLayout>
        Loading...
      </DashboardLayout>
    );
  }

  if (!analytics) {
    return (
      <DashboardLayout>
        Failed to load analytics.
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>

      <Header
        title="Analytics"
        subtitle="Revenue & Medicine Insights"
        date={analytics.report_date}
      />

      <RevenueChart
        data={analytics.revenue_by_hour}
        peakHour={analytics.peak_hour}
      />

            <div className="mt-8 grid gap-8 lg:grid-cols-2">

        <RankingList
          title="Top Medicines by Quantity"
          items={analytics.top_medicines_by_quantity}
          type="quantity"
        />

        <RankingList
          title="Top Medicines by Revenue"
          items={analytics.top_medicines_by_revenue}
          type="revenue"
        />

      </div>

    </DashboardLayout>
  );
}