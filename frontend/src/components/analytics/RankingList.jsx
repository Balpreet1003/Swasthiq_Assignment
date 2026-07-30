const formatCurrency = (value) =>
  `₹${(value / 100).toFixed(2)}`;

export default function RankingList({
  title,
  items,
  type,
}) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">

      <h2 className="mb-6 text-xl font-semibold">
        {title}
      </h2>

      <div className="space-y-5">

        {items.map((item, index) => (

          <div
            key={item.drug_name}
            className="flex items-center justify-between rounded-xl border border-slate-100 p-4 hover:bg-slate-50"
          >

            <div className="flex items-center gap-4">

              <div
                className="w-6 text-sm font-semibold text-slate-500"
              >
                {index + 1}
              </div>

              <div>

                <p className="font-semibold tracking-wide uppercase">
                  {item.drug_name}
                </p>

                <p className="text-sm text-slate-500">
                  {type === "quantity"
                    ? "Medicine Quantity"
                    : "Revenue Generated"}
                </p>

              </div>

            </div>

            <div className="text-slate-500 font-medium">
                {type === "quantity"
                    ? `${item.quantity} units`
                    : formatCurrency(item.revenue_paise)}
            </div>

          </div>

        ))}

      </div>

    </div>
  );
}