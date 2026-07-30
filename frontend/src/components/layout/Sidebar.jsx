import { NavLink } from "react-router-dom";
import {
  ClipboardList,
  BarChart3,
  Sparkles,
} from "lucide-react";

const menuItems = [
  {
    path: "/",
    icon: ClipboardList,
  },
  {
    path: "/analytics",
    icon: BarChart3,
  },
  {
    path: "/narrative",
    icon: Sparkles,
  },
];

export default function Sidebar() {
  return (
    <aside className="w-20 bg-white border-r border-slate-200 flex flex-col items-center py-8">

      <nav className="flex flex-col gap-6">

        {menuItems.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `h-12 w-12 rounded-xl flex items-center justify-center transition-all
                ${
                  isActive
                    ? "bg-blue-100 text-blue-600"
                    : "text-slate-500 hover:bg-slate-100"
                }`
              }
            >
              <Icon size={20} />
            </NavLink>
          );
        })}
      </nav>
    </aside>
  );
}