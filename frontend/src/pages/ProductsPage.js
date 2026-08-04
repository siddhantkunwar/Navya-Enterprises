import { useState } from "react";
import { Link } from "react-router-dom";
import HeroSection from "@/components/HeroSection";
import { Search } from "lucide-react";
import { PRODUCTS, CATEGORIES } from "@/data/products";
const HERO_IMG = "https://images.unsplash.com/photo-1774351128444-9f2bd99f71ed?w=1400&h=600&fit=crop";

export default function ProductsPage() {
  const products = PRODUCTS;
  const categories = CATEGORIES;
  const [activeCategory, setActiveCategory] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const loading = false;

  const handleCategoryButton = (cat) => {
    setActiveCategory(activeCategory === cat ? null : cat);
  };

  const filteredProducts = products.filter((p) => {
    const matchCategory = activeCategory ? p.category === activeCategory : true;
    const matchSearch = searchTerm
      ? p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        p.category.toLowerCase().includes(searchTerm.toLowerCase())
      : true;
    return matchCategory && matchSearch;
  });

  return (
    <div data-testid="products-page">
      <HeroSection
        image={HERO_IMG}
        title="Equipment that earns its place in the field."
        accentWords={["Equipment", "field."]}
      />

      <section className="py-12 lg:py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Search */}
          <div className="mb-8 max-w-md">
            <div className="relative">
              <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-sage" />
              <input
                type="text"
                data-testid="product-search"
                placeholder="Search products..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-3 rounded-full border border-sage/30 bg-white text-olive text-sm focus:outline-none focus:ring-2 focus:ring-forest/30 focus:border-forest/40 font-body"
              />
            </div>
          </div>

          {/* Category Button Filters */}
          <div className="mb-8 flex flex-wrap gap-2" data-testid="category-button-filters">
            <button
              data-testid="category-btn-all"
              onClick={() => setActiveCategory(null)}
              className={`category-pill px-5 py-2.5 rounded-full text-sm font-semibold border font-body
                ${!activeCategory
                  ? "bg-olive text-white border-olive"
                  : "bg-white text-olive border-sage/30 hover:bg-sage/10"
                }`}
            >
              All Products
            </button>
            {categories.map((cat) => (
              <button
                key={cat}
                data-testid={`category-btn-${cat.toLowerCase().replace(/\s+/g, "-")}`}
                onClick={() => handleCategoryButton(cat)}
                className={`category-pill px-5 py-2.5 rounded-full text-sm font-semibold border font-body
                  ${activeCategory === cat
                    ? "bg-olive text-white border-olive"
                    : "bg-white text-olive border-sage/30 hover:bg-sage/10"
                  }`}
              >
                {cat}
              </button>
            ))}
          </div>

          {/* Product Grid - Full Width */}
          {loading ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
              {Array.from({ length: 8 }).map((_, i) => (
                <div key={i} className="bg-sage/5 rounded-2xl h-72 animate-pulse" />
              ))}
            </div>
          ) : filteredProducts.length === 0 ? (
            <div className="text-center py-16" data-testid="no-products-found">
              <p className="text-forest/60 text-lg font-body">No products found matching your filters.</p>
            </div>
          ) : (
            <>
              <p className="text-sm text-sage mb-5 font-body" data-testid="product-count">
                Showing {filteredProducts.length} product{filteredProducts.length !== 1 ? "s" : ""}
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5" data-testid="products-grid">
                {filteredProducts.map((p) => (
                  <Link
                    key={p.id}
                    to={`/products/${p.id}`}
                    state={{ from: "/products" }}
                    data-testid={`product-card-${p.id}`}
                    className="product-card bg-white rounded-2xl overflow-hidden shadow-sm border border-sage/15"
                  >
                    <div className="h-44 overflow-hidden bg-sage/5">
                      <img
                        src={p.image}
                        alt={p.name}
                        className="w-full h-full object-cover hover:scale-105 transition-transform duration-500"
                      />
                    </div>
                    <div className="p-4">
                      <p className="text-xs text-brown font-semibold uppercase tracking-wider font-body">{p.category}</p>
                      <h4 className="font-heading text-lg font-extrabold text-olive mt-1 leading-tight">{p.name}</h4>
                      <p className="text-xs text-forest/60 mt-2 line-clamp-2 font-body">{p.description}</p>
                    </div>
                  </Link>
                ))}
              </div>
            </>
          )}
        </div>
      </section>
    </div>
  );
}
