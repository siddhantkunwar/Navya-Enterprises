import { useState, useEffect } from "react";
import { useParams, Link, useNavigate, useLocation } from "react-router-dom";
import axios from "axios";
import { ArrowLeft } from "lucide-react";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

export default function ProductDetailPage() {
  const { productId } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);

  // Determine where user came from
  const cameFrom = location.state?.from || null;
  const backLabel = cameFrom === "/" ? "Back to Home" : "Back to Products";
  const backPath = cameFrom === "/" ? "/" : "/products";

  useEffect(() => {
    axios
      .get(`${API}/products/${productId}`)
      .then((r) => {
        setProduct(r.data);
        setLoading(false);
      })
      .catch((e) => {
        console.error(e);
        setLoading(false);
      });
  }, [productId]);

  const handleBack = () => {
    if (cameFrom) {
      navigate(cameFrom);
    } else {
      navigate(-1);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="w-10 h-10 border-3 border-sage border-t-olive rounded-full animate-spin" />
      </div>
    );
  }

  if (!product) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center gap-4" data-testid="product-not-found">
        <p className="text-forest/60 text-lg font-body">Product not found.</p>
        <Link to="/products" className="text-olive font-semibold underline">
          Back to Products
        </Link>
      </div>
    );
  }

  return (
    <div data-testid="product-detail-page" className="bg-white">
      {/* Back Button */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6">
        <button
          onClick={handleBack}
          data-testid="back-to-products"
          className="inline-flex items-center gap-2 text-sm text-forest/70 hover:text-olive transition-colors font-semibold"
        >
          <ArrowLeft size={18} />
          {backLabel}
        </button>
      </div>

      {/* Product Info */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-16 items-start">
          {/* Product Image */}
          <div
            data-testid="product-main-image"
            className="rounded-2xl overflow-hidden shadow-lg bg-sage/5 border border-sage/15"
          >
            <img
              src={product.image}
              alt={product.name}
              className="w-full h-[400px] object-cover"
            />
          </div>

          {/* Description */}
          <div data-testid="product-info">
            <span className="inline-block px-4 py-1.5 bg-sage/15 text-forest text-xs font-semibold rounded-full uppercase tracking-wider mb-4 font-body">
              {product.category}
            </span>
            <h1 className="font-heading text-3xl sm:text-4xl text-olive font-extrabold leading-tight">
              {product.name}
            </h1>
            <p className="mt-6 text-forest/80 leading-relaxed text-base font-body">
              {product.description}
            </p>

            {/* Quick info */}
            <div className="mt-8 p-5 bg-sage/8 rounded-xl border border-sage/15">
              <h3 className="font-heading text-lg text-olive font-extrabold mb-2">Why Choose This Product?</h3>
              <ul className="space-y-2 text-sm text-forest/70 font-body">
                <li>Field-tested for Indian agricultural conditions</li>
                <li>Available for B2B and institutional procurement</li>
                <li>Dedicated after-sales service & support</li>
              </ul>
            </div>

            <Link
              to="/connect"
              data-testid="enquiry-btn"
              className="mt-8 inline-flex items-center gap-2 px-8 py-3.5 bg-olive text-white rounded-full text-sm font-semibold hover:bg-forest transition-colors"
            >
              Enquire Now
            </Link>
          </div>
        </div>
      </section>

      {/* Model Variants */}
      {product.models && product.models.length > 0 && (
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-20" data-testid="model-variants-section">
          <h2 className="font-heading text-2xl sm:text-3xl text-olive font-extrabold mb-8">
            Available Models & Variants
          </h2>
          <div className="flex gap-5 overflow-x-auto pb-4" style={{ scrollbarWidth: "none" }}>
            {product.models.map((m, i) => (
              <div
                key={i}
                data-testid={`model-variant-${i}`}
                className="flex-shrink-0 w-72 bg-white rounded-2xl overflow-hidden shadow-sm border border-sage/15 hover:shadow-md transition-shadow"
              >
                <div className="h-44 overflow-hidden bg-sage/5">
                  <img
                    src={m.image}
                    alt={m.name}
                    className="w-full h-full object-cover"
                  />
                </div>
                <div className="p-5">
                  <h4 className="font-heading text-lg text-olive font-extrabold">{m.name}</h4>
                  {m.specs && (
                    <p className="mt-2 text-sm text-forest/60 font-body">{m.specs}</p>
                  )}
                </div>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
