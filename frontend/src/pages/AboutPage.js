import HeroSection from "@/components/HeroSection";
import { Target, Eye, ShieldCheck, Truck, CheckCircle } from "lucide-react";

const HERO_IMG = "https://images.unsplash.com/photo-1574943320219-553eb213f72d?w=1400&h=600&fit=crop";

/* Accent text helper */
function AccentHeading({ children }) {
  return <span className="font-accent italic text-brown">{children}</span>;
}

const CATEGORIES_OVERVIEW = [
  "Farm Machinery",
  "Garden Equipment",
  "Agricultural Inputs",
  "Greenhouse",
  "Irrigation",
  "Miscellaneous",
];

export default function AboutPage() {
  return (
    <div data-testid="about-page">
      <HeroSection
        image={HERO_IMG}
        title="Supporting agriculture that's built to last"
        accentWords={["Supporting", "last"]}
      />

      {/* Business Strategy & Vision */}
      <section data-testid="strategy-vision-section" className="py-20 lg:py-28 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="font-heading text-3xl sm:text-4xl text-olive font-extrabold leading-tight">
              Driven by <AccentHeading>Purpose,</AccentHeading> Guided by <AccentHeading>Quality</AccentHeading>
            </h2>
            <p className="mt-6 text-forest/75 leading-relaxed font-body">
              At Navya Enterprises, our strategy is rooted in understanding the real needs of the agricultural community.
              We focus on providing field-tested, purpose-driven products that align with operational and compliance requirements
              of modern farming, horticulture, and allied sectors.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              {
                icon: Target,
                title: "Purpose-Driven Products",
                desc: "Every product in our portfolio is selected based on real-world application, durability, and performance in Indian agricultural conditions."
              },
              {
                icon: ShieldCheck,
                title: "Quality Assurance",
                desc: "We ensure consistent quality by partnering with trusted manufacturers and conducting field testing before adding any product to our range."
              },
              {
                icon: Truck,
                title: "Timely Fulfillment",
                desc: "We ensure timely availability and smooth order fulfillment, supporting large-scale projects and ongoing procurement needs with efficiency."
              },
              {
                icon: Eye,
                title: "Long-term Vision",
                desc: "Our vision is to be the most dependable agricultural supply partner in western India, empowering farmers and institutions alike."
              },
            ].map((item, i) => (
              <div
                key={i}
                data-testid={`strategy-card-${i}`}
                className="bg-sage/8 border border-sage/15 rounded-2xl p-7 hover:shadow-md transition-shadow group"
              >
                <div className="w-12 h-12 rounded-xl bg-olive flex items-center justify-center mb-5 group-hover:bg-forest transition-colors">
                  <item.icon size={22} className="text-sage" />
                </div>
                <h3 className="font-heading text-xl text-olive font-extrabold">{item.title}</h3>
                <p className="mt-3 text-sm text-forest/70 leading-relaxed font-body">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* About Our Firm */}
      <section data-testid="about-firm-section" className="py-20 bg-sage/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-20 items-center">
            <div className="rounded-2xl overflow-hidden shadow-lg">
              <img
                src="https://images.unsplash.com/photo-1770982699065-4d631e37186f?w=700&h=500&fit=crop"
                alt="Navya Enterprises Facility"
                className="w-full h-[400px] object-cover"
                data-testid="about-firm-image"
              />
            </div>
            <div>
              <h2 className="font-heading text-3xl sm:text-4xl text-olive font-extrabold leading-tight">
                About Our <AccentHeading>Firm</AccentHeading>
              </h2>
              <p className="mt-6 text-forest/80 leading-relaxed font-body">
                Navya Enterprises has been proudly serving the agricultural community since 1999.
                Based in Udaipur, Rajasthan, we have grown into a trusted name for agricultural
                tools, equipment, and inputs across the region.
              </p>
              <p className="mt-4 text-forest/80 leading-relaxed font-body">
                We supply tools and inputs across agriculture, floriculture, horticulture, nurseries,
                greenhouses, and government-backed projects. As an authorized distributor for multiple
                trusted brands, we provide procurement-ready supply solutions for institutional and
                B2B requirements with dedicated after-sales service.
              </p>
              <div className="mt-8 flex flex-wrap gap-3">
                {["Since 1999", "Udaipur Based", "B2B & Institutional", "Authorized Distributor"].map((tag) => (
                  <span
                    key={tag}
                    className="px-4 py-2 bg-olive/10 text-olive text-xs font-semibold rounded-full font-body"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* What We Offer */}
      <section data-testid="product-range-section" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-20 items-center">
            <div>
              <h2 className="font-heading text-3xl sm:text-4xl text-olive font-extrabold leading-tight">
                What We <AccentHeading>Offer</AccentHeading>
              </h2>
              <p className="mt-6 text-forest/80 leading-relaxed font-body">
                A wide range of high-quality agricultural tools, machinery, and inputs built for reliable performance across farming and horticulture.
              </p>

              {/* Service bullet pointers */}
              <div className="mt-6 space-y-3">
                {[
                  "Quality products from trusted brands",
                  "Dedicated after-sales service",
                  "Our own product range",
                ].map((item, i) => (
                  <div key={i} className="flex items-center gap-3">
                    <CheckCircle size={18} className="text-forest flex-shrink-0" />
                    <span className="text-sm text-forest/80 font-semibold font-body">{item}</span>
                  </div>
                ))}
              </div>

              {/* Categories removed as per user request */}
            </div>
            <div className="rounded-2xl overflow-hidden shadow-lg">
              <img
                src="https://images.unsplash.com/photo-1615811361523-6bd03d7748e7?w=700&h=500&fit=crop"
                alt="Product Range"
                className="w-full h-[400px] object-cover"
                data-testid="product-range-image"
              />
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
