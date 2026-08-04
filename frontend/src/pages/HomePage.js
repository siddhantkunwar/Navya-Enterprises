import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { ArrowRight, CheckCircle } from "lucide-react";
import useEmblaCarousel from "embla-carousel-react";
import { POPULAR_PRODUCTS } from "@/data/products";

const HERO_IMG = "/hero-home.webp";

const BRAND_LOGOS = [
  { name: "Stihl", img: "/brands/stihl.png" },
  { name: "Tata", img: "/brands/tata.png" },
  { name: "Mahindra & Mahindra", img: "/brands/M&M.png" },
  { name: "Aspee", img: "/brands/Aspee.png" },
  { name: "Falcon", img: "/brands/falcon.png" },
  { name: "Neptune", img: "/brands/neptune.png" },
  { name: "OleoMac", img: "/brands/oleomac.png" },
  { name: "Concorde", img: "/brands/concorde.png" },
  { name: "MaxGreen", img: "/brands/maxgreen.png" },
];

const TESTIMONIALS = [
  { name: "Rajesh Sharma", location: "Udaipur", text: "Navya Enterprises has been our go-to supplier for all agricultural needs. Their product quality and timely delivery is exceptional." },
  { name: "Priya Patel", location: "Ahmedabad", text: "Excellent range of garden equipment and greenhouse materials. The team is very knowledgeable and provides great after-sales support." },
  { name: "Mohan Singh", location: "Jodhpur", text: "We have been purchasing irrigation equipment from Navya for over 5 years. Reliable products and competitive pricing every time." },
  { name: "Kavita Joshi", location: "Jaipur", text: "The rescue kits we purchased for our wildlife sanctuary are of outstanding quality. Navya Enterprises is a trusted partner." },
];

/* Sleek slider dot component */
function SliderDots({ api, count }) {
  const [selected, setSelected] = useState(0);
  const [scrollProgress, setScrollProgress] = useState(0);

  useEffect(() => {
    if (!api) return;
    const onSelect = () => setSelected(api.selectedScrollSnap());
    const onScroll = () => {
      const progress = Math.max(0, Math.min(1, api.scrollProgress()));
      setScrollProgress(progress);
    };
    api.on("select", onSelect);
    api.on("scroll", onScroll);
    onSelect();
    return () => {
      api.off("select", onSelect);
      api.off("scroll", onScroll);
    };
  }, [api]);

  if (count <= 1) return null;

  return (
    <div className="flex items-center justify-center gap-2 mt-8" data-testid="slider-dots">
      {/* Progress bar style slider */}
      <div className="flex items-center gap-1.5">
        {Array.from({ length: count }).map((_, i) => (
          <button
            key={i}
            data-testid={`slider-dot-${i}`}
            onClick={() => api && api.scrollTo(i)}
            className={`rounded-full transition-all duration-300 ${
              i === selected
                ? "w-8 h-2 bg-olive"
                : "w-2 h-2 bg-sage/40 hover:bg-sage/60"
            }`}
          />
        ))}
      </div>
    </div>
  );
}

function ProductCarousel({ products }) {
  const [emblaRef, emblaApi] = useEmblaCarousel({
    align: "start",
    loop: false,
    slidesToScroll: 4,
    containScroll: "trimSnaps",
    dragFree: true,
  });

  const snapCount = emblaApi ? emblaApi.scrollSnapList().length : 0;

  if (!products.length) return null;

  return (
    <div data-testid="popular-products-carousel">
      <div className="overflow-hidden" ref={emblaRef}>
        <div className="flex gap-6">
          {products.map((p) => (
            <Link
              key={p.id}
              to={`/products/${p.id}`}
              state={{ from: "/" }}
              data-testid={`popular-product-${p.id}`}
              className="product-card flex-shrink-0 w-80 bg-white rounded-2xl overflow-hidden shadow-sm border border-sage/20"
            >
              <div className="h-64 overflow-hidden">
                <img src={p.image} alt={p.name} className="w-full h-full object-cover" />
              </div>
              <div className="p-4">
                <h4 className="font-heading text-base font-extrabold text-olive leading-tight">{p.name}</h4>
              </div>
            </Link>
          ))}
        </div>
      </div>
      <SliderDots api={emblaApi} count={snapCount} />
    </div>
  );
}

function BrandsCarousel() {
  // Double the logos for seamless infinite loop
  const doubled = [...BRAND_LOGOS, ...BRAND_LOGOS];

  return (
    <div data-testid="brands-carousel" className="overflow-hidden">
      <div className="brands-marquee flex items-center gap-10">
        {doubled.map((b, i) => (
          <div
            key={i}
            data-testid={`brand-logo-${i}`}
            className="flex-shrink-0 w-52 h-52 rounded-2xl bg-white shadow-sm border border-sage/20 flex items-center justify-center overflow-hidden hover:shadow-md transition-shadow p-5"
          >
            <img src={b.img} alt={b.name} className="w-full h-full object-contain" />
          </div>
        ))}
      </div>
    </div>
  );
}

