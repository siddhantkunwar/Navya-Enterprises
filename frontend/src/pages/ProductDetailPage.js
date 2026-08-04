import { useParams, Link, useNavigate, useLocation } from "react-router-dom";
import { ArrowLeft, CheckCircle } from "lucide-react";
import { getProductById } from "@/data/products";

export default function ProductDetailPage() {
  const { productId } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const product = getProductById(productId);

  const cameFrom = location.state?.from || null;
  const backLabel = cameFrom === "/" ? "Back to Home" : "Back to Products";

  const handleBack = () => {
    if (cameFrom) {
      navigate(cameFrom);
    } else {
      navigate(-1);
    }
  };

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
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 pb-20">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-16 items-start">
          {/* Product Image */}
          <div
            data-testid="product-main-image"
            className="rounded-2xl overflow-hidden shadow-lg bg-sage/5 border border-sage/15"
          >
            <img
              src={product.image}
              alt={product.name}
              className="w-full h-[400px] object-contain bg-white p-4"
            />
          </div>

          {/* Description + Benefits */}
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

            {/* Benefits */}
            {product.benefits && product.benefits.length > 0 && (
              <div className="mt-8" data-testid="product-benefits">
                <h3 className="font-heading text-xl text-olive font-extrabold mb-4">
                  Key <span className="font-accent italic text-brown">Benefits</span>
                </h3>
                <div className="space-y-3">
                  {product.benefits.map((b, i) => (
                    <div key={i} className="flex items-start gap-3" data-testid={`benefit-${i}`}>
                      <CheckCircle size={18} className="text-forest mt-0.5 flex-shrink-0" />
                      <span className="text-sm text-forest/80 font-body">{b}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

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

      {/* Model Variants - only show if models exist */}
      {product.models && product.models.length > 0 && (
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-20" data-testid="model-variants-section">
          <h2 className="font-heading text-2xl sm:text-3xl text-olive font-extrabold mb-8">
            Product <span className="font-accent italic text-brown">Variants</span>
          </h2>
          <div className="flex gap-5 overflow-x-auto pb-4" style={{ scrollbarWidth: "none" }}>
            {product.models.map((m, i) => (
              <div
                key={i}
                data-testid={`model-variant-${i}`}
                className="flex-shrink-0 w-72 bg-white rounded-2xl overflow-hidden shadow-sm border border-sage/15 hover:shadow-md transition-shadow"
              >
                <div className="h-44 overflow-hidden bg-white">
                  <img
                    src={m.image}
                    alt={m.name}
                    className="w-full h-full object-contain p-3"
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
