import { Link } from "react-router-dom";
import { MapPin, Phone, Mail, Instagram, Youtube } from "lucide-react";

const LOGO_URL = "/navya-logo-trimmed.png";

export default function Footer() {
  return (
    <footer data-testid="site-footer" className="bg-olive text-sage/80">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-12 lg:gap-16">
          {/* Brand */}
          <div className="space-y-5">
            <img src={LOGO_URL} alt="Navya Enterprises" className="h-[127px] w-auto" />
            <p className="text-sm leading-relaxed text-sage/60 max-w-xs">
              Proudly serving the agricultural community since 1999. Trusted supplier of tools and inputs across agriculture, floriculture, and horticulture.
            </p>
          </div>

          {/* Quick Links */}
          <div className="space-y-5">
            <h4 className="font-heading text-xl text-white font-bold">Quick Links</h4>
            <div className="flex flex-col gap-3">
              {[
                { label: "Home", path: "/" },
                { label: "About Us", path: "/about" },
                { label: "Products", path: "/products" },
                { label: "Connect With Us", path: "/connect" },
              ].map((link) => (
                <Link
                  key={link.path}
                  to={link.path}
                  data-testid={`footer-link-${link.label.toLowerCase().replace(/\s+/g, "-")}`}
                  className="text-sm hover:text-white transition-colors duration-200 w-fit"
                >
                  {link.label}
                </Link>
              ))}
            </div>
          </div>

          {/* Contact + Social */}
          <div className="space-y-5">
            <h4 className="font-heading text-xl text-white font-bold">Get In Touch</h4>
            <div className="flex flex-col gap-3 text-sm">
              <div className="flex items-start gap-3">
                <MapPin size={16} className="mt-0.5 flex-shrink-0 text-sage" />
                <span>44F Block, Subcity Centre, Opposite Income-tax Department, Udaipur, Rajasthan 313001</span>
              </div>
              <div className="flex items-center gap-3">
                <Phone size={16} className="flex-shrink-0 text-sage" />
                <span>+91-9414104098</span>
              </div>
              <div className="flex items-center gap-3">
                <Mail size={16} className="flex-shrink-0 text-sage" />
                <span>navyaenterprises73@gmail.com</span>
              </div>
            </div>
            {/* Social */}
            <div className="flex items-center gap-4 pt-2">
              <a
                href="https://www.instagram.com/navyaenterprises.agri/"
                target="_blank"
                rel="noopener noreferrer"
                data-testid="footer-instagram"
                className="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center hover:bg-sage/30 transition-colors"
              >
                <Instagram size={18} className="text-sage" />
              </a>
              <a
                href="https://youtube.com/@navyaenterprises-c3n6v?si=FFYekcCTvUc-4f5G"
                target="_blank"
                rel="noopener noreferrer"
                data-testid="footer-youtube"
                className="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center hover:bg-sage/30 transition-colors"
              >
                <Youtube size={18} className="text-sage" />
              </a>
            </div>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="mt-14 pt-6 border-t border-forest/30 flex flex-col sm:flex-row items-center justify-between gap-3">
          <p className="text-xs text-sage/50">
            &copy; {new Date().getFullYear()} Navya Enterprises. All rights reserved.
          </p>
          <p className="text-xs text-sage/40">
            Udaipur, Rajasthan
          </p>
        </div>
      </div>
    </footer>
  );
}