/* Accent text helper: wraps keywords in Bodoni Moda italic */
function AccentHeading({ children }) {
  return <span className="font-accent italic text-brown">{children}</span>;
}

export default function HomePage() {
  const popularProducts = POPULAR_PRODUCTS;

  return (
    <div data-testid="home-page">
      {/* Hero */}
      <section data-testid="hero-section" className="relative h-[60vh] min-h-[420px] max-h-[600px] overflow-hidden">
        <img
          src={HERO_IMG}
          alt="Agricultural landscape"
          className="absolute inset-0 w-full h-full object-cover"
        />
        <div className="hero-overlay absolute inset-0" />
        <div className="relative z-10 h-full flex flex-col items-center justify-center text-center px-4">
          <h1
            data-testid="hero-title"
            className="font-heading text-4xl sm:text-5xl lg:text-7xl text-white font-extrabold tracking-tight opacity-0 animate-fade-in leading-tight"
          >
            Built for the <span className="font-accent italic text-sage">fields</span><br className="hidden sm:block" />{" "}that feed the <span className="font-accent italic text-sage">future.</span>
          </h1>
        </div>
      </section>

      {/* Brief About + Work Image */}
      <section data-testid="about-brief-section" className="py-20 lg:py-28 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-20 items-center">
            <div className="opacity-0 animate-slide-in-left">
              <h2 className="font-heading text-3xl sm:text-4xl text-olive font-extrabold leading-tight">
                Serving the Agricultural Community with <AccentHeading>Excellence</AccentHeading>
              </h2>
              <p className="mt-6 text-forest/80 leading-relaxed font-body">
                Navya Enterprises has been proudly serving the agricultural community since 1999.
                We supply tools and inputs across agriculture, floriculture, horticulture, nurseries,
                greenhouses, and government-backed projects.
              </p>
              <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 gap-3">
                {[
                  "Authorized distributor for trusted brands",
                  "Procurement-ready for B2B requirements",
                  "Value-for-money solutions",
                  "Dedicated after-sales service",
                ].map((item, i) => (
                  <div key={i} className="flex items-start gap-2.5">
                    <CheckCircle size={18} className="text-forest mt-0.5 flex-shrink-0" />
                    <span className="text-sm text-forest/80 font-body">{item}</span>
                  </div>
                ))}
              </div>
              <Link
                to="/about"
                data-testid="home-about-link"
                className="mt-8 inline-flex items-center gap-2 px-6 py-3 bg-olive text-white rounded-full text-sm font-semibold hover:bg-forest transition-colors"
              >
                Learn More <ArrowRight size={16} />
              </Link>
            </div>
            <div className="opacity-0 animate-slide-in-right">
              <div className="rounded-2xl overflow-hidden shadow-lg">
                <img
                  src="https://images.unsplash.com/photo-1615811361523-6bd03d7748e7?w=700&h=500&fit=crop"
                  alt="Agricultural work"
                  className="w-full h-[380px] object-cover"
                  data-testid="home-work-image"
                />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Popular Products Slideshow */}
      <section data-testid="popular-products-section" className="py-20 bg-gradient-to-b from-white to-sage/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="font-heading text-3xl sm:text-4xl text-olive font-extrabold">
              Popular <AccentHeading>Products</AccentHeading>
            </h2>
          </div>
          <ProductCarousel products={popularProducts} />
          <div className="text-center mt-10">
            <Link
              to="/products"
              data-testid="home-view-all-products"
              className="inline-flex items-center gap-2 px-6 py-3 border-2 border-olive text-olive rounded-full text-sm font-semibold hover:bg-olive hover:text-white transition-all"
            >
              View All Products <ArrowRight size={16} />
            </Link>
          </div>
        </div>
      </section>

      {/* Brands Slideshow */}
      <section data-testid="brands-section" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="font-heading text-3xl sm:text-4xl text-olive font-extrabold">
              Brands We <AccentHeading>Deal With</AccentHeading>
            </h2>
          </div>
          <BrandsCarousel />
        </div>
      </section>

      {/* Testimonials */}
      <section data-testid="testimonials-section" className="py-20 bg-sage/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="font-heading text-3xl sm:text-4xl text-olive font-extrabold">
              What Our <AccentHeading>Clients</AccentHeading> Say
            </h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {TESTIMONIALS.map((t, i) => (
              <div
                key={i}
                data-testid={`testimonial-${i}`}
                className="bg-white rounded-2xl p-6 shadow-sm border border-sage/15 hover:shadow-md transition-shadow"
              >
                <p className="text-forest/70 text-sm leading-relaxed italic font-body">"{t.text}"</p>
                <div className="mt-5 pt-4 border-t border-sage/15">
                  <p className="font-heading text-lg font-extrabold text-olive">{t.name}</p>
                  <p className="text-xs text-sage font-body">{t.location}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
