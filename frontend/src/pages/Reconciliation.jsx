import { useEffect, useState } from "react";

import DashboardLayout from "../layouts/DashboardLayout";
import Header from "../components/layout/Header";
import StatCard from "../components/reconciliation/StatCard";
import PaymentTable from "../components/reconciliation/PaymentTable";
import UploadSection from "../components/reconciliation/UploadSection";

import { getReport } from "../api/api";

const formatCurrency = (paise = 0) =>
  `₹${(Number(paise) / 100).toFixed(2)}`;

export default function Reconciliation() {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadReport = async () => {
    try {
      setLoading(true);
      setError("");

      const data = await getReport();

      console.log("Fresh Report:", data); // Add this
      setReport(data);
    } catch (err) {
      console.error(err);
      setError("Failed to load reconciliation report.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadReport();
  }, []);

  if (loading) {
    return (
      <DashboardLayout>
        <div className="text-lg text-slate-500">
          Loading...
        </div>
      </DashboardLayout>
    );
  }

  if (error) {
    return (
      <DashboardLayout>
        <div className="rounded-xl border border-red-200 bg-red-50 p-6 text-red-700">
          {error}
        </div>
      </DashboardLayout>
    );
  }

  if (!report) {
    return (
      <DashboardLayout>
        <div className="rounded-xl border border-yellow-200 bg-yellow-50 p-6">
          No reconciliation data found.
        </div>
      </DashboardLayout>
    );
  }

  const billed = report.total_billed_paise;
  const collected = report.total_collected_paise;

  const collectionPercentage =
    billed === 0
      ? 0
      : Math.round((collected / billed) * 100);

  return (
    <DashboardLayout>
      <Header
        title="EOD Reconciliation"
        subtitle="Mehta Multi-Speciality Clinic"
      />
      <UploadSection
        onUploadSuccess={loadReport}
      />

      <div className="mt-8 grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-4">

        <StatCard
          title="Total Billed"
          value={formatCurrency(report.total_billed_paise)}
          subtitle="Billing Summary"
          subtitleColor="text-blue-600"
        />

        <StatCard
          title="Collected"
          value={formatCurrency(report.total_collected_paise)}
          subtitle={`${collectionPercentage}% of billed`}
          subtitleColor="text-green-600"
        />

        <StatCard
          title="Outstanding"
          value={formatCurrency(report.outstanding_paise)}
          subtitle={
            report.outstanding_paise > 0
              ? "Pending collection"
              : "No pending dues"
          }
          subtitleColor="text-amber-500"
        />

        <StatCard
          title="Refunds"
          value={formatCurrency(report.total_refund_paise)}
          subtitle={
            report.total_refund_paise > 0
              ? "Refund issued"
              : "No refunds"
          }
          subtitleColor="text-red-500"
        />

      </div>

      <div className="mt-8">
        <PaymentTable
          paymentSummary={report.payment_summary}
        />
      </div>
    </DashboardLayout>
  );
}