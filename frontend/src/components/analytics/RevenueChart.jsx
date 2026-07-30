import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Cell,
} from "recharts";

const LIGHT_BAR = "#C7D7F5";
const PEAK_BAR = "#2563EB";

const formatCurrency = (value) =>
  `₹${(value / 100).toFixed(0)}`;

export default function RevenueChart({ data, peakHour }) {
  // Dynamic bar width
  const barSize = Math.min(
    64, // Maximum width
    Math.max(
      20, // Minimum width
      Math.floor(520 / data.length)
    )
  );

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">

      <div className="mb-6 flex items-center justify-between">
        <h2 className="text-xl font-semibold">
          Revenue by Hour of Day
        </h2>

        <span className="rounded-full bg-blue-100 px-3 py-1 text-sm font-semibold text-blue-700">
          Peak: {peakHour.hour} — {formatCurrency(peakHour.revenue_paise)}
        </span>
      </div>

      <ResponsiveContainer width="100%" height={300}>
        <BarChart
          data={data}
          margin={{
            top: 20,
            right: 10,
            left: -20,
            bottom: 5,
          }}
          barGap={6}
          barCategoryGap="18%"
        >
          <CartesianGrid
            vertical={false}
            stroke="#EEF2F7"
            strokeDasharray="3 3"
          />

          <XAxis
            dataKey="hour"
            axisLine={false}
            tickLine={false}
            tick={{ fill: "#64748B", fontSize: 13 }}
          />

          <YAxis
            axisLine={false}
            tickLine={false}
            tickFormatter={formatCurrency}
            tick={{ fill: "#64748B", fontSize: 13 }}
          />

          <Tooltip
            formatter={formatCurrency}
            cursor={{ fill: "#EFF6FF" }}
          />

          <Bar
            dataKey="revenue_paise"
            radius={[8, 8, 0, 0]}
            barSize={barSize}
          >
            {data.map((entry, index) => (
              <Cell
                key={index}
                fill={
                  entry.hour === peakHour.hour
                    ? PEAK_BAR
                    : LIGHT_BAR
                }
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>

    </div>
  );
}