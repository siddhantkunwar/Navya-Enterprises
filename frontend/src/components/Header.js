import { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { Menu, X } from "lucide-react";

const LOGO_URL = "/navya-logo-trimmed.png";

const NAV_ITEMS = [
  { label: "Home", path: "/" },
  { label: "About Us", path: "/about" },
  { label: "Products", path: "/products" },
  { label: "Connect", path: "/connect" },
];

export default function Header() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const location = useLocation();

  return (
    <header
      data-testid="site-header"
      className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-sage/20 shadow-sm"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          {/* Logo - trimmed, no extra padding */}
          <Link to="/" data-testid="header-logo-link" className="flex-shrink-0">
            <img
              src={LOGO_URL}
              alt="Navya Enterprises"
              className="h-16 w-auto object-contain"
            />
          </Link>

          {/* Desktop Nav */}
          <nav className="hidden md:flex items-center gap-1" data-testid="desktop-nav">
            {NAV_ITEMS.map((item) => {
              const isActive = location.pathname === item.path;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  data-testid={`nav-${item.label.toLowerCase().replace(/\s+/g, "-")}`}
                  className={`px-5 py-2.5 rounded-full text-sm font-semibold tracking-wide transition-all duration-300
                    ${isActive
                      ? "bg-olive text-white"
                      : "text-olive hover:text-forest hover:bg-sage/15"
                    }`}
                >
                  {item.label}
                </Link>
              );
            })}
          </nav>

          {/* Mobile toggle */}
          <button
            data-testid="mobile-menu-toggle"
            className="md:hidden text-olive p-2"
            onClick={() => setMobileOpen(!mobileOpen)}
          >
            {mobileOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </div>

      {/* Mobile Nav */}
      {mobileOpen && (
        <div className="md:hidden bg-white border-t border-sage/20" data-testid="mobile-nav">
          <div className="px-4 py-4 flex flex-col gap-2">
            {NAV_ITEMS.map((item) => {
              const isActive = location.pathname === item.path;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  data-testid={`mobile-nav-${item.label.toLowerCase().replace(/\s+/g, "-")}`}
                  onClick={() => setMobileOpen(false)}
                  className={`px-4 py-3 rounded-lg text-sm font-semibold transition-colors
                    ${isActive
                      ? "bg-olive/10 text-olive"
                      : "text-forest/70 hover:text-olive hover:bg-sage/5"
                    }`}
                >
                  {item.label}
                </Link>
              );
            })}
          </div>
        </div>
      )}
    </header>
  );
}
