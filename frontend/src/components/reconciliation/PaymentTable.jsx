const formatCurrency = (paise) =>
  `₹${(paise / 100).toFixed(2)}`;

export default function PaymentTable({
  paymentSummary,
}) {
  return (
    <div
      className="
      rounded-2xl
      border
      border-slate-200
      bg-white
      shadow-sm
      overflow-hidden
    "
    >

      <div className="border-b border-slate-200 px-6 py-3">

        <h2 className="text-lg font-semibold">
          Payment Mode Breakdown
        </h2>

      </div>

      <table className="min-w-full">

        <thead className="bg-slate-50">

          <tr>

            <th className="px-6 py-4 text-left text-sm font-semibold text-slate-500">
              Payment Mode
            </th>

            <th className="px-6 py-4 text-right text-sm font-semibold text-slate-500">
              Billed
            </th>

            <th className="px-6 py-4 text-right text-sm font-semibold text-slate-500">
              Collected
            </th>

            <th className="px-6 py-4 text-right text-sm font-semibold text-slate-500">
              Outstanding
            </th>

            <th className="px-6 py-4 text-right text-sm font-semibold text-slate-500">
              Refunded
            </th>

          </tr>

        </thead>

        <tbody>

          {paymentSummary.map((row) => (
            <tr
              key={row.payment_mode}
              className="border-t border-slate-100 hover:bg-slate-50"
            >

              <td className="px-6 py-5 font-medium capitalize">
                {row.payment_mode}
              </td>

              <td className="px-6 py-5 text-right font-medium">
                {formatCurrency(row.billed_paise)}
              </td>

              <td className="px-6 py-5 text-right font-medium">
                {formatCurrency(row.collected_paise)}
              </td>

              <td className="px-6 py-5 text-right font-medium">
                {formatCurrency(row.outstanding_paise)}
              </td>

              <td className="px-6 py-5 text-right font-medium text-red-600">
                {formatCurrency(row.refunded_paise)}
              </td>

            </tr>
          ))}

        </tbody>

      </table>

    </div>
  );
}