import HeroSection from "@/components/HeroSection";
import { User, Phone, MapPin, Clock, Mail } from "lucide-react";
import { CONTACT_INFO } from "@/data/contact";
const HERO_IMG = "https://images.unsplash.com/photo-1500937386664-56d1dfef3854?w=1400&h=600&fit=crop";

export default function ConnectPage() {
  const contact = CONTACT_INFO;

  const infoItems = [
    { icon: User, label: "Point of Contact", value: "Vinay Gupta" },
    { icon: Phone, label: "Mobile", value: contact.phone },
    { icon: MapPin, label: "Location", value: contact.address },
    { icon: Clock, label: "Business Timing", value: "Mon - Sat: 11:00 AM - 7:00 PM" },
    { icon: Mail, label: "Email", value: contact.email },
  ];

  return (
    <div data-testid="connect-page">
      <HeroSection
        image={HERO_IMG}
        title="Connect With Us"
        subtitle="Reach out to discuss your agricultural requirements and procurement needs"
        accentWord="Us"
      />

      <section className="py-20 lg:py-28 bg-white" data-testid="contact-info-section">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-14">
            <h2 className="font-heading text-3xl sm:text-4xl text-olive font-extrabold">
              Get In <span className="font-accent italic text-brown">Touch</span>
            </h2>
          </div>

          <div className="bg-sage/5 rounded-3xl border border-sage/15 p-8 sm:p-10 space-y-0 divide-y divide-sage/15">
            {infoItems.map((item, i) => (
              <div
                key={i}
                data-testid={`contact-item-${item.label.toLowerCase().replace(/\s+/g, "-")}`}
                className="flex items-start gap-5 py-6 first:pt-0 last:pb-0"
              >
                <div className="w-11 h-11 rounded-xl bg-olive flex items-center justify-center flex-shrink-0">
                  <item.icon size={20} className="text-sage" />
                </div>
                <div>
                  <p className="text-xs text-sage font-semibold uppercase tracking-wider mb-1 font-body">{item.label}</p>
                  <p className="text-base text-olive font-semibold font-body">{item.value}</p>
                </div>
              </div>
            ))}
          </div>

          {/* Map */}
          <div className="mt-12 rounded-2xl overflow-hidden shadow-lg border border-sage/15" data-testid="map-section">
            <iframe
              title="Navya Enterprises Location"
              src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3627.7975234775!2d73.71245!3d24.58518!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3967e56c8e4e5bcb%3A0x1234567890!2sSubcity%20Centre%2C%20Udaipur%2C%20Rajasthan!5e0!3m2!1sen!2sin!4v1700000000000!5m2!1sen!2sin"
              width="100%"
              height="300"
              style={{ border: 0 }}
              allowFullScreen
              loading="lazy"
              referrerPolicy="no-referrer-when-downgrade"
            />
          </div>
        </div>
      </section>
    </div>
  );
}
