import { useState, useEffect, useRef, useCallback } from "react";
import { Link } from "react-router-dom";
import { ChevronLeft, ChevronRight, ArrowRight, CheckCircle } from "lucide-react";
import axios from "axios";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const HERO_IMG = "https://customer-assets.emergentagent.com/job_agri-layout-preview/artifacts/3eyqyo7h_hero%20image%20for%20home%20page.png";

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

function ProductCarousel({ products }) {
  const scrollRef = useRef(null);

  const scroll = useCallback((dir) => {
    if (!scrollRef.current) return;
    const amount = 280;
    scrollRef.current.scrollBy({ left: dir === "left" ? -amount : amount, behavior: "smooth" });
  }, []);

  if (!products.length) return null;

  return (
    <div className="relative" data-testid="popular-products-carousel">
      <button
        onClick={() => scroll("left")}
        data-testid="carousel-prev-products"
        className="carousel-btn absolute left-0 top-1/2 -translate-y-1/2 -translate-x-4 z-10 w-10 h-10 rounded-full bg-olive text-white flex items-center justify-center shadow-lg"
      >
        <ChevronLeft size={20} />
      </button>

      <div ref={scrollRef} className="flex gap-6 overflow-x-auto scrollbar-hide scroll-smooth px-2 py-4" style={{ scrollbarWidth: "none" }}>
        {products.map((p) => (
          <Link
            key={p.id}
            to={`/products/${p.id}`}
            data-testid={`popular-product-${p.id}`}
            className="product-card flex-shrink-0 w-56 bg-white rounded-2xl overflow-hidden shadow-sm border border-sage/20"
          >
            <div className="h-40 overflow-hidden">
              <img src={p.image} alt={p.name} className="w-full h-full object-cover" />
            </div>
            <div className="p-4">
              <p className="text-xs text-sage font-bold uppercase tracking-wider">{p.category}</p>
              <h4 className="font-heading text-lg font-bold text-olive mt-1 leading-tight">{p.name}</h4>
            </div>
          </Link>
        ))}
      </div>

      <button
        onClick={() => scroll("right")}
        data-testid="carousel-next-products"
        className="carousel-btn absolute right-0 top-1/2 -translate-y-1/2 translate-x-4 z-10 w-10 h-10 rounded-full bg-olive text-white flex items-center justify-center shadow-lg"
      >
        <ChevronRight size={20} />
      </button>
    </div>
  );
}

function BrandsCarousel() {
  const scrollRef = useRef(null);

  const scroll = useCallback((dir) => {
    if (!scrollRef.current) return;
    scrollRef.current.scrollBy({ left: dir === "left" ? -200 : 200, behavior: "smooth" });
  }, []);

  return (
    <div className="relative" data-testid="brands-carousel">
      <button
        onClick={() => scroll("left")}
        data-testid="carousel-prev-brands"
        className="carousel-btn absolute left-0 top-1/2 -translate-y-1/2 -translate-x-4 z-10 w-10 h-10 rounded-full bg-olive text-white flex items-center justify-center shadow-lg"
      >
        <ChevronLeft size={20} />
      </button>

      <div ref={scrollRef} className="flex gap-10 overflow-x-auto scrollbar-hide scroll-smooth px-2 py-4 items-center justify-center" style={{ scrollbarWidth: "none" }}>
        {BRAND_LOGOS.map((b, i) => (
          <div
            key={i}
            data-testid={`brand-logo-${i}`}
            className="flex-shrink-0 w-28 h-28 rounded-full bg-white shadow-sm border border-sage/20 flex items-center justify-center overflow-hidden hover:shadow-md transition-shadow p-3"
          >
            <img src={b.img} alt={b.name} className="w-full h-full object-contain" />
          </div>
        ))}
      </div>

      <button
        onClick={() => scroll("right")}
        data-testid="carousel-next-brands"
        className="carousel-btn absolute right-0 top-1/2 -translate-y-1/2 translate-x-4 z-10 w-10 h-10 rounded-full bg-olive text-white flex items-center justify-center shadow-lg"
      >
        <ChevronRight size={20} />
      </button>
    </div>
  );
}

export default function HomePage() {
  const [popularProducts, setPopularProducts] = useState([]);

  useEffect(() => {
    axios.get(`${API}/products?popular=true`).then((r) => setPopularProducts(r.data)).catch(console.error);
  }, []);

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
            className="font-heading text-4xl sm:text-5xl lg:text-7xl text-white font-black tracking-tight opacity-0 animate-fade-in leading-tight"
          >
            Built for the fields<br />that feed the future.
          </h1>
        </div>
      </section>

      {/* Brief About + Work Image */}
      <section data-testid="about-brief-section" className="py-20 lg:py-28 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-20 items-center">
            <div className="opacity-0 animate-slide-in-left">
              <h2 className="font-heading text-3xl sm:text-4xl text-olive font-black leading-tight">
                Serving the Agricultural Community with Excellence
              </h2>
              <p className="mt-6 text-forest/80 leading-relaxed">
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
                    <span className="text-sm text-forest/80">{item}</span>
                  </div>
                ))}
              </div>
              <Link
                to="/about"
                data-testid="home-about-link"
                className="mt-8 inline-flex items-center gap-2 px-6 py-3 bg-olive text-white rounded-full text-sm font-bold hover:bg-forest transition-colors"
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
            <h2 className="font-heading text-3xl sm:text-4xl text-olive font-black">Popular Products</h2>
          </div>
          <ProductCarousel products={popularProducts} />
          <div className="text-center mt-10">
            <Link
              to="/products"
              data-testid="home-view-all-products"
              className="inline-flex items-center gap-2 px-6 py-3 border-2 border-olive text-olive rounded-full text-sm font-bold hover:bg-olive hover:text-white transition-all"
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
            <h2 className="font-heading text-3xl sm:text-4xl text-olive font-black">Brands We Deal With</h2>
          </div>
          <BrandsCarousel />
        </div>
      </section>

      {/* Testimonials */}
      <section data-testid="testimonials-section" className="py-20 bg-sage/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="font-heading text-3xl sm:text-4xl text-olive font-black">What Our Clients Say</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {TESTIMONIALS.map((t, i) => (
              <div
                key={i}
                data-testid={`testimonial-${i}`}
                className="bg-white rounded-2xl p-6 shadow-sm border border-sage/15 hover:shadow-md transition-shadow"
              >
                <p className="text-forest/70 text-sm leading-relaxed italic">"{t.text}"</p>
                <div className="mt-5 pt-4 border-t border-sage/15">
                  <p className="font-heading text-lg font-bold text-olive">{t.name}</p>
                  <p className="text-xs text-sage">{t.location}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
